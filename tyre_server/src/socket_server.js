const ws = require('nodejs-websocket');
const fs = require('fs');
const logger = require('../config/logger').applicationLogger;
const { exec } = require('child_process');
const { framesToImg, responseFrames } = require('./util/frames');
const checkRecordsDal = require('./dal/check_records_dal');
const tyreImgDal = require('./dal/tyre_imgs_dal');
const redisDB = require('./db/conn').redisDB;


/*
 * 存储客户端MAC地址及socket信息
 * MAC地址为键，socket对象为值
 */
const sockets = new Map();


/*
 * 客户端消息帧缓冲区
 * MAC地址为键，值为数组结构[socket, framesNum, [frames], firstTime, isHandle]
 * 其中framesNum为总帧数，frames为存储帧的数组，firstTime为首帧接收时间，isHandle为是否开始执行算法任务
 * 服务端收到客户端发出的帧时，按照帧中携带的MAC地址查找键，将对应信息存储在数组中
 */
const clientBuffer = new Map();


// 超时重传时间
const framesTimeout = 3000;


const socketServer = ws.createServer(socket => {

  // 监听客户端心跳包文本消息
  socket.on('text', str => {
    if (str === 'ping') {
      socket.sendText('pong');
      console.log('heart');
    }
  });

  // 监听客户端消息帧
  socket.on('binary', inStream => {
    inStream.on('readable', () => {
      // 接收客户端发送的帧
      const frame = inStream.read();
      // 客户端MAC地址
      const mac = frame.toString('utf8', 4, 4 + 17);
      // 存储客户端MAC地址及socket信息
      if (!sockets.has(mac)) {
        sockets.set(mac, socket);
      }
      // 将帧置入缓冲区中
      if (!clientBuffer.has(mac)) {
        // 总帧数
        const framesNum = frame.readIntBE(53, 4);
        clientBuffer.set(mac, [socket, framesNum, [frame], new Date().getTime(), false]);
      } else {
        clientBuffer.get(mac)[2].push(frame);
      }
    });
  });

  // 客户端关闭socket
  socket.on('close', () => {
    for (const [k, v] of sockets) {  
      if (v === socket) {
        // 清除redis指令信息
        redisDB.hDel(k, 'instruction', 'data', 'counter');
        // 清空socket信息
        sockets.delete(k);
      }
    }
    // 清空消息帧缓冲区信息
    for (const [k, v] of clientBuffer) {
      if (v[0] === socket) {
        clientBuffer.delete(k);
      }
    }
    console.log('connection has closed');
  });

  // socket异常处理
  socket.on('error', (code, reason) => {
    // 记录日志
    logger.error('socket连接异常: ' + code + ' ' + reason);
  });

});


// 定时器，执行识别任务
setInterval(async () => {
  // 检查缓冲区中是否有帧接收完毕
  for (const [, value] of clientBuffer) {
    const buffer = value;
    if (buffer[4] ||  buffer[1] !== buffer[2].length) {
      continue;
    }
    // 帧接收完毕
    buffer[4] = true;
    const frameList = buffer[2];
    // 将帧还原为图像和参数
    const { imgBuffer, params } = framesToImg(frameList);
    const frameId = params['frame_id'];
    const checkType = params['check_type'];
    const mac = params['mac'];
    const instruction = params['instruction'];
    // 查询redisDB是否存在对应mac的指令信息，若不存在说明是新的socket连接
    // 存储指令信息
    const action = await redisDB.hGet(mac, 'instruction');
    if (action === null) {
      console.log('存储指令')
      // 指令信息
      redisDB.hSet(mac, 'instruction', instruction);
      // 缓存数据
      redisDB.hSet(mac, 'data', JSON.stringify([]));
      // 计数器
      redisDB.hSet(mac, 'counter', '0');
    }
    // 根据检测任务类型将图片写入文件，写入文件的路径后期可以更改
    if (parseInt(checkType) === 0) {
      // 缺陷检测，后续这里注意图片类型
      fs.writeFileSync(`imgs/qx/original/${frameId}.bmp`, imgBuffer);
    } else {
      // 内外侧检测
      fs.writeFileSync(`imgs/nwc/${frameId}.jpg`, imgBuffer);
    }
    // 传递给子进程的参数字符串
    const paraStr = 
      ` ${frameId} ${Buffer.from(JSON.stringify({...params['algorithm'], check_type: checkType})).toString('base64')}`;
    // 开始检测时间
    const startTime = new Date();
    // 开启子进程，调用python算法模块，执行算法识别任务
    exec('python src/py/main.py' + paraStr, async (error, stdout) => {
      let frames = null;
      let res = null;
      let msg = null;
      // 算法模块执行错误
      if (error) {
        // 记录日志
        logger.error('算法模块执行异常: ' + error);
        // 向客户端发送错误帧
        frames = responseFrames(400, null, null, '算法模块执行错误');
      } else {
        console.log(stdout)
        resData = JSON.parse(stdout);
        res = resData.res;
        msg = resData.msg;
        console.log(res)
        // 如果是缺陷检测且检测出缺陷，读取结果目录下的结果图像
        // 其余情况直接返回原图像
        let resImg = null;
        if (parseInt(checkType) === 0 && res === 0) {
          try {
            resImg = fs.readFileSync(`imgs/qx/result/${frameId}.bmp`);
          } catch (e) {
            logger.error('读取结果图像异常');
          }
        } else {
          resImg = imgBuffer;
        }
        console.log('已读取结果图像')
        frames = responseFrames(200, resImg, stdout);
        console.log(frames.length)
      }
      // 向客户端发送响应帧
      const socket = sockets.get(mac);
      console.log('响应ock')
      for (let frame of frames) {
        // 这里多一步判断是为了防止客户端在服务端响应时突然断开
        if (socket) {
          socket.sendBinary(frame);
        }
      }
      // 在数据库中存储检测结果和图像
      checkRecordsDal.store({
        frameId: params['frame_id'],
        tyreType: params['tyre_type'],
        lineNumber: params['line_number'],
        clientMac: mac,
        startTime: startTime,
        endTime: new Date(),
        checkType: checkType,
        acceptable: error ? 3 : res,
        description: error ? '' : msg,
      });
      tyreImgDal.store({
        checkRecordId: params['frame_id'],
        originalPath: parseInt(checkType) === 0 ? `imgs/qx/original/${frameId}.bmp` :
          `imgs/nwc/${frameId}.jpg`,
        resultPath: parseInt(checkType) === 0 && res === 0 ? `imgs/qx/result/${frameId}.bmp` : '',
      });
      // 动作指令计数器 + 1
      const rrr = await redisDB.hGet(mac, 'instruction');
      console.log(rrr);

      // 清空缓冲区
      clientBuffer.delete(mac);
    });
  }
}, 30);



// 定时器，检测是否丢帧
setInterval(() => {
  const current = new Date().getTime()
  for (let [, v] of clientBuffer) {
    // 如果当前时间减去首帧到达时间超过最大限定时间，则需要客户端重传
    const buffer = v;
    if (buffer[1] !== buffer[2].length && buffer[3] !== null && current - buffer[3] > framesTimeout) {
      buffer[3] = null;
      buffer[2] = [];
      // 向客户端发送重传帧
      const frame = responseFrames(300);
      if (buffer[0]) {
        buffer[0].sendBinary(frame[0]);
      }
    }
  }
}, 300);



// 捕获全局异常
process.on('uncaughtException', err => {
  console.log(err.stack);
  // 记录日志
  logger.error('服务端异常: ' + err);
});


socketServer.listen(9090); 
const UUID = require('uuid');


// 将接收到的帧序列还原为图像，并提取算法参数
const framesToImg = (frameList) => {
  // 按帧索引排序
  frameList.sort((preFrame, nextFrame) => {
    return preFrame.readIntBE(57, 4) - nextFrame.readIntBE(57, 4);
  });
  const imgList = [];
  // 将除最后一帧外的帧还原为图像
  for (const frame of frameList) {
    imgList.push(frame.slice(63));
  }
  const imgBuffer = Buffer.concat(imgList);
  // 提取最后一帧中的参数
  const lastFrame = frameList[frameList.length - 1];
  // 客户端MAC地址，帧ID
  const mac = lastFrame.slice(4, 21).toString('utf-8');
  const frameId = lastFrame.slice(21, 53).toString('utf-8');
  const params = JSON.parse(lastFrame.slice(63).toString('utf8'));
  params.mac = mac;
  params['frame_id'] = frameId;
  // 返回图片字节流及参数对象
  return { imgBuffer, params };
}


// 封装响应帧
const responseFrames = (type, imgBuffer, resJson, errMsg) => {
  const resArr = [];
  // 按响应类型封装数据实体
  if (type === 300) {
    // 重传帧，无数据实体
    resArr.push(Buffer.alloc(0));
  } else if (type === 400) {
    // 错误帧
    resArr.push(Buffer.from(JSON.stringify({ res: false, msg: errMsg }), 'utf8'));
  } else {
    if (imgBuffer === null) {
      resArr.push(Buffer.from(resJson));
    } else {
      // 图像帧，每帧长度不超过32kB
      const dataLen = 32 * 1024;
      for (let i = 0; i < Math.floor(imgBuffer.length / dataLen); i++) {
        const frame = imgBuffer.slice(dataLen * i, dataLen * (i + 1));
        resArr.push(frame);
      }
    }
  }
  const frameId = UUID.v1().replace(/-/g, '');
  const total = Buffer.alloc(4);
  total.writeIntBE(resArr.length + 1, 0, 4);
  const status = Buffer.alloc(2);
  status.writeIntBE(200, 0, 2);
  console.log(resArr.length)
  // 封装首部
  if (resArr.length > 1) {
    console.log(typeof resJson)
    for (let i = 0; i < resArr.length; i++) {
      const current = Buffer.alloc(4);
      current.writeIntBE(i, 0, 4);
      const frameHead = Buffer.concat([
        // 帧头 4字节 0000表示请求帧，1111表示响应帧
        Buffer.from('1111', 'utf8'),
        // 帧标识 32字节 随机生成uuid
        Buffer.from(frameId, 'utf8'),
        // 总帧数 4字节 大端模式存储，总帧数为图像帧数 + 结果参数1帧
        total,
        // 当前帧索引 4字节 大端模式存储
        current,
        // 状态码 2字节 200表示正常 300表示重传 400表示异常
        status,
      ]);
      // 数据实体，除最后一帧外其余帧皆为图像帧，最后一帧为结果参数
      resArr[i] = Buffer.concat([frameHead, resArr[i]]);
    }
    // 封装结果参数帧
    const current = Buffer.alloc(4);
    current.writeIntBE(resArr.length, 0, 4);
    resArr.push(Buffer.concat([
      Buffer.from('1111', 'utf8'),
      Buffer.from(frameId, 'utf8'),
      total,
      current,
      status,
      Buffer.from(resJson, 'utf8')
    ]));
  } else {
    const total = Buffer.alloc(4);
    total.writeIntBE(1, 0, 4);
    const current = Buffer.alloc(4);
    current.writeIntBE(0, 0, 4);
    const status = Buffer.alloc(2);
    status.writeIntBE(type, 0, 2);
    resArr[0] = Buffer.concat([
      Buffer.from('1111', 'utf8'),
      Buffer.from(frameId, 'utf8'),
      total,
      current,
      status,
      resArr[0],
    ]);
  }
  console.log('总帧数:' + resArr.length)
  return resArr;
}


module.exports = {
  framesToImg,
  responseFrames,
};
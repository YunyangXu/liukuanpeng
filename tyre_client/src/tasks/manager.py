import sys, os

sys.path.append(os.path.join(__file__, '../../'))
from datetime import datetime
import json

from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from common.commlib import imgToFrames
from common.enums import socketStateEnum


'''
  设备缓冲区管理器
  1. 循环读取缓冲区
  2. 通知窗口线程显示图片
  3. 将图像bytearray拆分并封装成帧，发送到服务端
  4. 处理重传
'''
class DeviceBufferManager(QThread):
  
  # 线程退出标识
  exitFlag = False
  # 串行锁，每发送一副图像后加锁，接收到结果图像后解锁
  serialLock = False
  # 通知网络线程信号
  sockSignal = pyqtSignal(bytearray)
  # 弹出警告窗口信号
  showAlertSignal = pyqtSignal(str)
  # 通知主窗口显示图像
  showLeftImageSignal = pyqtSignal(bytearray)
  # 通知检测信息面板显示参数
  showParams = pyqtSignal(bool, bool, object, object)


  def __init__(self, config, buffer, socket):

    super().__init__()
    self.config = config
    self.buffer = buffer
    self.socket = socket
    self.sockSignal.connect(self.noticeSocket)
    # 每幅图像发送后开始计时，超过限定时间没有响应，提示用户
    self.preTime = None
    self.unlockTime = 10
    self.preTimeMutex = QMutex()
    # 当前图像帧序列，用于重传
    self.preFrames = None
    # 重传标识
    self.retransFlag = False
    self.retransFlagMutex = QMutex()
    

  def run(self):
    while True:

      if self.exitFlag:
        break

      # 超过规定时间服务端未响应，未解锁
      self.preTimeMutex.lock()
      if self.preTime and (datetime.now() - self.preTime).seconds > self.unlockTime and self.serialLock:
        # 如果不是由于重连导致超时
        if self.socket.getSocketState() != socketStateEnum.reconnecting:
          self.showAlertSignal.emit('服务端未响应，请关闭程序并查看服务端日志')
          self.preTime = None
      self.preTimeMutex.unlock()

      # 由于网络重连或丢帧而进行重传
      self.retransFlagMutex.lock()
      if self.retransFlag:
        # 重传，发送至网络线程
        print('正在重传...')
        for i in range(0, len(self.preFrames)):
          self.sockSignal.emit(self.preFrames[i])
        self.retransFlag = False
        self.preTime = datetime.now()
      self.retransFlagMutex.unlock()

      if self.serialLock:
        continue

      # 这里后期需要修改
      # 目前在buffer队列中存储的是整张图像的bytearray
      # 后期根据具体的相机通信协议，可能需要将多个帧组合成完整的bytearray
      if not self.serialLock:
        try:
          imgArr = self.buffer.get(True, timeout=1)
        except:
          continue

        # 通知主窗口显示图像
        self.showLeftImageSignal.emit(imgArr)
        self.showParams.emit(False, False, None, None) 
        res = imgToFrames(self.config, imgArr)
        self.preFrames = res
        print('发送帧')
        # 发送至网络线程
        for i in range(0, len(res)):
          self.sockSignal.emit(res[i])

      # 加锁
      self.serialLock = True
      self.preTime = datetime.now()


  def noticeSocket(self, frame):
    self.socket.sendImageFrames(frame)

  def unlock(self):
    self.preTimeMutex.lock()
    print('解锁')
    self.serialLock = False
    self.preTime = None
    self.preTimeMutex.unlock()

  def reTransmission(self):
    self.retransFlagMutex.lock()
    self.retransFlag = True
    self.retransFlagMutex.unlock()


'''
  服务器缓冲区管理器
  1. 循环读取缓冲区
  2. 将服务端响应帧还原成图片，通知窗口线程显示结果图片
  3. 通知窗口线程显示结果图片
  4. 通知设备缓冲区管理器线程解锁
  5. 通知设备缓冲区管理器线程重传
'''
class ServerBufferManager(QThread):
  
  # 线程退出标识
  exitFlag = False
  # 通知设备缓冲区管理器线程解锁
  unlockSignal = pyqtSignal()
  # 通知主窗口显示图像
  showRightImageSignal = pyqtSignal(bytearray)
  # 通知检测信息面板显示参数
  showParams = pyqtSignal(bool, bool, object, object)
  # 弹出警告窗口
  showAlertSignal = pyqtSignal(str)
  # 重传信号
  retransSignal = pyqtSignal()

  def __init__(self, buffer, socket):

    super().__init__()
    self.buffer = buffer
    self.socket = socket
    # 总帧数
    self.totalFramesNum = 0
    self.counter = 0
    # 帧序列
    self.frames = []
    
  
  def run(self):
    while True:
      if self.exitFlag:
        break
      try:
        frame = self.buffer.get(True, timeout=1)
      except:
        continue
      print('拿到帧')
      if self.counter == 0:
        self.totalFramesNum = int.from_bytes(frame.data()[36:40], byteorder='big')
        print('返回总帧数: ' + str(self.totalFramesNum))
      self.counter += 1
      self.frames.append(frame)
      if self.counter == self.totalFramesNum:
        print('hhh')
        if self.totalFramesNum != 1:
          # 排序
          self.frames.sort(key=lambda x: int.from_bytes(x.data()[40:44], byteorder='big'))
          # 提取图像
          img = bytearray()
          for i in range(0, len(self.frames) - 1):
            img += bytearray(self.frames[i].data()[46:])
          self.showRightImageSignal.emit(img)
          # 提取参数
          paramsStr = self.frames[-1].data()[46:]
          params = json.loads(paramsStr.decode('utf-8'))
          print(params)
          res = params['res']
          msgs = params['msg']
          # 检测出缺陷
          if res == 0:
            for i in range(0, len(msgs)):
              msgs[i] = str(i + 1) + ': ' + msgs[i]
            self.showParams.emit(False, True, res, '   '.join(msgs))
          # 检测通过
          elif res == 1:
            self.showParams.emit(False, True, res, '')
          # 检测失败
          else:
            self.showParams.emit(False, True, res, msgs[0])
        else:
          statusCode = int.from_bytes(self.frames[0].data()[44:46], byteorder='big')
          # 错误帧
          if statusCode == 400:
            params = json.loads(self.frames[0].data()[46:].decode('utf-8'))
            self.showParams.emit(False, True, 2, params['msg'])
          # 重传帧
          else:
            print('重传')
            self.retransSignal.emit()
            self.totalFramesNum = 0
            self.counter = 0
            self.frames.clear()
            continue

        self.totalFramesNum = 0
        self.counter = 0
        self.frames.clear()
        # 休眠1秒是为了看清楚检测结果，后续可以修改或去掉
        self.sleep(1)
        self.unlockSignal.emit()

        
        
import sys, os
sys.path.append(os.path.join(__file__, '../../'))

from PyQt5.QtCore import QObject, QUrl, QTimer,  pyqtSignal
from PyQt5.QtWebSockets import QWebSocket
from common.enums import socketStateEnum

configPath = os.path.join(__file__, '../../../') + '/config'


'''
  对Websocket通信过程进行封装，SocketClient类用于与服务端Node进程通信，
  若X光扫描图像需要截屏通过网络传输，可在本文件中继续封装SocketServer类
'''
class SocketClient(QObject):

  # 更新状态信息信号
  updateInfoSignal = pyqtSignal([str, bool])
  statusSignal = pyqtSignal([bool, str])
  # 通知device线程重传
  retransSignal = pyqtSignal()


  def __init__(self, config, buffer):

    super().__init__()

    basicSetting = config['basic_setting']
    ip = basicSetting['ip_address']
    port = basicSetting['port']
    self.url = 'ws://' + ip + ':' + port + '/sock'
    
    # 缓冲区
    self.buffer = buffer
    # socket实例
    self.socket = None
    # socket状态
    self.socketState = socketStateEnum.stateNone
    # 是否手动关闭
    self.closeByHand = False
    # 心跳包内容
    self.heartBeatText = 'ping'
    # 心跳数据发送时间间隔
    self.heartBeatTime = 20 * 1000
    # 需要重连的心跳发送失败次数
    self.reconnectHeartBeatCounter = 3
    # 重连时间间隔
    self.reconnectTime = 1 * 1000
    # 心跳发送失败次数
    self.heartBeatFailedCounter = 0
    # 重连失败次数
    self.reconnectFailedCounter = 0
    # 最大重连次数
    self.maxReconnectNum = 1
    # 心跳发送定时器
    self.heartBeatTimer = QTimer()
    # 重连定时器
    self.reconnectTimer = QTimer()


  # 开启连接
  def connect(self):
    self.socket = QWebSocket()
    self.socket.open(QUrl(self.url))
    # 首次连接，绑定槽函数
    if self.socketState == socketStateEnum.stateNone:
      self.socket.connected.connect(self.onConnected)
      self.socket.disconnected.connect(self.onDisconnected)
      self.socket.binaryFrameReceived.connect(self.receiveImageFrames)
      self.heartBeatTimer.timeout.connect(self.heartBeat)
      self.reconnectTimer.timeout.connect(self.reconnect)


  # 重连
  def reconnect(self):
    self.reconnectTimer.stop()
    # 关闭当前连接
    self.socket.close()
    # 如果达到最大重连次数，不再重连，此时处于断开状态
    if self.reconnectFailedCounter == self.maxReconnectNum:
      self.socketState = socketStateEnum.disconnected
      self.reconnectTimer.stop()
      self.statusSignal.emit(False, '网络异常断开，服务已停止，请关闭程序重试')
      self.reconnectFailedCounter = 0
    # 开始连接
    else:
      self.reconnectFailedCounter += 1
      self.connect()
    
  
  # 断开连接
  def disconnect(self): 
    self.closeByHand = True
    if self.socketState != socketStateEnum.stateNone:
      self.socket.close()
    # 释放socket连接
    del self.socket
    self.socketState = socketStateEnum.disconnected
    self.heartBeatTimer.stop()
    self.reconnectTimer.stop()

  
  # 连接成功
  def onConnected(self):
    self.updateInfoSignal.emit('serverStatusLabel', True)
    # 如果重连成功，停止重连的timer
    if self.socketState == socketStateEnum.reconnecting:
      self.reconnectTimer.stop()
      # 重连成功后要通知device线程重传
      self.retransSignal.emit()
    self.socketState = socketStateEnum.connected
    # 开始发送心跳包
    self.heartBeatTimer.start(self.heartBeatTime)
    self.reconnectFailedCounter = 0
    self.reconnectHeartBeatCounter = 0


  # 连接断开，服务器主动断开或异常断开时触发此方法
  def onDisconnected(self):
    # 如果不是手动关闭，则需要重连
    if not self.closeByHand:
      self.heartBeatTimer.stop()
      self.reconnectTimer.start(self.reconnectTime)
      self.socketState = socketStateEnum.reconnecting

  
  # 发送图像帧
  def sendImageFrames(self, frame):
    self.socket.sendBinaryMessage(frame)


  # 接收图像帧
  def receiveImageFrames(self, frame):
    self.buffer.put(frame)


  # 定时发送心跳包，保持与Nginx代理服务器的长连接
  def heartBeat(self):
    sendBytes = self.socket.sendTextMessage(self.heartBeatText)
    # 发送心跳失败
    if sendBytes != len(self.heartBeatText):
      self.heartBeatFailedCounter += 1
      # 心跳失败次数等于需要重连的次数
      if self.heartBeatFailedCounter == self.reconnectHeartBeatCounter:
        self.heartBeatTimer.stop()
        self.reconnectTimer.start(self.reconnectTime)
        self.socketState = socketStateEnum.reconnecting

  
  # 获取连接状态
  def getSocketState(self):
    return self.socketState
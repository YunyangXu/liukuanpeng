import sys, os
sys.path.append(os.path.join(__file__, '../../'))
import json

from datetime import datetime
from queue import Queue
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QLabel
from PyQt5.QtGui import QColor, QEnterEvent, QMouseEvent
from PyQt5.QtCore import Qt, QPoint
from layouts.FlexiableLayout import FlexiableLayoutWindow
from widgets.MainTitleBar import MainTitleBarWidget
from widgets.MainWindowPanel import MainWindowPanelWidget
from widgets.MainMenu import MainMenuWidget
from pages.ConfirmWindow import ConfirmWindowPage
from pages.AlertWindow import AlertWindowPage
from pages.CameraWindow import CameraWindowPage
from pages.NetworkWindow import NetworkWindowPage
from pages.ParameterWindow import ParameterWindowPage
from pages.TableWindow import TableWindowPage
from tasks.sockets import SocketClient
from common.commlib import loadQss
from common.enums import socketStateEnum
from tasks.imitate import ReadImage
from tasks.manager import DeviceBufferManager, ServerBufferManager

staticPath = os.path.join(__file__, '../../../') + '/static'
configPath = os.path.join(__file__, '../../../') + '/config'


class MainWindowPage(FlexiableLayoutWindow):
  # 是否开启服务
  serviceFlag = False
  # 是否开始检测
  detectionFlag = False
  # 程序开始运行时间戳
  startTimestamp = None
  # 缓冲区：用于接收相机或X光机的图像帧
  deviceBuffer = Queue()
  # 缓冲区：用于接收服务器回传的消息帧
  serverBuffer = Queue()
  # socket连接
  socketClient = None
  # 读取图像模拟任务
  readImageTask = None
  # 设备缓冲区管理器
  deviceBufferManager = None
  # 服务器缓冲区管理器
  serverBufferManager = None
  # 正在检测第n幅图像
  imgCheckCounter = 1

  def __init__(self):
    # 主窗口尺寸
    self.windowWidth = 1520
    self.windowHeight = 900

    # 阴影设置
    self.shadowX = 0
    self.shadowY = 0
    self.shadowWidth = 60
    self.shadowColor = QColor(132, 132, 132)

    # 样式表
    self.qss = staticPath + '/qss/main_window.qss'

    # 窗口标题
    self.windowTitle = '轮胎缺陷监测系统V3.0'

    super(MainWindowPage, self).__init__(False, self.windowWidth, 
      self.windowHeight, self.shadowX, self.shadowY, self.shadowWidth, self.shadowColor)

    self.renderWindow()
    self.enableFunctions()
    self.startTimestamp = datetime.now()


  def renderWindow(self):
    # 加载样式表
    self.setStyleSheet(loadQss(self.qss))

    # 布局
    self.mainGridLayout = QGridLayout()

    # 设置周围阴影
    self.mainGridLayout.setContentsMargins(self.shadowWidth, self.shadowWidth, 
      self.shadowWidth, self.shadowWidth)
    self.mainGridLayout.setSpacing(0)

    self.setWindowTitle(self.windowTitle)
    
    # 主窗口标题栏
    self.menuBar = MainTitleBarWidget(self.windowTitle)
    self.menuBar.windowMove.connect(self.move)
    self.menuBar.windowFullScreen.connect(self.changeWindowSize)
    self.menuBar.installEventFilter(self)
    self.menuBar.showSubWindow.connect(self.showExitWindow)
    self.menuBar.showMainMenu.connect(self.showMenu)
    
    # 主窗口面板
    self.mainPanel = MainWindowPanelWidget()
    self.mainPanel.setObjectName('mainWindowPanel')
    self.mainPanel.installEventFilter(self)
    self.mainPanel.showSubWindow.connect(self.showCameraWindow)
    self.mainPanel.showNetworkWindow.connect(self.showNetworkWindow)
    self.mainPanel.showParaWindow.connect(self.showParaWindow)
    self.mainPanel.showTableWindow.connect(self.showTableWindow)
    self.mainPanel.showAlertWindow.connect(self.showAlertWindow)
    self.mainPanel.toggleService.connect(self.toggleService)
    self.mainPanel.toggleDetection.connect(self.toggleDetection)
    
    self.mainGridLayout.addWidget(self.menuBar)
    self.mainGridLayout.addWidget(self.mainPanel)
    self.mainWidget.setLayout(self.mainGridLayout)

    # 主菜单面板
    self.mainMenu = MainMenuWidget()
    self.mainMenu.setParent(self)
    self.mainMenu.hide()
    self.mainMenu.togglePanelSignal.connect(self.togglePanel)
    self.mainMenu.showExitWindowSignal.connect(self.showExitWindow)

    # 相机窗口
    self.cameraWindow = CameraWindowPage()
    self.cameraWindow.setWindowModality(Qt.ApplicationModal)
    self.cameraWindow.showAlertSignal.connect(self.showAlertWindow)
    self.cameraWindow.hide()

    # 网络设置窗口
    self.networkWindow = NetworkWindowPage()
    self.networkWindow.showAlertSignal.connect(self.showAlertWindow)
    self.networkWindow.setBtnEnableSignal.connect(self.setBtnEnable)
    self.networkWindow.hide()

    # 参数设置窗口
    self.parameterWindow = ParameterWindowPage()
    self.parameterWindow.showAlertSignal.connect(self.showAlertWindow)
    self.parameterWindow.setBtnEnableSignal.connect(self.setBtnEnable)
    self.parameterWindow.hide()

    # 检测结果窗口
    self.tableWindow = TableWindowPage()
    self.tableWindow.hide()

    # 确认窗口
    self.confirmWindow = ConfirmWindowPage()
    self.confirmWindow.setWindowModality(Qt.ApplicationModal)
    self.confirmWindow.confirmSignal.connect(self.exitSystem)

    # 警告窗口
    self.alertWindow = AlertWindowPage()
    self.alertWindow.setWindowModality(Qt.ApplicationModal)

    self.show()


  # 检查配置文件，确定哪些功能可用
  def enableFunctions(self):
    self.mainPanel.toolPanelWidget.setAllBtnsStatus(False)
    try:
      with open(configPath + '/global.dat', 'r', encoding='utf-8') as f:
        self.clientConfig = json.load(f)
      # 如果未填写ip和端口，则提示用户填写
      if not self.clientConfig['network_enable']:
        self.mainPanel.toolPanelWidget.setBtnEnable('networkBtn')
        return self.showAlertWindow('首次使用系统，请设置网络参数')
      # 如果未配置系统运行参数，则提示用户填写
      elif not self.clientConfig['sys_enable']:
        self.mainPanel.toolPanelWidget.setBtnEnable('networkBtn')
        self.mainPanel.toolPanelWidget.setBtnEnable('settingBtn')
        return self.showAlertWindow('首次使用系统，请设置系统参数')
      else:
        self.mainPanel.toolPanelWidget.setAllBtnsStatus(True)
    except:
      self.showAlertWindow('系统无法找到配置文件，系统功能无法启用')

  
  # 设置面板按钮可用
  def setBtnEnable(self, name):
    if name == 'all':
      self.mainPanel.toolPanelWidget.setAllBtnsStatus(True)
    else:
      self.mainPanel.toolPanelWidget.setBtnEnable(name)


  # 更新状态信息面板
  def updateInfoPanel(self, item, status):
    statusArr = ['已断开', '已连接', '连接中...']
    label = self.findChild(QLabel, item)
    label.setText(statusArr[int(status)])
    if status == True:
      label.setProperty('statusLabel', 'connected')
    else:
      label.setProperty('statusLabel', 'disconnected')
    label.style().unpolish(label)
    label.style().polish(label)


  # 连接状态
  def connectionStatusSlot(self, status, msg):
    if not status:
      self.showAlertWindow(msg)
      # 有任一设备连接失败，则停止检测及服务
      self.stopDetection()
      self.stopService()
      self.mainPanel.toolPanelWidget.stopDetectionRender()
      self.mainPanel.toolPanelWidget.stopServiceRender()
    

  # 开启服务
  def startService(self):
    self.serviceFlag = True
    # 从文件中加载配置
    with open(configPath + '/global.dat', 'r', encoding='utf-8') as f:
      self.clientConfig = json.load(f)
    # 更新检测信息面板
    self.updateCheckInfoPanel(True, None, None, None)
    # Websocket连接开启
    if not self.socketClient:
      self.socketClient = SocketClient(self.clientConfig, self.serverBuffer)
      self.socketClient.updateInfoSignal.connect(self.updateInfoPanel)
      self.socketClient.statusSignal.connect(self.connectionStatusSlot) 
    self.socketClient.connect()
    # 相机、X光机、警报装置开启连接过程在这里继续补充
    # 注意：根据当前检测模式，相机和X光机的连接状态是互斥的，即系统在开启服务后只能完成同一种检测任务
    # 相机、X光机、警报装置三个连接类都要绑定updateInfoSignal和showAlertSignal
    # ...
    # ...
    # ...
    # ...
    # ...
    # 更新状态信息
    self.updateInfoPanel('serverStatusLabel', 2)


  # 停止服务
  def stopService(self):
    if self.serviceFlag:
      self.serviceFlag = False
      # 更新检测信息面板
      self.updateCheckInfoPanel(None, None, None, None)
      # 清空图像面板
      imgPanel = self.mainPanel.rightPanelWidget.imgPanel
      imgPanel.clearImgPanel('left')
      imgPanel.clearImgPanel('right')
      if self.socketClient:
        self.socketClient.disconnect()
        # 注意销毁连接占用的内存
        del self.socketClient
        self.updateInfoPanel('serverStatusLabel', 0)
      # 依次关闭相机、X光机、警报装置连接
      # ...
      # ...
      # ...
      # ...
      # ...


  # 开启/停止服务
  def toggleService(self, flag):
    # 如果此时正在执行检测任务，必须先暂停检测才能开启/停止服务
    if self.detectionFlag:
      return
    if flag:
      self.startService()
    else:
      self.stopService()


  # 开始检测
  def startDetection(self):
    # 因此检测网络连接状态、相机连接状态、X关机连接状态
    # 若连接失败或正在连接，弹窗提示
    if self.socketClient.getSocketState() != socketStateEnum.connected:
      self.mainPanel.toolPanelWidget.stopDetectionRender()
      return self.showAlertWindow('正在连接服务器，请稍后再试')
    self.detectionFlag = True
    # 开启线程
    self.readImageTask = ReadImage(self.clientConfig, self.deviceBuffer)
    self.deviceBufferManager = DeviceBufferManager(self.clientConfig, self.deviceBuffer, self.socketClient)
    self.deviceBufferManager.showAlertSignal.connect(self.showAlertWindow)
    self.deviceBufferManager.showLeftImageSignal.connect(self.updateLeftImgPanel)
    self.deviceBufferManager.showParams.connect(self.updateCheckInfoPanel)
    self.socketClient.retransSignal.connect(self.deviceBufferManager.reTransmission)
    self.serverBufferManager = ServerBufferManager(self.serverBuffer, self.socketClient)
    self.serverBufferManager.showRightImageSignal.connect(self.updateRightImgPanel)
    self.serverBufferManager.showParams.connect(self.updateCheckInfoPanel)
    self.serverBufferManager.unlockSignal.connect(self.deviceBufferManager.unlock)
    self.serverBufferManager.showAlertSignal.connect(self.showAlertWindow)
    self.serverBufferManager.retransSignal.connect(self.deviceBufferManager.reTransmission)
    self.readImageTask.start()
    self.deviceBufferManager.start()
    self.serverBufferManager.start()


  # 停止检测
  def stopDetection(self):
    if self.detectionFlag:
      self.detectionFlag = False
    # 停止线程
    if self.readImageTask:
      self.readImageTask.exitFlag = True
      self.readImageTask.quit()
    if self.deviceBufferManager:
      self.deviceBufferManager.exitFlag = True
      self.deviceBufferManager.quit()
    if self.serverBufferManager:
      self.serverBufferManager.exitFlag = True
      self.serverBufferManager.quit()
    # 清空缓冲区
    self.deviceBuffer.queue.clear()
    self.serverBuffer.queue.clear()
    

  # 开始检测/暂停检测
  def toggleDetection(self, flag):
    print(flag)
    if not self.serviceFlag:
      return
    if flag:
      self.startDetection()
    else:
      self.stopDetection()


  # 更新左侧图片面板
  def updateLeftImgPanel(self, imgArr):
    imgPanel = self.mainPanel.rightPanelWidget.imgPanel
    # 先清空右侧结果图像
    imgPanel.clearImgPanel('right')
    imgPanel.updateImgPanel(imgArr, 'left')


  # 更新右侧图片面板
  def updateRightImgPanel(self, imgArr):
    imgPanel = self.mainPanel.rightPanelWidget.imgPanel
    imgPanel.updateImgPanel(imgArr, 'right')

  
  # 更新检测信息面板
  def updateCheckInfoPanel(self, first, isFinished, res, msg):
    lineLabel = self.findChild(QLabel, 'productionLineLabel')
    lineNumber = self.clientConfig['basic_setting']['line_number']
    checkType = self.clientConfig['basic_setting']['check_type']
    checkingIcon = self.findChild(QLabel, 'checkingIcon')
    checkingLabel = self.findChild(QLabel, 'checkingLabel')
    resultLabel = self.findChild(QLabel, 'resultLabel')
    errorLabel = self.findChild(QLabel, 'errorLabel')
    if not self.serviceFlag:
      lineLabel.hide()
      checkingIcon.hide()
      checkingLabel.hide()
      resultLabel.hide()
      errorLabel.hide()
      return
    # 更新生产线编号和检测模式信息
    if first:
      if checkType == 0:
        checkType = '缺陷检测'
      else:
        checkType = '内外侧检测'
      lineLabel.setText('生产线' + lineNumber + '  ' + checkType)
      lineLabel.show()
    else:
      if isFinished:
        checkingIcon.hide()
        checkingLabel.hide()
        errorLabel.setText(msg)
        errorLabel.show()
        if res == 1:
          resultLabel.setProperty('resultLabel', True)
          resultLabel.setText('检测通过')
        elif res == 0:
          resultLabel.setProperty('resultLabel', False)
          resultLabel.setText('检测不通过')
        else:
          resultLabel.setProperty('resultLabel', False)
          resultLabel.setText('检测失败') 
        resultLabel.style().unpolish(resultLabel)
        resultLabel.style().polish(resultLabel)
        resultLabel.show()
      else:
        checkingIcon.show()
        checkingLabel.setText('正在检测第 ' + str(self.imgCheckCounter) + ' 幅图像')
        self.imgCheckCounter += 1
        checkingLabel.show()
        resultLabel.hide()
        errorLabel.hide()


  # 显示主菜单
  def showMenu(self, msg):
    if msg:
      self.mainMenu.setPosition()
      self.mainMenu.show()
    else:
      self.mainMenu.hide()


  # 显示/隐藏面板
  def togglePanel(self, type):
    widget = self.findChild(QWidget, type)
    if widget.isHidden():
      widget.show()
    else:
      widget.hide()


  # 显示相机窗口
  def showCameraWindow(self):
    if not self.serviceFlag:
      return self.showAlertWindow('请开启服务后再调整相机')
    if self.detectionFlag:
      return self.showAlertWindow('请暂停检测后再调整相机')
    self.cameraWindow.openCamera()

  
  # 显示网络设置窗口
  def showNetworkWindow(self):
    if self.serviceFlag:
      return self.showAlertWindow('请停止服务后再设置网络参数')
    self.networkWindow.show()
    self.networkWindow.fillPara()


  # 显示参数设置窗口
  def showParaWindow(self):
    if self.serviceFlag:
      return self.showAlertWindow('请停止服务后再设置参数')
    self.parameterWindow.show()
    # 请求服务端参数
    self.parameterWindow.getSelections()


  # 显示检测结果窗口
  def showTableWindow(self):
    self.tableWindow.show()


  # 显示退出系统确认窗口
  def showExitWindow(self):
    if self.detectionFlag or self.serviceFlag:
      return self.showAlertWindow('请暂停检测及停止服务后再退出系统')
    self.confirmWindow.setMessage('确定要退出系统吗？')
    self.confirmWindow.show()


  # 退出系统
  def exitSystem(self):
    QApplication.instance().quit()


  # 显示警告窗口
  def showAlertWindow(self, msg):
    self.alertWindow.setMessage(msg)
    self.alertWindow.show()


  # 槽函数，响应全屏信号
  def changeWindowSize(self, msg):
    if (msg == 'max'):
      if (self.isFullScreen()):
        self.mainGridLayout.setContentsMargins(self.shadowWidth, self.shadowWidth, 
          self.shadowWidth, self.shadowWidth)
        self.showNormal()
      else:
        self.mainGridLayout.setContentsMargins(0, 0, 0, 0)
        self.showFullScreen()
      self.mainMenu.update()
    else:
      self.showMinimized()
  

  # 槽函数，响应移动窗口的信号
  def move(self, pos):
    # 窗口处于全屏或最大化状态时不允许移动
    if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
      return
    super(MainWindowPage, self).move(pos - QPoint(self.shadowWidth, self.shadowWidth))


  # 事件过滤
  def eventFilter(self, obj, e):
    if isinstance(e, QEnterEvent):
      self.setCursor(Qt.ArrowCursor)
    # 点击面板任意位置收起菜单
    if isinstance(e, QMouseEvent):
      self.showMenu(False)
    return super(MainWindowPage, self).eventFilter(obj, e)


  def getShadowWidth(self):
    return self.shadowWidth


  def getMenuBarHeight(self):
    return self.menuBar.height()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  mw = MainWindowPage()
  sys.exit(app.exec_())
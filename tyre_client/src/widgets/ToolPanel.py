import os, sys
sys.path.append(os.path.join(__file__, '../../'))
from PyQt5.QtWidgets import QWidget, QToolButton, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from common.commlib import loadQss, getRootWidget

staticPath = os.path.join(__file__, '../../../') + '/static'


class ToolPanelWidget(QWidget):

  # 显示相机窗口信号
  showSubWindow = pyqtSignal()
  # 显示网络设置窗口信号
  showNetworkWindow = pyqtSignal()
  # 显示参数设置窗口信号
  showParaWindow = pyqtSignal()
  # 显示检测结果窗口信号
  showTableWindow = pyqtSignal()
  # 显示警告窗口信号
  showAlertWindow = pyqtSignal(str)
  # 开启/停止服务信号
  toggleService = pyqtSignal(bool)
  # 开始/暂停检测信号
  toggleDetection = pyqtSignal(bool)


  def __init__(self):
    super().__init__()

    # 工具栏宽度
    self.toolMaxWidth = 120

    # 按钮尺寸
    self.btnSize = 100
    # 按钮图标尺寸
    self.btnIconSize = 48

    # 样式表
    self.qss = staticPath + '/qss/tool_panel.qss'

    self.render()
      
  def render(self):
    self.setAttribute(Qt.WA_StyledBackground, True)

    # 加载样式表
    self.setObjectName('toolPanel')
    self.setStyleSheet(loadQss(self.qss))

    self.setMaximumWidth(self.toolMaxWidth)

    # 布局
    self.toolPanelLayout = QVBoxLayout()
    self.toolPanelLayout.setContentsMargins(10, 10, 10, 10)
    
    self.iconPath = staticPath + '/icons/'

    self.serviceBtn = QToolButton()
    self.serviceBtn.setObjectName('serviceBtn')
    self.serviceBtn.setIcon(QIcon(self.iconPath + 'service_start.svg'))
    self.serviceBtn.setIconSize(QSize(self.btnIconSize, self.btnIconSize))
    self.serviceBtn.setText('开启服务')
    self.serviceBtn.setToolTip('开启服务')
    self.serviceBtn.setFont(QFont('Microsoft YaHei'))
    self.serviceBtn.setCursor(Qt.PointingHandCursor)
    self.serviceBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)  
    self.serviceBtn.setFixedSize(self.btnSize, self.btnSize)
    self.serviceBtn.clicked.connect(self.toggleServiceRender)

    self.camBtn = QToolButton()
    self.camBtn.setObjectName('camBtn')
    self.camBtn.setIcon(QIcon(self.iconPath + 'camera.svg'))
    self.camBtn.setIconSize(QSize(self.btnIconSize, self.btnIconSize))
    self.camBtn.setText('相机调整')
    self.camBtn.setToolTip('相机调整')
    self.camBtn.setFont(QFont('Microsoft YaHei'))
    self.camBtn.setCursor(Qt.PointingHandCursor)
    self.camBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    self.camBtn.setFixedSize(self.btnSize, self.btnSize)
    self.camBtn.clicked.connect(self.showSubWindow.emit)

    self.startBtn = QToolButton()
    self.startBtn.setObjectName('startBtn')
    self.startBtn.setIcon(QIcon(self.iconPath + 'start.svg'))
    self.startBtn.setIconSize(QSize(self.btnIconSize, self.btnIconSize))
    self.startBtn.setText('开始检测')
    self.startBtn.setToolTip('开始检测')
    self.startBtn.setFont(QFont('Microsoft YaHei'))
    self.startBtn.setCursor(Qt.PointingHandCursor)
    self.startBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    self.startBtn.setFixedSize(self.btnSize, self.btnSize)
    self.startBtn.clicked.connect(self.toggleDetectionRender)

    self.networkBtn = QToolButton()
    self.networkBtn.setObjectName('networkBtn')
    self.networkBtn.setIcon(QIcon(self.iconPath + 'network.svg'))
    self.networkBtn.setIconSize(QSize(self.btnIconSize, self.btnIconSize))
    self.networkBtn.setText('网络设置')
    self.networkBtn.setToolTip('网络设置')
    self.networkBtn.setFont(QFont('Microsoft YaHei'))
    self.networkBtn.setCursor(Qt.PointingHandCursor)
    self.networkBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    self.networkBtn.setFixedSize(self.btnSize, self.btnSize)
    self.networkBtn.clicked.connect(self.showNetworkWindow.emit)

    self.settingBtn = QToolButton()
    self.settingBtn.setObjectName('settingBtn')
    self.settingBtn.setIcon(QIcon(self.iconPath + 'setting.svg'))
    self.settingBtn.setIconSize(QSize(self.btnIconSize, self.btnIconSize))
    self.settingBtn.setText('参数设置')
    self.settingBtn.setToolTip('参数设置')
    self.settingBtn.setFont(QFont('Microsoft YaHei'))
    self.settingBtn.setCursor(Qt.PointingHandCursor)
    self.settingBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    self.settingBtn.setFixedSize(self.btnSize, self.btnSize)
    self.settingBtn.clicked.connect(self.showParaWindow.emit)

    self.resultBtn = QToolButton()
    self.resultBtn.setObjectName('resultBtn')
    self.resultBtn.setIcon(QIcon(self.iconPath + 'result.svg'))
    self.resultBtn.setIconSize(QSize(self.btnIconSize, self.btnIconSize))
    self.resultBtn.setText('结果分析')
    self.resultBtn.setToolTip('结果分析')
    self.resultBtn.setFont(QFont('Microsoft YaHei'))
    self.resultBtn.setCursor(Qt.PointingHandCursor)
    self.resultBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    self.resultBtn.setFixedSize(self.btnSize, self.btnSize)
    self.resultBtn.clicked.connect(self.showTableWindow.emit)

    self.toolPanelLayout.addWidget(self.serviceBtn)
    self.toolPanelLayout.addWidget(self.camBtn)
    self.toolPanelLayout.addWidget(self.startBtn)
    self.toolPanelLayout.addWidget(self.networkBtn)
    self.toolPanelLayout.addWidget(self.settingBtn)
    self.toolPanelLayout.addWidget(self.resultBtn)
    self.toolPanelLayout.addStretch()

    self.setLayout(self.toolPanelLayout)


  # 开启服务
  def startServiceRender(self):
    self.serviceBtn.setIcon(QIcon(self.iconPath + 'service_close.svg'))
    self.serviceBtn.setText('停止服务')
    self.serviceBtn.setToolTip('停止服务')

  # 停止服务
  def stopServiceRender(self):
    self.serviceBtn.setIcon(QIcon(self.iconPath + 'service_start.svg'))
    self.serviceBtn.setText('开启服务')
    self.serviceBtn.setToolTip('开启服务')

  # 开启/停止服务
  def toggleServiceRender(self):
    mainWindow = getRootWidget(self)
    if mainWindow.detectionFlag:
      return self.showAlertWindow.emit('请暂停检测后再停止服务')
    if not mainWindow.serviceFlag:
      self.startServiceRender()
      self.toggleService.emit(True)
    else:
      self.stopServiceRender()
      self.toggleService.emit(False)
      
  # 开始检测
  def startDetectionRender(self):
    self.startBtn.setIcon(QIcon(self.iconPath + 'pause.svg'))
    self.startBtn.setText('暂停检测')
    self.startBtn.setToolTip('暂停检测')

  # 暂停检测    
  def stopDetectionRender(self):
    self.startBtn.setIcon(QIcon(self.iconPath + 'start.svg'))
    self.startBtn.setText('开始检测')
    self.startBtn.setToolTip('开始检测')

  # 开始/暂停检测
  def toggleDetectionRender(self):
    mainWindow = getRootWidget(self)
    if not mainWindow.serviceFlag:
      return self.showAlertWindow.emit('请开启服务后再开始检测')
    if not mainWindow.detectionFlag:
      self.startDetectionRender()
      self.toggleDetection.emit(True)
    else:
      self.stopDetectionRender()
      self.toggleDetection.emit(False)

  # 设置所有按钮状态：可用/不可用
  def setAllBtnsStatus(self, enable):
    btns = self.findChildren(QToolButton)
    for i in range(0, len(btns)):
      btns[i].setEnabled(enable)

  # 设置某个按钮可用
  def setBtnEnable(self, btnName):
    self.findChild(QToolButton, btnName).setEnabled(True)

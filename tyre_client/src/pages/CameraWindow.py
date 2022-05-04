import sys, os
sys.path.append(os.path.join(__file__, '../../'))

from PyQt5.QtWidgets import QGridLayout, QWidget, QLabel
from PyQt5.QtGui import QColor, QPixmap, QImage
from PyQt5.QtCore import pyqtSignal, QPoint
from layouts.StaticLayout import StaticLayoutWindow
from widgets.SubTitleBar import SubTitleBarWidget
from widgets.CameraShadow import CameraShadowWidget
from tasks.camera import CameraCapture
from common.commlib import loadQss

staticPath = os.path.join(__file__, '../../../') + '/static'


class CameraWindowPage(StaticLayoutWindow):

  showAlertSignal = pyqtSignal(str)

  def __init__(self):

    # 图像尺寸
    self.imgWidth = 1280
    self.imgHeight = 720

    # 阴影设置
    self.shadowX = 0
    self.shadowY = 0
    self.shadowWidth = 40
    self.shadowColor = QColor(168, 168, 168)
    self.menuBarHeight = 48

    # 主窗口尺寸
    self.windowWidth = self.imgWidth + 2 * self.shadowWidth
    self.windowHeight = self.imgHeight + 2 * self.shadowWidth + self.menuBarHeight

    # 样式表
    self.qss = staticPath + '/qss/confirm_window.qss'

    # 窗口标题
    self.windowTitle = '轮胎缺陷监测系统 - 相机调整'

    # 是否停止接收帧
    self.stopReceive = False

    super(CameraWindowPage, self).__init__(False, True, 0, 0, self.windowWidth, 
      self.windowHeight, self.shadowX, self.shadowY, self.shadowWidth, self.shadowColor)

    self.renderWindow()

  def renderWindow(self):
    # 加载样式表
    self.setStyleSheet(loadQss(self.qss))

    # 布局
    self.mainGridLayout = QGridLayout()
    self.mainGridLayout.setContentsMargins(0, 0, 0, 0)

    # 设置周围阴影
    self.mainGridLayout.setContentsMargins(self.shadowWidth, self.shadowWidth, 
      self.shadowWidth, self.shadowWidth)
    self.mainGridLayout.setSpacing(0)

    self.setWindowTitle(self.windowTitle)
    
    # 窗口标题栏
    self.menuBar = SubTitleBarWidget(self.windowTitle, False, False)
    self.menuBar.windowClose.connect(self.closeCamera)
    self.menuBar.windowMove.connect(self.move)
    
    # 主窗口面板
    self.mainPanel = QWidget()
    self.mainPanel.setObjectName('cameraMainPanel')
    self.mainPanelLayout = QGridLayout()
    self.mainPanelLayout.setContentsMargins(0, 0, 0, 0)

    self.imgLabel = QLabel()

    self.shadowWidget = CameraShadowWidget(self.imgWidth, self.imgHeight, self.shadowWidth, self.menuBarHeight)
    self.shadowWidget.setParent(self)
    
    self.mainPanelLayout.addWidget(self.imgLabel)
    self.mainPanel.setLayout(self.mainPanelLayout)
    self.mainGridLayout.addWidget(self.menuBar)
    self.mainGridLayout.addWidget(self.mainPanel)
    self.mainWidget.setLayout(self.mainGridLayout)
  
  # 调用摄像头捕获帧
  def openCamera(self):
    self.stopReceive = False
    self.capture = CameraCapture(self.windowWidth, self.windowHeight)
    self.capture.sendImgSignal.connect(self.displayImage)
    self.capture.start()
    self.show()
  
  def closeCamera(self):
    if self.capture:
      self.stopReceive = True
      self.capture.exitFlag = True
      self.capture.quit()
      self.imgLabel.setPixmap(QPixmap(''))
      self.close()

  # 显示帧
  def displayImage(self, frame, msg):
    if (msg):
      if not self.stopReceive:
        shape = frame.shape
        self.imgLabel.setPixmap(QPixmap.fromImage(QImage(frame.copy().data, shape[1], shape[0], shape[1] * 3, QImage.Format_RGB888)))
    else:
      self.stopReceive = True
      self.showAlertSignal.emit('相机连接已断开，请检查相机连接状态')
      self.closeCamera()

  # 移动窗口
  def move(self, pos):
    super(CameraWindowPage, self).move(pos - QPoint(self.shadowWidth, self.shadowWidth))
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QWidget, QGraphicsDropShadowEffect, QGridLayout
from PyQt5.QtCore import Qt

'''
  不可调整大小，带阴影边框的窗口
'''
class StaticLayoutWindow(QMainWindow):
  
  def __init__(self, isWindowTop, isCenter, windowX, windowY,
      minWindowWidth, minWindowHeight, shadowX, shadowY, shadowWidth, shadowColor):
    super().__init__()
    # 窗口是否位于顶层
    self.isWindowTop = isWindowTop
    # 窗口阴影设置
    self.shadowX = shadowX
    self.shadowY = shadowY
    self.shadowWidth = shadowWidth
    self.shadowColor = shadowColor
    # 窗口最小宽度
    self.minWindowWidth = minWindowWidth
    # 窗口最小高度
    self.minWindowHeight = minWindowHeight
    # 是否居中
    self.isCenter = isCenter
    # 窗口坐标
    self.windowX = windowX
    self.windowY = windowY

    self.render()

  def render(self):

    # 无标题栏窗体
    if self.isWindowTop:
      self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    else:
      self.setWindowFlag(Qt.FramelessWindowHint)

    # 设置窗体背景透明
    self.setAttribute(Qt.WA_TranslucentBackground)
    
    # 设置窗口尺寸
    self.setGeometry(self.windowX, self.windowY, self.minWindowWidth, self.minWindowHeight)
    self.setMinimumSize(self.minWindowWidth, self.minWindowHeight)
    if (self.isCenter):
      self.center()
    
    # 窗口主部件
    self.mainWidget = QWidget()
    self.setCentralWidget(self.mainWidget)

    # 设置窗口阴影
    self.effectShadow = QGraphicsDropShadowEffect(self)
    self.effectShadow.setOffset(self.shadowX, self.shadowY)
    self.effectShadow.setBlurRadius(self.shadowWidth)
    self.effectShadow.setColor(self.shadowColor)
    self.setGraphicsEffect(self.effectShadow)
    self.mainWidget.setGraphicsEffect(self.effectShadow)

    # 光标追踪
    self.setMouseTracking(True)
    self.mainWidget.setMouseTracking(True)

  # 窗口居中
  def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())
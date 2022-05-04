from PyQt5.QtWidgets import QMainWindow, QGraphicsDropShadowEffect, QDesktopWidget, QWidget
from PyQt5.QtCore import Qt

'''
  可调整大小，带阴影边框的窗口
'''

Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)


class FlexiableLayoutWindow(QMainWindow):
  
  def __init__(self, isWindowTop, minWindowWidth, minWindowHeight, shadowX, shadowY, shadowWidth, shadowColor):
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

    # 尺寸调整指针边距
    self.arrowMargin = 5
    # 拖动方向
    self.direction = None
    # 鼠标键是否按下
    self.btnPressed = False

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
    self.setGeometry(0, 0, self.minWindowWidth, self.minWindowHeight)
    self.setMinimumSize(self.minWindowWidth, self.minWindowHeight)
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
  
  # 重写鼠标事件，实现自由改变窗口尺寸
  def mousePressEvent(self, e):
    if e.button() == Qt.LeftButton:
      self.mPos = e.pos()
      self.btnPressed = True

  def mouseReleaseEvent(self, e):
    self.btnPressed = False
    self.direction = None

  def mouseMoveEvent(self, e):
    shadowWidth = self.shadowWidth
    arrowMargin = self.arrowMargin
    pos = e.pos()
    xPos, yPos = pos.x(), pos.y()
    wm, hm = self.width() - shadowWidth, self.height() - shadowWidth
    if self.isMaximized() or self.isFullScreen():
      self.direction = None
      self.setCursor(Qt.ArrowCursor)
      return
    if e.buttons() == Qt.LeftButton and self.btnPressed:
      self.resizeWindow(pos)
      return
    if shadowWidth - arrowMargin <= xPos <= shadowWidth and shadowWidth - arrowMargin <= yPos <= shadowWidth:
      # 左上角
      self.direction = LeftTop
      self.setCursor(Qt.SizeFDiagCursor)
      return
    elif wm <= xPos <= wm + arrowMargin and shadowWidth - arrowMargin <= yPos <= shadowWidth:
      # 右上角
      self.direction = RightTop
      self.setCursor(Qt.SizeBDiagCursor)
      return
    elif shadowWidth - arrowMargin <= xPos <= shadowWidth and hm <= yPos <= hm + arrowMargin:
      # 左下角
      self.direction = LeftBottom
      self.setCursor(Qt.SizeBDiagCursor)
      return
    elif wm <= xPos <= wm + arrowMargin and hm <= yPos <= hm + arrowMargin:
      # 右下角
      self.direction = RightBottom
      self.setCursor(Qt.SizeFDiagCursor)
      return
    elif shadowWidth - arrowMargin <= xPos <= shadowWidth and shadowWidth <= yPos <= hm:
      # 左边
      self.direction = Left
      self.setCursor(Qt.SizeHorCursor)
      return
    elif wm <= xPos <= wm + arrowMargin and shadowWidth <= yPos <= hm:
      # 右边
      self.direction = Right
      self.setCursor(Qt.SizeHorCursor)
      return
    elif shadowWidth <= xPos <= wm and shadowWidth - arrowMargin <= yPos <= shadowWidth:
      # 上边
      self.direction = Top
      self.setCursor(Qt.SizeVerCursor)
      return
    elif shadowWidth <= xPos <= wm and hm <= yPos <= hm + arrowMargin:
      # 下边
      self.direction = Bottom
      self.setCursor(Qt.SizeVerCursor)
      return
    else:
      self.setCursor(Qt.ArrowCursor)

  def resizeWindow(self, pos):
    if self.direction == None:
      return 
    mpos = pos - self.mPos
    xPos, yPos = mpos.x(), mpos.y()
    geometry = self.geometry()
    x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
    if self.direction == LeftTop:
      if w - xPos > self.minimumWidth():
        x += xPos
        w -= xPos
      if h - yPos > self.minimumHeight():
        y += yPos
        h -= yPos
    elif self.direction == RightBottom:
      if w + xPos > self.minimumWidth():
        w += xPos
        self.mPos = pos
      if h + yPos > self.minimumHeight():
        h += yPos
        self.mPos = pos
    elif self.direction == RightTop:
      if h - yPos > self.minimumHeight():
        y += yPos
        h -= yPos
      if w + xPos > self.minimumWidth():
        w += xPos
        self.mPos.setX(pos.x())
    elif self.direction == LeftBottom:
      if w - xPos > self.minimumWidth():
        x += xPos
        w -= xPos
      if h + yPos > self.minimumHeight():
        h += yPos
        self.mPos.setY(pos.y())
    elif self.direction == Left:
      if w - xPos > self.minimumWidth():
        x += xPos
        w -= xPos
      else: 
        return
    elif self.direction == Right:
      if w + xPos > self.minimumWidth():
        w += xPos
        self.mPos = pos
      else:
        return
    elif self.direction == Top:
      if h - yPos > self.minimumHeight():
        y += yPos
        h -= yPos
      else:
        return
    elif self.direction == Bottom:
      if h + yPos > self.minimumHeight():
        h += yPos
        self.mPos = pos
      else:
        return
    self.setGeometry(x, y, w, h)
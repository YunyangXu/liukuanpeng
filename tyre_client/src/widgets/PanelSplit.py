from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


# 面板分割线组件
class PanelSplitWidget(QWidget):
  def __init__(self):
    super().__init__()

    # 分割线宽度
    self.lineWidth = 8
    # 鼠标上一次位置
    self.mPos = None
    # 鼠标是否点击
    self.mPressed = False
    # 父级图像面板最小宽度
    self.minPanelWidth = 360

    self.render()
      
  def render(self):
    self.setAttribute(Qt.WA_StyledBackground, True)
    self.setStyleSheet('background-color: #E8E8E8')
    self.setFixedWidth(self.lineWidth)

    self.setMouseTracking(True)
    self.setCursor(Qt.SizeHorCursor)

  # 重写鼠标事件，实现拖动分割线自由分割面板
  def mousePressEvent(self, e):
    self.mPos = e.globalPos()
    self.mPressed = True

  def mouseMoveEvent(self, e):
    if e.buttons() == Qt.LeftButton and self.mPressed:
      # 父级面板
      parentPanel = self.parentWidget()
      # 父级左侧面板
      pLeftPanel = parentPanel.findChild(QWidget, 'imgLeft')
      # 父级右侧面板
      pRightPanel = parentPanel.findChild(QWidget, 'imgRight')
      pos = e.globalPos() - self.mPos
      deltaWidth = pos.x()
      # 分割线左右移动
      if (deltaWidth < 0 and self.x() > self.minPanelWidth) or (deltaWidth > 0 and parentPanel.width() - self.lineWidth - self.x() > self.minPanelWidth):
        self.setGeometry(self.x() + deltaWidth, self.y(), self.width(), self.height())
        leftWidth = pLeftPanel.width() + deltaWidth
        rightWidth = parentPanel.width() - leftWidth - self.width()
        pLeftPanel.setMinimumWidth(leftWidth)
        pLeftPanel.setGeometry(pLeftPanel.x(), pLeftPanel.y(), leftWidth, pLeftPanel.height())
        pRightPanel.setMinimumWidth(rightWidth)
        pRightPanel.setGeometry(pRightPanel.x() + deltaWidth, pLeftPanel.y(), rightWidth, pLeftPanel.height())
      self.mPos = e.globalPos()

  def mouseReleaseEvent(self, e):
    self.mPos = None
    self.mPressed = False
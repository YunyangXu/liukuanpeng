import sys, os
sys.path.append(os.path.join(__file__, '../../'))

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QPointF, QRectF
from common.commlib import loadQss
import math

staticPath = os.path.join(__file__, '../../../') + '/static'

class CameraShadowWidget(QWidget):
  def __init__(self, width, height, shadowWidth, menuBarHeight):
    super().__init__()

    self.width = width
    self.height = height
    self.shadowWidth = shadowWidth
    self.menuBarHeihgt = menuBarHeight

    # 样式表
    self.qss = staticPath + '/qss/confirm_window.qss'
  
    self.render()

  def render(self):

    self.setAttribute(Qt.WA_StyledBackground, True)
    self.setObjectName('cameraShadowWidget')
    self.setStyleSheet(loadQss(self.qss))

    self.setGeometry(self.shadowWidth, self.shadowWidth + self.menuBarHeihgt, self.width, self.height)

  def paintEvent(self, e):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing, True)
    pen = QPen()
    pen.setStyle(Qt.DashLine)
    pen.setWidth(2)
    pen.setBrush(QColor(255, 255, 255))
    pen.setCapStyle(Qt.SquareCap)
    pen.setJoinStyle(Qt.RoundJoin)
    painter.setPen(pen)

    # 绘制虚线
    pointStart = QPointF(0, math.ceil(self.height / 2))
    pointEnd = QPointF(self.width, math.ceil(self.height / 2))
    painter.drawLine(pointStart, pointEnd)
    pointStart = QPointF(math.ceil(self.width / 2), 0)
    pointEnd = QPointF(math.ceil(self.width / 2), self.height)
    painter.drawLine(pointStart, pointEnd)

    # 绘制矩形
    pen.setStyle(Qt.SolidLine)
    pen.setWidth(1)
    pen.setBrush(QColor(0, 0, 0, 0))
    painter.setPen(pen)
    brush = QBrush()
    brush.setStyle(Qt.SolidPattern)
    brush.setColor(QColor(0, 0, 0, 50))
    painter.setBrush(brush)
    rect = QRectF(30, 30, 280, 60)
    painter.drawRect(rect)
    
    # 绘制文字
    pen.setBrush(QColor(255, 255, 255))
    painter.setPen(pen)
    painter.setFont(QFont('Microsoft YaHei', 12))
    painter.drawText(rect, Qt.AlignCenter, '请将胎冠中线对准白色虚线')

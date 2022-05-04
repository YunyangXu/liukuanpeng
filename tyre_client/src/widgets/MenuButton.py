import sys, os
sys.path.append(os.path.join(__file__, '../../'))

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from common.commlib import loadQss

staticPath = os.path.join(__file__, '../../../') + '/static'


class MenuButtonWidget(QWidget):
  showSubWindow = pyqtSignal(str)

  def __init__(self, width, height, icon, text, type):

    # 按钮尺寸
    self.width = width
    self.height = height

    # 按钮图标
    self.icon = icon

    # 按钮文本
    self.text = text

    # 样式表
    self.qss = staticPath + '/qss/main_menu.qss'

    self.type = type

    super().__init__()
    self.render()


  def render(self):
    # 加载样式表
    self.setStyleSheet(loadQss(self.qss))
    self.setAttribute(Qt.WA_StyledBackground, True)
    self.setProperty('menuBtn', True)
    self.setFixedHeight(self.height)
    self.setCursor(Qt.PointingHandCursor)

    self.layout = QHBoxLayout()
    
    self.iconLabel = QLabel()
    self.iconLabel.setProperty('iconLabel', True)
    ic = QPixmap()
    ic.load(staticPath + '/icons/' + self.icon)
    self.iconLabel.setPixmap(ic.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    self.iconLabel.setFixedWidth(36)

    self.textLabel = QLabel()
    self.textLabel.setProperty('textLabel', True)
    self.textLabel.setText(self.text)

    self.layout.addWidget(self.iconLabel)
    self.layout.addWidget(self.textLabel)

    self.setLayout(self.layout)


  def mousePressEvent(self, e):
    self.showSubWindow.emit(self.type)

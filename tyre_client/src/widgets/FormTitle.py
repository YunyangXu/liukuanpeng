import sys, os
sys.path.append(os.path.join(__file__, '../../'))

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from common.commlib import loadQss

staticPath = os.path.join(__file__, '../../../') + '/static'

class FormTitleWidget(QWidget):
  def __init__(self, titleWidth, title):
    super().__init__()

    self.titleWidth = titleWidth
    self.title = title

    # 样式表
    self.qss = staticPath + '/qss/para_window.qss'
  
    self.render()

  def render(self):
    self.setAttribute(Qt.WA_StyledBackground, True)
    self.setStyleSheet(loadQss(self.qss))
    
    self.setProperty('paraTitle', True)
    self.setFixedWidth(self.titleWidth)
    self.paraTitleLayout = QGridLayout()
    self.paraTitleLayout.setContentsMargins(0, 10, 0, 10)
    self.paraTitleLabel = QLabel(self.title)
    self.paraTitleLabel.setProperty('paraTitleLabel', True)
    self.paraTitleLabel.setAlignment(Qt.AlignCenter)
    self.paraTitleLayout.addWidget(self.paraTitleLabel)
    self.setLayout(self.paraTitleLayout)
import os, sys
sys.path.append(os.path.join(__file__, '../../'))
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from widgets.ImagePanel import ImagePanelWidget
from widgets.InfoPanel import InfoPanelWidget
from common.commlib import loadQss

staticPath = os.path.join(__file__, '../../../') + '/static'


class RightPanelWidget(QWidget):
  def __init__(self):
    super().__init__()

    # 页脚高度
    self.footerHeight = 32

    # 样式表
    self.qss = staticPath + '/qss/right_panel.qss'

    self.render()
      
  def render(self):
    self.setAttribute(Qt.WA_StyledBackground, True)
    self.setStyleSheet(loadQss(self.qss))

    # 布局
    self.rightPanelLayout = QGridLayout()
    self.rightPanelLayout.setContentsMargins(0, 0, 0, 0)
    self.rightPanelLayout.setSpacing(0)
    
    # 图片面板
    self.imgPanel = ImagePanelWidget()

    # 信息面板
    self.infoPanel = InfoPanelWidget()
    self.infoPanel.setMaximumHeight(240)

    # 页脚
    self.footerWidget = QWidget()
    self.footerWidget.setFixedHeight(self.footerHeight)
    self.footerWidget.setObjectName('footer')
    self.footerLayout = QGridLayout()
    self.footerLayout.setContentsMargins(0, 0, 0, 0)
    self.footerLabel = QLabel()
    self.footerLabel.setObjectName('footerLabel')
    self.footerLabel.setText('版权所有 XXXXXXXX')
    self.footerLabel.setFont(QFont('Microsoft YaHei'))
    self.footerLabel.setAlignment(Qt.AlignCenter)
    self.footerLayout.addWidget(self.footerLabel)
    self.footerWidget.setLayout(self.footerLayout)
    
    self.rightPanelLayout.addWidget(self.imgPanel)
    self.rightPanelLayout.addWidget(self.infoPanel)
    self.rightPanelLayout.addWidget(self.footerWidget)
    self.setLayout(self.rightPanelLayout)
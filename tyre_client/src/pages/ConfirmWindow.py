import sys, os
sys.path.append(os.path.join(__file__, '../../'))

from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from layouts.StaticLayout import StaticLayoutWindow
from widgets.SubTitleBar import SubTitleBarWidget
from common.commlib import loadQss

staticPath = os.path.join(__file__, '../../../') + '/static'


class ConfirmWindowPage(StaticLayoutWindow):
  # 点击确认按钮向主窗口发送的信号
  confirmSignal = pyqtSignal()

  def __init__(self):

    # 主窗口尺寸
    self.windowWidth = 640
    self.windowHeight = 320

    # 阴影设置
    self.shadowX = 0
    self.shadowY = 0
    self.shadowWidth = 40
    self.shadowColor = QColor(168, 168, 168)
    # 样式表
    self.qss = staticPath + '/qss/confirm_window.qss'

    super(ConfirmWindowPage, self).__init__(False, True, 0, 0, self.windowWidth, 
      self.windowHeight, self.shadowX, self.shadowY, self.shadowWidth, self.shadowColor)

    self.renderWindow()

  def renderWindow(self):
    # 加载样式表
    self.setStyleSheet(loadQss(self.qss))

    # 布局
    self.mainGridLayout = QGridLayout()

    # 设置周围阴影
    self.mainGridLayout.setContentsMargins(self.shadowWidth, self.shadowWidth, 
      self.shadowWidth, self.shadowWidth)
    self.mainGridLayout.setSpacing(0)
    
    # 窗口标题栏
    self.menuBar = SubTitleBarWidget('提示信息', False, False)
    self.menuBar.windowClose.connect(self.closeWindow)
    
    # 主窗口面板
    self.mainPanel = QWidget()
    self.mainPanel.setObjectName('subWindowPanel')

    self.mainPanelLayout = QGridLayout()
    self.topSection = QWidget()
    self.topSectionLayout = QGridLayout()
    self.alertIcon = QLabel()
    icon = QPixmap()
    icon.load(staticPath + '/icons/confirm.png')
    self.alertIcon.setPixmap(icon.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    self.alertIcon.setFixedWidth(60)
    self.messageLabel = QLabel()
    self.messageLabel.setObjectName('messageLabel')
    self.messageLabel.setWordWrap(True)
    self.topSectionLayout.addWidget(self.alertIcon, 0, 0)
    self.topSectionLayout.addWidget(self.messageLabel, 0, 1)
    self.topSection.setLayout(self.topSectionLayout)

    self.bottomSection = QWidget()
    self.bottomSection.setFixedHeight(60)
    self.bottomSectionLayout = QHBoxLayout()
    self.confirmBtn = QPushButton('确定')
    self.confirmBtn.setObjectName('confirmBtn')
    self.confirmBtn.setCursor(Qt.PointingHandCursor)
    self.confirmBtn.clicked.connect(self.confirm)

    self.cancelBtn = QPushButton('取消')
    self.cancelBtn.setObjectName('cancelBtn')
    self.cancelBtn.setCursor(Qt.PointingHandCursor)
    self.cancelBtn.clicked.connect(self.closeWindow)
  
    self.bottomSectionLayout.addStretch()
    self.bottomSectionLayout.addWidget(self.confirmBtn)
    self.bottomSectionLayout.addWidget(self.cancelBtn)

    self.bottomSection.setLayout(self.bottomSectionLayout)

    self.mainPanelLayout.addWidget(self.topSection)
    self.mainPanelLayout.addWidget(self.bottomSection)
    self.mainPanel.setLayout(self.mainPanelLayout)
    
    self.mainGridLayout.addWidget(self.menuBar)
    self.mainGridLayout.addWidget(self.mainPanel)
    self.mainWidget.setLayout(self.mainGridLayout)

  def setMessage(self, msg):
    self.messageLabel.setText(msg)

  def confirm(self):
    self.confirmSignal.emit()

  # 关闭窗口
  def closeWindow(self):
    self.close()
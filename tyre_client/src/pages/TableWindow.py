import sys, os
sys.path.append(os.path.join(__file__, '../../'))

from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, \
  QScrollArea, QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton
from PyQt5.QtGui import QColor, QEnterEvent
from PyQt5.QtCore import Qt, QPoint
from layouts.FlexiableLayout import FlexiableLayoutWindow
from widgets.SubTitleBar import SubTitleBarWidget
from widgets.TablePanel import TablePanelWidget
from common.commlib import loadQss

staticPath = os.path.join(__file__, '../../../') + '/static'


class TableWindowPage(FlexiableLayoutWindow):
  def __init__(self):

    # 窗口尺寸
    self.windowWidth = 1520
    self.windowHeight = 900

    # 阴影设置
    self.shadowX = 0
    self.shadowY = 0
    self.shadowWidth = 60
    self.shadowColor = QColor(132, 132, 132)

    # 样式表
    self.qss = staticPath + '/qss/para_window.qss'

    # 窗口标题
    self.windowTitle = '轮胎缺陷监测系统 - 检测结果分析'

    super(TableWindowPage, self).__init__(False, self.windowWidth, 
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

    self.setWindowTitle(self.windowTitle)
    
    # 窗口标题栏
    self.menuBar = SubTitleBarWidget(self.windowTitle, True, True)
    self.menuBar.windowMove.connect(self.move)
    self.menuBar.windowFullScreen.connect(self.changeWindowSize)
    self.menuBar.windowClose.connect(self.closeWindow)
    self.menuBar.installEventFilter(self)

    # 窗口面板
    self.mainPanel = QWidget()
    self.mainPanel.setObjectName('tablePanel')
    self.mainPanel.installEventFilter(self)
    self.mainPanelLayout = QGridLayout()
    self.mainPanelLayout.setContentsMargins(0, 0, 0, 0)

    self.tabPanel = QTabWidget()

    self.searchPanel1 = TablePanelWidget()
    self.searchPanel2 = QWidget()
    self.searchPanel3 = QWidget()

    self.tabPanel.addTab(self.searchPanel1, '缺陷检测报告')
    self.tabPanel.addTab(self.searchPanel2, '缺陷检测结果')
    self.tabPanel.addTab(self.searchPanel3, '内外侧检测结果')

    self.mainPanelLayout.addWidget(self.tabPanel)
    self.mainPanel.setLayout(self.mainPanelLayout)

    self.mainGridLayout.addWidget(self.menuBar)
    self.mainGridLayout.addWidget(self.mainPanel)
    self.mainWidget.setLayout(self.mainGridLayout)

  # 最小化、最大化/还原窗口
  def changeWindowSize(self, msg):
    if msg == 'min':
      self.showMinimized()
    else:
      if (self.isFullScreen()):
        self.mainGridLayout.setContentsMargins(self.shadowWidth, self.shadowWidth, 
          self.shadowWidth, self.shadowWidth)
        self.showNormal()
      else:
        self.mainGridLayout.setContentsMargins(0, 0, 0, 0)
        self.showFullScreen()

  # 关闭窗口
  def closeWindow(self):
    self.close()
  
  # 移动窗口
  def move(self, pos):
    if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
      return
    super(TableWindowPage, self).move(pos - QPoint(self.shadowWidth, self.shadowWidth))

  def eventFilter(self, obj, e):
    if isinstance(e, QEnterEvent):
      self.setCursor(Qt.ArrowCursor)
    return super(TableWindowPage, self).eventFilter(obj, e)
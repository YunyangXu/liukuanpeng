import sys, os
sys.path.append(os.path.join(__file__, '../../'))

from PyQt5.QtWidgets import QGridLayout, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from layouts.StaticLayout import StaticLayoutWindow
from widgets.MenuButton import MenuButtonWidget
from common.commlib import loadQss

staticPath = os.path.join(__file__, '../../../') + '/static'


class MainMenuWidget(StaticLayoutWindow):

  togglePanelSignal = pyqtSignal(str)
  showExitWindowSignal = pyqtSignal()

  def __init__(self):

    # 主窗口尺寸
    self.windowWidth = 300
    self.windowHeight = 260

    # 阴影设置
    self.shadowX = 0
    self.shadowY = 0
    self.shadowWidth = 20
    self.shadowColor = QColor(168, 168, 168)

    # 样式表
    self.qss = staticPath + '/qss/main_menu.qss'

    self.toolPanelShow = True
    self.checkPanelShow = True
    self.statusPanelShow = True

    super(MainMenuWidget, self).__init__(True, False, 0, 0, self.windowWidth, 
      self.windowHeight, self.shadowX, self.shadowY, self.shadowWidth, self.shadowColor)

    self.renderWindow()

  def renderWindow(self):
    # 加载样式表
    self.setStyleSheet(loadQss(self.qss))

    # 布局
    self.mainLayout = QGridLayout()

    # 设置周围阴影
    self.mainLayout.setContentsMargins(self.shadowWidth, self.shadowWidth, 
      self.shadowWidth, self.shadowWidth)
    self.mainLayout.setSpacing(0)
    
    # 菜单面板
    self.menuPanel = QWidget()
    self.menuPanel.setObjectName('menuPanel')
    
    self.menuPanelLayout = QGridLayout()
    self.menuPanelLayout.setContentsMargins(0, 0, 0, 0)

    self.menuTopPanel = QWidget()
    self.menuTopPanelLayout = QGridLayout()
    self.menuTopPanelLayout.setContentsMargins(16, 16, 16, 16)
    self.menuTopPanelLayout.setSpacing(16)
    
    self.btnOpenIcon = QIcon(staticPath + '/icons/btn_open.png')
    self.btnCloseIcon = QIcon(staticPath + '/icons/btn_close.png')

    self.toolPanelShowLabel = QLabel('显示工具面板')
    self.toolPanelShowLabel.setProperty('panelShowLabel', True)
    self.toolPanelShowBtn = QPushButton()
    self.toolPanelShowBtn.setProperty('panelShowBtn', True)
    self.toolPanelShowBtn.setFixedSize(32, 24)
    self.toolPanelShowBtn.setIcon(self.btnOpenIcon)
    self.toolPanelShowBtn.setIconSize(QSize(32, 32))
    self.toolPanelShowBtn.setCursor(Qt.PointingHandCursor)
    self.toolPanelShowBtn.clicked.connect(lambda: self.togglePanel('toolPanel'))

    self.checkPanelShowLabel = QLabel('显示检测面板')
    self.checkPanelShowLabel.setProperty('panelShowLabel', True)
    self.checkPanelShowBtn = QPushButton()
    self.checkPanelShowBtn.setProperty('panelShowBtn', True)
    self.checkPanelShowBtn.setFixedSize(32, 24)
    self.checkPanelShowBtn.setIcon(self.btnOpenIcon)
    self.checkPanelShowBtn.setIconSize(QSize(32, 32))
    self.checkPanelShowBtn.setCursor(Qt.PointingHandCursor)
    self.checkPanelShowBtn.clicked.connect(lambda: self.togglePanel('infoPanelLeft'))

    self.statusPanelShowLabel = QLabel('显示状态面板')
    self.statusPanelShowLabel.setProperty('panelShowLabel', True)
    self.statusPanelShowBtn = QPushButton()
    self.statusPanelShowBtn.setProperty('panelShowBtn', True)
    self.statusPanelShowBtn.setFixedSize(32, 24)
    self.statusPanelShowBtn.setIcon(self.btnOpenIcon)
    self.statusPanelShowBtn.setIconSize(QSize(32, 32))
    self.statusPanelShowBtn.setCursor(Qt.PointingHandCursor)
    self.statusPanelShowBtn.clicked.connect(lambda: self.togglePanel('infoPanelRight'))

    self.menuTopPanelLayout.addWidget(self.toolPanelShowLabel, 0, 0)
    self.menuTopPanelLayout.addWidget(self.toolPanelShowBtn, 0, 1)
    self.menuTopPanelLayout.addWidget(self.checkPanelShowLabel, 1, 0)
    self.menuTopPanelLayout.addWidget(self.checkPanelShowBtn, 1, 1)
    self.menuTopPanelLayout.addWidget(self.statusPanelShowLabel, 2, 0)
    self.menuTopPanelLayout.addWidget(self.statusPanelShowBtn, 2, 1)
    self.menuTopPanel.setLayout(self.menuTopPanelLayout)
    
    self.panelSplit = QWidget()
    self.panelSplit.setObjectName('panelSplit')
    self.panelSplit.setFixedHeight(1)

    self.menuBottomPanel = QWidget()
    self.menuBottomPanelLayout = QGridLayout()
    self.menuBottomPanelLayout.setContentsMargins(0, 0, 0, 0)
    self.menuBottomPanelLayout.setSpacing(0)
    self.menuBottomPanelLayout.setAlignment(Qt.AlignTop)

    self.exitBtn = MenuButtonWidget(self.width, 48, 'exit.png', '退出系统', 'exit')
    self.exitBtn.showSubWindow.connect(self.showSubWindow)
    
    self.menuBottomPanelLayout.addWidget(self.exitBtn)
    self.menuBottomPanel.setLayout(self.menuBottomPanelLayout)

    self.menuPanelLayout.addWidget(self.menuTopPanel)
    self.menuPanelLayout.addWidget(self.panelSplit)
    self.menuPanelLayout.addWidget(self.menuBottomPanel)

    self.menuPanel.setLayout(self.menuPanelLayout)
    self.mainLayout.addWidget(self.menuPanel)
    self.mainWidget.setLayout(self.mainLayout)

  def showSubWindow(self, msg):
    if msg == 'exit':
      self.showExitWindowSignal.emit()
    self.closeMenu()

  # 显示/隐藏面板
  def togglePanel(self, type):
    if type == 'toolPanel':
      self.toolPanelShowBtn.setIcon(self.btnCloseIcon if self.toolPanelShow else self.btnOpenIcon)
      self.toolPanelShow = not self.toolPanelShow
    elif type == 'infoPanelLeft':
      self.checkPanelShowBtn.setIcon(self.btnCloseIcon if self.checkPanelShow else self.btnOpenIcon)
      self.checkPanelShow = not self.checkPanelShow
    else:
      self.statusPanelShowBtn.setIcon(self.btnCloseIcon if self.statusPanelShow else self.btnOpenIcon)
      self.statusPanelShow = not self.statusPanelShow
    self.togglePanelSignal.emit(type)

  # 隐藏菜单
  def closeMenu(self):
    self.close()
  
  # 计算绘制位置
  def setPosition(self):
    mainWindow = self.parentWidget()
    width = mainWindow.width()
    shadowWidth = mainWindow.getShadowWidth()
    menuBarHeight = mainWindow.getMenuBarHeight()
    if (mainWindow.isFullScreen()):
      self.setGeometry(width - self.windowWidth, menuBarHeight - self.shadowWidth, self.windowWidth, self.windowHeight)
    else:
      self.setGeometry(width - self.windowWidth - shadowWidth, 
        shadowWidth + menuBarHeight - self.shadowWidth, self.windowWidth, self.windowHeight)

  def paintEvent(self, e):
    self.setPosition()
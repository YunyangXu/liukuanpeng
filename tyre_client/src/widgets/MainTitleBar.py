import sys, os
from xmlrpc.client import boolean
sys.path.append(os.path.join(__file__, '../../'))

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QToolButton
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPoint
from common.commlib import loadQss

staticPath = os.path.join(__file__, '../../../') + '/static'

'''
  主窗口标题栏
'''
class MainTitleBarWidget(QWidget):

  # 窗口移动信号
  windowMove = pyqtSignal(QPoint)
  # 窗口全屏信号
  windowFullScreen = pyqtSignal(str)
  # 显示子窗口信号
  showSubWindow = pyqtSignal()
  # 显示主菜单信号
  showMainMenu = pyqtSignal(boolean)

  def __init__(self, title):
    super().__init__()
    
    # 鼠标指针位置
    self.mousePos = None
    # 最大高度
    self.maxHeight = 60
    # 左侧图标
    self.icon = staticPath + '/icons/tyre.svg'
    # 菜单图标
    self.menuIcon = staticPath + '/icons/menu.svg'
    # 最小化图标
    self.minIcon = staticPath + '/icons/min.svg'
    # 最大化图标
    self.maxIcon = staticPath + '/icons/max.svg'
    # 还原图标
    self.normalIcon = staticPath + '/icons/normal.svg'
    # 关闭图标
    self.closeIcon = staticPath + '/icons/close.svg'
    # 左侧图标大小
    self.leftIconSize = 32
    # 右侧图标大小
    self.rightIconSize = 20
    # 标题
    self.title = title
    # 标题文字大小
    self.titleSize = 14
    # 标题字体
    fontId = QFontDatabase.addApplicationFont(staticPath + '/fonts/华文中宋.ttf')
    self.titleFont = QFont(QFontDatabase.applicationFontFamilies(fontId)[0], self.titleSize)
    # 样式表
    self.qss = staticPath + '/qss/main_title_bar.qss'

    self.render()

  def render(self):
    # 加载样式表
    self.setAttribute(Qt.WA_StyledBackground, True)
    self.setStyleSheet(loadQss(self.qss))

    # 布局
    self.layout = QHBoxLayout()
    self.layout.setContentsMargins(0, 0, 0, 0)
    self.layout.setSpacing(0)

    # 设置左侧图标
    self.leftIcon = QToolButton()
    self.leftIcon.setObjectName('titleLeftIcon')
    self.leftIcon.setIcon(QIcon(self.icon))
    self.leftIcon.setIconSize(QSize(self.leftIconSize, self.leftIconSize))
    self.layout.addWidget(self.leftIcon)

    # 设置标题
    self.title = QLabel(self.title)
    self.title.setObjectName('titleLeftLabel')
    self.title.setFont(QFont(self.titleFont))
    self.layout.addWidget(self.title)

    # 右侧菜单，最小化，最大化，关闭按钮
    self.menuBtn = QToolButton()
    self.menuBtn.setObjectName('menuBtn')
    self.menuBtn.setIcon(QIcon(self.menuIcon))
    self.menuBtn.setIconSize(QSize(self.rightIconSize, self.rightIconSize))
    self.menuBtn.setCursor(Qt.PointingHandCursor)
    self.menuBtn.setToolTip('主菜单')
    self.layout.addWidget(self.menuBtn)

    self.minBtn = QToolButton()
    self.minBtn.setObjectName('minBtn')
    self.minBtn.setIcon(QIcon(self.minIcon))
    self.minBtn.setIconSize(QSize(self.rightIconSize, self.rightIconSize))
    self.minBtn.setCursor(Qt.PointingHandCursor)
    self.minBtn.setToolTip('最小化')
    self.layout.addWidget(self.minBtn)

    self.maxBtn = QToolButton()
    self.maxBtn.setObjectName('maxBtn')
    self.maxBtn.setIcon(QIcon(self.maxIcon))
    self.maxBtn.setIconSize(QSize(self.rightIconSize, self.rightIconSize))
    self.maxBtn.setCursor(Qt.PointingHandCursor)
    self.maxBtn.setToolTip('最大化')
    self.layout.addWidget(self.maxBtn)

    self.closeBtn = QToolButton()
    self.closeBtn.setObjectName('closeBtn')
    self.closeBtn.setIcon(QIcon(self.closeIcon))
    self.closeBtn.setIconSize(QSize(self.rightIconSize, self.rightIconSize))
    self.closeBtn.setCursor(Qt.PointingHandCursor)
    self.closeBtn.setToolTip('关闭')

    self.menuBtn.clicked.connect(self.showMenu)
    # 点击按钮最小化窗口
    self.minBtn.clicked.connect(lambda: self.changeWindowSize('min'))
    # 点击按钮最大化/还原窗口
    self.maxBtn.clicked.connect(lambda: self.changeWindowSize('max'))
    
    # 点击按钮关闭主窗口
    self.closeBtn.clicked.connect(self.closeWindow)
    self.layout.addWidget(self.closeBtn)

    # 设置最大最小高度
    self.setMinimumHeight(self.maxHeight)
    self.setMaximumHeight(self.maxHeight)
    self.setLayout(self.layout)

    self.setMouseTracking(True)

  # 显示主菜单
  def showMenu(self):
    self.showMainMenu.emit(True)
  
  # 最小化和最大化窗口
  def changeWindowSize(self, type):
    self.showMainMenu.emit(False)
    if self.maxBtn.toolTip() == '最大化' and type != 'min':
      self.maxBtn.setIcon(QIcon(self.normalIcon))
      self.maxBtn.setToolTip('还原')
    elif type != 'min':
      self.maxBtn.setIcon(QIcon(self.maxIcon))
      self.maxBtn.setToolTip('最大化')
    self.windowFullScreen.emit(type)

  # 关闭窗口
  def closeWindow(self):
    self.showMainMenu.emit(False)
    self.showSubWindow.emit()
    
  # 重写鼠标事件，实现自由拖拽窗口
  def mousePressEvent(self, e):
    if e.button() == Qt.LeftButton:
      self.mousePos = e.pos()
    e.accept()

  def mouseReleaseEvent(self, e):
    self.mousePos = None
    e.accept()

  def mouseMoveEvent(self, e):
    if e.buttons() == Qt.LeftButton and self.mousePos:
      self.windowMove.emit(self.mapToGlobal(e.pos() - self.mousePos))
    e.accept()
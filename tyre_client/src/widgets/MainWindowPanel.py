import sys, os
sys.path.append(os.path.join(__file__, '../../'))
from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal
from widgets.ToolPanel import ToolPanelWidget
from widgets.RightPanel import RightPanelWidget


class MainWindowPanelWidget(QWidget):
  
  showSubWindow = pyqtSignal()
  showNetworkWindow = pyqtSignal()
  showParaWindow = pyqtSignal()
  showTableWindow = pyqtSignal()
  showAlertWindow = pyqtSignal(str)
  toggleService = pyqtSignal(bool)
  toggleDetection = pyqtSignal(bool)

  def __init__(self):
    super().__init__()
    self.render()


  def render(self):
    self.setMouseTracking(True)
    self.setAttribute(Qt.WA_StyledBackground, True)

    # 布局
    self.mainPanelLayout = QGridLayout()
    self.mainPanelLayout.setContentsMargins(0, 0, 0, 0)
    self.mainPanelLayout.setSpacing(0)

    # 左侧工具栏
    self.toolPanelWidget = ToolPanelWidget()
    self.toolPanelWidget.setObjectName('toolPanel')
    self.toolPanelWidget.showSubWindow.connect(self.showSubWindow)
    self.toolPanelWidget.showNetworkWindow.connect(self.showNetworkWindow)
    self.toolPanelWidget.showParaWindow.connect(self.showParaWindow)
    self.toolPanelWidget.showTableWindow.connect(self.showTableWindow)
    self.toolPanelWidget.showAlertWindow.connect(self.showAlertWindow)
    self.toolPanelWidget.toggleService.connect(self.toggleService)
    self.toolPanelWidget.toggleDetection.connect(self.toggleDetection)

    # 右侧功能面板
    self.rightPanelWidget = RightPanelWidget()

    self.mainPanelLayout.addWidget(self.toolPanelWidget, 0, 0)
    self.mainPanelLayout.addWidget(self.rightPanelWidget, 0, 1)
    self.setLayout(self.mainPanelLayout)
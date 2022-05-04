import os, sys
sys.path.append(os.path.join(__file__, '../../'))

from datetime import datetime
import math
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtGui import QFont, QColor, QPixmap, QMovie
from PyQt5.QtCore import Qt, QTimer
from common.commlib import loadQss, renderShadow, getRootWidget

staticPath = os.path.join(__file__, '../../../') + '/static'

class InfoPanelWidget(QWidget):
  def __init__(self):
    super().__init__()

    self.panelTitleHeight = 40

    # 样式表
    self.qss = staticPath + '/qss/info_panel.qss'

    self.render()
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.accumulateTime)
    self.timer.start(1000)

      
  def render(self):
    self.setAttribute(Qt.WA_StyledBackground, True)
    self.setStyleSheet(loadQss(self.qss))

    self.infoPanelLayout = QHBoxLayout()
    self.infoPanelLayout.setContentsMargins(12, 6, 12, 12)
    self.infoPanelLayout.setSpacing(12)
    self.infoPanelLeft = QWidget()
    self.infoPanelLeft.setObjectName('infoPanelLeft')
    self.infoPanelLeftLayout = QGridLayout()
    self.infoPanelLeftLayout.setContentsMargins(0, 0, 0, 0)
    self.infoPanelLeftLayout.setSpacing(0)

    self.panelLeftTitle = QWidget()
    self.panelLeftTitle.setObjectName('panelLeftTitle')
    self.panelLeftTitle.setFixedHeight(self.panelTitleHeight)
    self.panelLeftTitleLayout = QHBoxLayout()
    self.panelLeftTitleIcon = QLabel()
    self.panelLeftTitleIcon.setObjectName('panelLeftTitleIcon')
    self.panelLeftTitleIcon.setFixedWidth(24)
    icon = QPixmap()
    icon.load(staticPath + '/icons/search.svg')
    self.panelLeftTitleIcon.setPixmap(icon.scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    self.panelLeftTitleText = QLabel()
    self.panelLeftTitleText.setObjectName('panelLeftTitleText')
    self.panelLeftTitleText.setText('检测信息')
    self.panelLeftTitleText.setFont(QFont('Microsoft YaHei'))
    self.panelLeftTitleLayout.addWidget(self.panelLeftTitleIcon)
    self.panelLeftTitleLayout.addWidget(self.panelLeftTitleText)
    self.panelLeftTitle.setLayout(self.panelLeftTitleLayout)

    self.panelLeftBody = QWidget()
    self.panelLeftBodyLayout = QVBoxLayout()
    self.panelLeftBodyLayout.setContentsMargins(0, 0, 0, 0)
    self.panelLeftBodyContent = QWidget()
    self.panelLeftBodyContent.setObjectName('panelLeftBodyContent')
    self.panelLeftBodyContentLayout = QVBoxLayout()
    self.panelLeftBodyContentLayout.setContentsMargins(10, 10, 10, 10)
    self.panelLeftBodyContentLayout.setAlignment(Qt.AlignTop)

    self.checkingList = QWidget()
    self.checkingListLayout = QHBoxLayout()
    self.checkingListLayout.setAlignment(Qt.AlignLeft)
    self.checkingListLayout.setContentsMargins(0, 0, 0, 0)
    self.productionLineLabel = QLabel()
    self.productionLineLabel.setObjectName('productionLineLabel')
    self.productionLineLabel.hide()
    self.checkingIcon = QLabel()
    self.checkingIcon.setObjectName('checkingIcon')
    self.gifIcon = QMovie(staticPath + '/icons/check_loading.gif')
    self.checkingIcon.setMovie(self.gifIcon)
    self.gifIcon.start()
    self.checkingIcon.hide()
    self.checkingLabel = QLabel()
    self.checkingLabel.setObjectName('checkingLabel')
    self.checkingLabel.setText('正在检测')
    self.checkingLabel.hide()
    self.checkingListLayout.addWidget(self.productionLineLabel)
    self.checkingListLayout.addWidget(self.checkingIcon)
    self.checkingListLayout.addWidget(self.checkingLabel)
    self.checkingList.setLayout(self.checkingListLayout)
    self.checkingList.setFixedHeight(24)

    self.resultList = QWidget()
    self.resultListLayout = QHBoxLayout()
    self.resultListLayout.setAlignment(Qt.AlignLeft)
    self.resultListLayout.setContentsMargins(0, 0, 0, 0)
    self.resultLabel = QLabel()
    self.resultLabel.setObjectName('resultLabel')
    self.resultListLayout.addWidget(self.resultLabel)
    self.resultList.setLayout(self.resultListLayout)
    self.resultList.setFixedHeight(24)

    self.errorLabel = QLabel()
    self.errorLabel.setObjectName('errorLabel')
    self.errorLabel.setProperty('errMessage', True)
    self.errorLabel.setWordWrap(True)
    self.errorLabel.setFixedWidth(600)

    self.panelLeftBodyContentLayout.addWidget(self.checkingList)
    self.panelLeftBodyContentLayout.addWidget(self.resultList)
    self.panelLeftBodyContentLayout.addWidget(self.errorLabel)
    self.panelLeftBodyContentLayout.setSpacing(6)

    self.panelLeftBodyContent.setLayout(self.panelLeftBodyContentLayout)
            
    self.panelLeftBodyScroll = QScrollArea()
    self.panelLeftBodyScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    self.panelLeftBodyScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.panelLeftBodyScroll.setWidget(self.panelLeftBodyContent)
    self.panelLeftBodyLayout.addWidget(self.panelLeftBodyScroll)
    self.panelLeftBody.setLayout(self.panelLeftBodyLayout)
    
    self.infoPanelLeftLayout.addWidget(self.panelLeftTitle)
    self.infoPanelLeftLayout.addWidget(self.panelLeftBody)
    self.infoPanelLeft.setLayout(self.infoPanelLeftLayout)

    self.infoPanelRight = QWidget()
    self.infoPanelRight.setObjectName('infoPanelRight')
    self.infoPanelRightLayout = QGridLayout()
    self.infoPanelRightLayout.setContentsMargins(0, 0, 0, 0)
    self.infoPanelRightLayout.setSpacing(0)
    self.panelRightTitle = QWidget()
    self.panelRightTitle.setObjectName('panelRightTitle')
    self.panelRightTitle.setFixedHeight(self.panelTitleHeight)
    self.panelRightTitleLayout = QHBoxLayout()
    self.panelRightTitleIcon = QLabel()
    self.panelRightTitleIcon.setObjectName('panelRightTitleIcon')
    self.panelRightTitleIcon.setFixedWidth(24)
    icon = QPixmap()
    icon.load(staticPath + '/icons/status.png')
    self.panelRightTitleIcon.setPixmap(icon.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    self.panelRightTitleText = QLabel()
    self.panelRightTitleText.setObjectName('panelRightTitleText')
    self.panelRightTitleText.setText('状态信息')
    self.panelRightTitleText.setFont(QFont('Microsoft YaHei'))
    self.panelRightTitleLayout.addWidget(self.panelRightTitleIcon)
    self.panelRightTitleLayout.addWidget(self.panelRightTitleText)
    self.panelRightTitle.setLayout(self.panelRightTitleLayout)

    self.panelRightBody = QWidget()
    self.panelRightBodyLayout = QVBoxLayout()
    self.panelRightBodyLayout.setContentsMargins(0, 0, 0, 0)
    self.panelRightBodyContent = QWidget()
    self.panelRightBodyContent.setObjectName('panelRightBodyContent')
    self.panelRightBodyContentLayout = QVBoxLayout()
    self.panelRightBodyContentLayout.setContentsMargins(10, 10, 10, 10)
    self.panelRightBodyContentLayout.setAlignment(Qt.AlignTop)

    self.time1Label = QLabel()
    self.time1Label.setObjectName('time1Label')
    self.time1Label.setFixedHeight(20)

    self.time2Label = QLabel()
    self.time2Label.setObjectName('time2Label')
    self.time2Label.setFixedHeight(20)

    self.cameraList = QWidget()
    self.cameraListLayout = QHBoxLayout()
    self.cameraListLayout.setAlignment(Qt.AlignLeft)
    self.cameraListLayout.setContentsMargins(0, 0, 0, 0)
    self.cameraLabel = QLabel()
    self.cameraLabel.setObjectName('cameraLabel')
    self.cameraLabel.setText('相机连接状态:')
    self.cameraLabel.setFixedWidth(140)
    self.cameraStatusLabel = QLabel()
    self.cameraStatusLabel.setObjectName('cameraStatusLabel')
    self.cameraStatusLabel.setProperty('statusLabel', 'disconnected')
    self.cameraStatusLabel.setText('已断开')
    self.cameraListLayout.addWidget(self.cameraLabel)
    self.cameraListLayout.addWidget(self.cameraStatusLabel)
    self.cameraList.setLayout(self.cameraListLayout)
    self.cameraList.setFixedHeight(20)

    self.xrayList = QWidget()
    self.xrayListLayout = QHBoxLayout()
    self.xrayListLayout.setAlignment(Qt.AlignLeft)
    self.xrayListLayout.setContentsMargins(0, 0, 0, 0)
    self.xrayLabel = QLabel()
    self.xrayLabel.setObjectName('xrayLabel')
    self.xrayLabel.setText('X光机连接状态:')
    self.xrayLabel.setFixedWidth(140)
    self.xrayStatusLabel = QLabel()
    self.xrayStatusLabel.setObjectName('xrayStatusLabel')
    self.xrayStatusLabel.setProperty('statusLabel', 'disconnected')
    self.xrayStatusLabel.setText('已断开')
    self.xrayListLayout.addWidget(self.xrayLabel)
    self.xrayListLayout.addWidget(self.xrayStatusLabel)
    self.xrayList.setLayout(self.xrayListLayout)
    self.xrayList.setFixedHeight(20)

    self.serverList = QWidget()
    self.serverListLayout = QHBoxLayout()
    self.serverListLayout.setAlignment(Qt.AlignLeft)
    self.serverListLayout.setContentsMargins(0, 0, 0, 0)
    self.serverLabel = QLabel()
    self.serverLabel.setObjectName('serverLabel')
    self.serverLabel.setText('服务器连接状态:')
    self.serverLabel.setFixedWidth(140)
    self.serverStatusLabel = QLabel()
    self.serverStatusLabel.setObjectName('serverStatusLabel')
    self.serverStatusLabel.setProperty('statusLabel', 'disconnected')
    self.serverStatusLabel.setText('已断开')
    self.serverListLayout.addWidget(self.serverLabel)
    self.serverListLayout.addWidget(self.serverStatusLabel)
    self.serverList.setLayout(self.serverListLayout)
    self.serverList.setFixedHeight(20)

    self.alertList = QWidget()
    self.alertListLayout = QHBoxLayout()
    self.alertListLayout.setAlignment(Qt.AlignLeft)
    self.alertListLayout.setContentsMargins(0, 0, 0, 0)
    self.alertLabel = QLabel()
    self.alertLabel.setObjectName('alertLabel')
    self.alertLabel.setText('警报装置连接状态:')
    self.alertLabel.setFixedWidth(140)
    self.alertStatusLabel = QLabel()
    self.alertStatusLabel.setObjectName('alertStatusLabel')
    self.alertStatusLabel.setProperty('statusLabel', 'disconnected')
    self.alertStatusLabel.setText('已断开')
    self.alertListLayout.addWidget(self.alertLabel)
    self.alertListLayout.addWidget(self.alertStatusLabel)
    self.alertList.setLayout(self.alertListLayout)
    self.alertList.setFixedHeight(20)
 
    self.panelRightBodyContentLayout.addWidget(self.time1Label)
    self.panelRightBodyContentLayout.addWidget(self.time2Label)
    self.panelRightBodyContentLayout.addWidget(self.cameraList)
    self.panelRightBodyContentLayout.addWidget(self.xrayList)
    self.panelRightBodyContentLayout.addWidget(self.serverList)
    self.panelRightBodyContentLayout.addWidget(self.alertList)
    self.panelRightBodyContentLayout.setSpacing(6)

    self.panelRightBodyContent.setLayout(self.panelRightBodyContentLayout)

    self.panelRightBodyScroll = QScrollArea()
    self.panelRightBodyScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    self.panelRightBodyScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.panelRightBodyScroll.setWidget(self.panelRightBodyContent)
    self.panelRightBodyLayout.addWidget(self.panelRightBodyScroll)
    self.panelRightBody.setLayout(self.panelRightBodyLayout)
    
    self.infoPanelRightLayout.addWidget(self.panelRightTitle)
    self.infoPanelRightLayout.addWidget(self.panelRightBody)
    self.infoPanelRight.setLayout(self.infoPanelRightLayout)

    # 信息面板设置阴影
    renderShadow(self, self.infoPanelLeft, 0, 0, 10, QColor(200, 200, 200))
    renderShadow(self, self.infoPanelRight, 0, 0, 10, QColor(200, 200, 200))

    self.infoPanelLayout.addWidget(self.infoPanelLeft)
    self.infoPanelLayout.addWidget(self.infoPanelRight)
    self.setLayout(self.infoPanelLayout)


  # 累计程序运行时间
  def accumulateTime(self):
    dateNow = datetime.now()
    deltaTime = dateNow - getRootWidget(self).startTimestamp
    deltaSeconds = deltaTime.seconds
    days = math.floor(deltaSeconds / (3600 * 24))
    hours = math.floor(deltaSeconds % (3600 * 24) / 3600)
    minutes = math.floor(deltaSeconds % 3600 / 60)
    seconds = deltaSeconds % 60
    self.time1Label.setText('当前时间: ' + str(dateNow.strftime("%Y-%m-%d %H:%M:%S")))
    self.time2Label.setText('程序已运行 ' + str(days) + ' 天 ' + str(hours) + ' 时 ' 
      + str(minutes) + ' 分 ' + str(seconds) + ' 秒')


  def paintEvent(self, e):
    if not self.infoPanelLeft.isHidden() and not self.infoPanelRight.isHidden():
      newWidth = self.width() / 2
      newHeight = self.height() - self.panelTitleHeight
      self.panelLeftBodyContent.setMinimumSize(newWidth, newHeight - 20)
      self.panelRightBodyContent.setMinimumSize(newWidth, newHeight - 20)
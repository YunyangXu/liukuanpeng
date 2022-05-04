import sys, os
sys.path.append(os.path.join(__file__, '../../'))
import json

from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QWidget,  QLabel, QLineEdit, QHBoxLayout, QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QPoint, QUrl, pyqtSignal
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from layouts.StaticLayout import StaticLayoutWindow
from widgets.SubTitleBar import SubTitleBarWidget
from common.commlib import loadQss, lineEditValidation

staticPath = os.path.join(__file__, '../../../') + '/static'
configPath = os.path.join(__file__, '../../../') + '/config'


class NetworkWindowPage(StaticLayoutWindow):
  # 显示警告窗口信号
  showAlertSignal = pyqtSignal(str)
  # 设置按钮可用
  setBtnEnableSignal = pyqtSignal(str)

  def __init__(self):

    # 窗口尺寸
    self.windowWidth = 660
    self.windowHeight = 560

    # 阴影设置
    self.shadowX = 0
    self.shadowY = 0
    self.shadowWidth = 60
    self.shadowColor = QColor(132, 132, 132)

    # 样式表
    self.qss = staticPath + '/qss/para_window.qss'

    # 窗口标题
    self.windowTitle = '轮胎缺陷监测系统 - 网络设置'

    super(NetworkWindowPage, self).__init__(False, True, 0, 0, self.windowWidth, 
      self.windowHeight, self.shadowX, self.shadowY, self.shadowWidth, self.shadowColor)

    self.netManager = QNetworkAccessManager()

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
    self.menuBar = SubTitleBarWidget(self.windowTitle, False, False)
    self.menuBar.windowMove.connect(self.move)
    self.menuBar.windowClose.connect(self.closeWindow)
    # self.menuBar.installEventFilter(self)

    # 窗口面板
    self.mainPanel = QWidget()
    self.mainPanel.setObjectName('paraMainPanel')

    self.mainPanelLayout = QGridLayout()
    self.mainPanelLayout.setContentsMargins(0, 0, 0, 0)

    self.paraForm = QWidget()
    self.paraForm.setObjectName('paraForm')
    self.paraFormLayout = QVBoxLayout()
    self.paraFormLayout.setContentsMargins(40, 40, 40, 0)
    self.paraFormLayout.setAlignment(Qt.AlignTop)

    self.basicParaPanel = QWidget()
    self.basicParaPanelLayout = QGridLayout()
    self.basicParaPanelLayout.setSpacing(20)
    self.basicParaPanelLayout.setAlignment(Qt.AlignLeft)
    self.addressLabel = QLabel('服务器IP地址')
    self.addressLabel.setProperty('paraLabel', True)
    self.addressLabel.setFixedWidth(120)
    self.addressEdit = QLineEdit()
    self.addressEdit.setProperty('paraEdit', True)
    self.addressEdit.setFixedSize(300, 40)
    self.portLabel = QLabel('端口号')
    self.portLabel.setProperty('paraLabel', True)
    self.portEdit = QLineEdit()
    self.portEdit.setProperty('paraEdit', True)
    self.portEdit.setFixedSize(300, 40)
   
    self.basicParaPanelLayout.addWidget(self.addressLabel, 0, 0)
    self.basicParaPanelLayout.addWidget(self.addressEdit, 0, 1)
    self.basicParaPanelLayout.addWidget(self.portLabel, 1, 0)
    self.basicParaPanelLayout.addWidget(self.portEdit, 1, 1)
    self.basicParaPanel.setLayout(self.basicParaPanelLayout)

    self.paraErrorPanel = QWidget()
    self.paraErrorPanelLayout = QGridLayout()
    self.paraErrorLabel = QLabel()
    self.paraErrorLabel.setObjectName('paraErrorLabel')
    self.paraErrorPanelLayout.addWidget(self.paraErrorLabel)
    self.paraErrorPanel.setLayout(self.paraErrorPanelLayout)
    
    self.paraFormLayout.addWidget(self.basicParaPanel)
    self.paraFormLayout.addWidget(self.paraErrorPanel)
    self.paraForm.setLayout(self.paraFormLayout)

    self.btnPanel = QWidget()
    self.btnPanelLayout = QHBoxLayout()
    self.confirmBtn = QPushButton('保存参数')
    self.confirmBtn.setObjectName('confirmBtn')
    self.confirmBtn.setFixedSize(200, 50)
    self.confirmBtn.setCursor(Qt.PointingHandCursor)
    self.confirmBtn.clicked.connect(self.saveConfig)
    self.closeBtn = QPushButton('关闭')
    self.closeBtn.setObjectName('closeBtn')
    self.closeBtn.setFixedSize(100, 50)
    self.closeBtn.setCursor(Qt.PointingHandCursor)
    self.closeBtn.clicked.connect(self.closeWindow)
    self.btnPanelLayout.addStretch()
    self.btnPanelLayout.addWidget(self.confirmBtn)
    self.btnPanelLayout.addWidget(self.closeBtn)
    self.btnPanelLayout.addStretch()
    self.btnPanel.setLayout(self.btnPanelLayout)

    self.mainPanelLayout.addWidget(self.paraForm)
    self.mainPanelLayout.addWidget(self.btnPanel)
    self.mainPanel.setLayout(self.mainPanelLayout)

    self.mainGridLayout.addWidget(self.menuBar)
    self.mainGridLayout.addWidget(self.mainPanel)
    self.mainWidget.setLayout(self.mainGridLayout)

  # 关闭窗口
  def closeWindow(self):
    self.close()
  
  # 移动窗口
  def move(self, pos):
    super(NetworkWindowPage, self).move(pos - QPoint(self.shadowWidth, self.shadowWidth))

  # 校验参数
  def validation(self):
    arr = [
      {
        'labelName': self.addressLabel.text(),
        'widget': self.addressEdit,
        'empty': False,
        'reg': '^((25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$',
        'msg': 'IP地址格式错误'
      },
      {
        'labelName': self.portLabel.text(),
        'widget': self.portEdit,
        'empty': True,
        'reg': '^([0-9]|[1-9]\d|[1-9]\d{2}|[1-9]\d{3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$',
        'msg': '端口号必须为0-65535的整数'
      }
    ]
    isValid, errMsg = lineEditValidation(arr)
    self.paraErrorLabel.setText(errMsg)
    return isValid


  # 保存参数
  def saveConfig(self):
    isValid = self.validation()
    if not isValid:
      return
    # 检测网络通信是否正常
    host = self.addressEdit.text()
    port = self.portEdit.text()
    url = QUrl('http://' + host + ':' + str(port) + '/connection')
    req = QNetworkRequest(url)
    res = self.netManager.get(req)
    res.finished.connect(lambda: self.resFinished(res))
    res.error.connect(self.resError)


  def resFinished(self, res):
    # 获取状态码
    statusCode = res.attribute(QNetworkRequest.HttpStatusCodeAttribute)
    if statusCode != 200:
      return self.paraErrorLabel.setText('连接服务器失败，请检查IP地址和端口是否正确')
    else:
      # 将参数写入文件
      with open(configPath + '/global.dat', 'r', encoding='utf-8') as f:
        clientConfig = json.load(f)
      clientConfig['network_enable'] = True
      clientConfig['basic_setting']['ip_address'] = self.addressEdit.text()
      clientConfig['basic_setting']['port'] = self.portEdit.text()
      with open(configPath + '/global.dat', 'w', encoding='utf-8') as f:
        f.write(json.dumps(clientConfig))
      self.showAlertSignal.emit('网络参数保存成功')
      self.setBtnEnableSignal.emit('settingBtn')
      self.closeWindow()


  def resError(self, err):
    self.paraErrorLabel.setText('连接服务器失败，请检查IP地址和端口是否正确')


  # 回填参数
  def fillPara(self):
    with open(configPath + '/global.dat', 'r', encoding='utf-8') as f:
      clientConfig = json.load(f)
    self.addressEdit.setText(clientConfig['basic_setting']['ip_address'])
    self.portEdit.setText(clientConfig['basic_setting']['port'])
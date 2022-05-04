import sys, os
sys.path.append(os.path.join(__file__, '../../'))
import json

from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, \
  QScrollArea, QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QPoint, QUrl, pyqtSignal
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from layouts.StaticLayout import StaticLayoutWindow
from widgets.SubTitleBar import SubTitleBarWidget
from widgets.FormTitle import FormTitleWidget
from common.commlib import loadQss, lineEditValidation

staticPath = os.path.join(__file__, '../../../') + '/static'
configPath = os.path.join(__file__, '../../../') + '/config'


class ParameterWindowPage(StaticLayoutWindow):
  # 显示警告窗口信号
  showAlertSignal = pyqtSignal(str)
  # 设置按钮可用
  setBtnEnableSignal = pyqtSignal(str)

  def __init__(self):

    # 窗口尺寸
    self.windowWidth = 1280
    self.windowHeight = 1000

    # 阴影设置
    self.shadowX = 0
    self.shadowY = 0
    self.shadowWidth = 60
    self.shadowColor = QColor(132, 132, 132)

    # 样式表
    self.qss = staticPath + '/qss/para_window.qss'

    # 窗口标题
    self.windowTitle = '轮胎缺陷监测系统 - 参数设置'

    super(ParameterWindowPage, self).__init__(False, True, 0, 0, self.windowWidth, 
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
    self.menuBar = SubTitleBarWidget(self.windowTitle, True, False)
    self.menuBar.windowMove.connect(self.move)
    self.menuBar.windowFullScreen.connect(self.changeWindowSize)
    self.menuBar.windowClose.connect(self.closeWindow)
    self.menuBar.installEventFilter(self)

    # 窗口面板
    self.mainPanel = QWidget()
    self.mainPanel.setObjectName('paraMainPanel')

    self.mainPanelLayout = QGridLayout()
    self.mainPanelLayout.setContentsMargins(0, 0, 0, 0)

    self.mainPanelScroll = QScrollArea()
    self.mainPanelScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    self.mainPanelScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    self.paraForm = QWidget()
    self.paraForm.setObjectName('paraForm')
    self.paraForm.setMinimumSize(self.windowWidth - 2 * self.shadowWidth, 1800)
    self.paraFormLayout = QVBoxLayout()
    self.paraFormLayout.setContentsMargins(40, 40, 40, 40)
    self.paraFormLayout.setAlignment(Qt.AlignTop)

    self.paraTitleBasic = FormTitleWidget(125, '基本参数设置')
    self.basicParaPanel = QWidget()
    self.basicParaPanelLayout = QGridLayout()
    self.basicParaPanelLayout.setSpacing(20)
    self.basicParaPanelLayout.setAlignment(Qt.AlignLeft)
    self.productionLineLabel = QLabel('生产线编号')
    self.productionLineLabel.setProperty('paraLabel', True)
    self.productionLineLabel.setFixedWidth(120)
    self.productionLineEdit = QLineEdit()
    self.productionLineEdit.setProperty('paraEdit', True)
    self.typeLabel = QLabel('轮胎型号')
    self.typeLabel.setProperty('paraLabel', True)
    self.typeLabel.setFixedWidth(80)
    self.typeEdit = QLineEdit()
    self.typeEdit.setProperty('paraEdit', True)
    self.typeEdit.setFixedSize(300, 40)
    self.productionLineEdit.setFixedSize(300, 40)
    self.patternLabel = QLabel('检测模式')
    self.patternLabel.setProperty('paraLabel', True)
    self.patternLabel.setFixedWidth(120)
    self.patternCombox = QComboBox()
    self.patternCombox.setFixedSize(200, 40)
    self.patternCombox.setCursor(Qt.PointingHandCursor)

    self.basicParaPanelLayout.addWidget(self.productionLineLabel, 0, 0)
    self.basicParaPanelLayout.addWidget(self.productionLineEdit, 0, 1)
    self.basicParaPanelLayout.addWidget(self.typeLabel, 0, 2)
    self.basicParaPanelLayout.addWidget(self.typeEdit, 0, 3)
    self.basicParaPanelLayout.addWidget(self.patternLabel, 1, 0)
    self.basicParaPanelLayout.addWidget(self.patternCombox, 1, 1)
    self.basicParaPanel.setLayout(self.basicParaPanelLayout)

    self.paraTitleAlgorithm = FormTitleWidget(125, '算法参数设置')
    self.algoParaPanel = QWidget()
    self.algoParaPanelLayout = QGridLayout()
    self.algoParaPanelLayout.setSpacing(20)
    self.algoParaPanelLayout.setAlignment(Qt.AlignLeft)
    self.orderLabel = QLabel('轮胎内外侧顺序')
    self.orderLabel.setProperty('paraLabel', True)
    self.orderLabel.setFixedWidth(200)
    self.orderCombox = QComboBox()
    self.orderCombox.setFixedSize(200, 40)
    self.orderCombox.setCursor(Qt.PointingHandCursor)
    self.algoLabel = QLabel('内外侧检测算法')
    self.algoLabel.setProperty('paraLabel', True)
    self.algoLabel.setFixedWidth(200)
    self.algoCombox = QComboBox()
    self.algoCombox.setFixedSize(200, 40)
    self.algoCombox.setCursor(Qt.PointingHandCursor)
    self.x1Label = QLabel('截取图像上半部分坐标X')
    self.x1Label.setProperty('paraLabel', True)
    self.x1Label.setFixedWidth(200)
    self.x1Edit = QLineEdit()
    self.x1Edit.setFixedSize(200, 40)
    self.x1Edit.setProperty('paraEdit', True)
    self.y1Label = QLabel('截取图像上半部分坐标Y')
    self.y1Label.setProperty('paraLabel', True)
    self.y1Label.setFixedWidth(200)
    self.y1Edit = QLineEdit()
    self.y1Edit.setFixedSize(200, 40)
    self.y1Edit.setProperty('paraEdit', True)
    self.width1Label = QLabel('截取图像上半部分宽度')
    self.width1Label.setProperty('paraLabel', True)
    self.width1Label.setFixedWidth(200)
    self.width1Edit = QLineEdit()
    self.width1Edit.setFixedSize(200, 40)
    self.width1Edit.setProperty('paraEdit', True)
    self.height1Label = QLabel('截取图像上半部分高度')
    self.height1Label.setProperty('paraLabel', True)
    self.height1Label.setFixedWidth(200)
    self.height1Edit = QLineEdit()
    self.height1Edit.setFixedSize(200, 40)
    self.height1Edit.setProperty('paraEdit', True)
    self.x2Label = QLabel('截取图像下半部分坐标X')
    self.x2Label.setProperty('paraLabel', True)
    self.x2Label.setFixedWidth(200)
    self.x2Edit = QLineEdit()
    self.x2Edit.setFixedSize(200, 40)
    self.x2Edit.setProperty('paraEdit', True)
    self.y2Label = QLabel('截取图像下半部分坐标Y')
    self.y2Label.setProperty('paraLabel', True)
    self.y2Label.setFixedWidth(200)
    self.y2Edit = QLineEdit()
    self.y2Edit.setFixedSize(200, 40)
    self.y2Edit.setProperty('paraEdit', True)
    self.width2Label = QLabel('截取图像下半部分宽度')
    self.width2Label.setProperty('paraLabel', True)
    self.width2Label.setFixedWidth(200)
    self.width2Edit = QLineEdit()
    self.width2Edit.setFixedSize(200, 40)
    self.width2Edit.setProperty('paraEdit', True)
    self.height2Label = QLabel('截取图像下半部分高度')
    self.height2Label.setProperty('paraLabel', True)
    self.height2Label.setFixedWidth(200)
    self.height2Edit = QLineEdit()
    self.height2Edit.setFixedSize(200, 40)
    self.height2Edit.setProperty('paraEdit', True)
    self.algo2Label = QLabel('胎冠缺陷检测算法')
    self.algo2Label.setProperty('paraLabel', True)
    self.algo1List = QWidget()
    self.algo1ListLayout = QGridLayout()
    self.algo1ListLayout.setContentsMargins(0, 0, 0, 0)
    self.algo1ListLayout.setAlignment(Qt.AlignTop)
    self.algo1List.setLayout(self.algo1ListLayout)
    self.algo3Label = QLabel('胎侧缺陷检测算法')
    self.algo3Label.setProperty('paraLabel', True)
    self.algo2List = QWidget()
    self.algo2ListLayout = QGridLayout()
    self.algo2ListLayout.setContentsMargins(0, 0, 0, 0)
    self.algo2ListLayout.setAlignment(Qt.AlignTop)
    self.algo2List.setLayout(self.algo2ListLayout)

    self.algoParaPanelLayout.addWidget(self.orderLabel, 0, 0)
    self.algoParaPanelLayout.addWidget(self.orderCombox, 0, 1)
    self.algoParaPanelLayout.addWidget(self.algoLabel, 1, 0)
    self.algoParaPanelLayout.addWidget(self.algoCombox, 1, 1)
    self.algoParaPanelLayout.addWidget(self.x1Label, 2, 0)
    self.algoParaPanelLayout.addWidget(self.x1Edit, 2, 1)
    self.algoParaPanelLayout.addWidget(self.y1Label, 2, 2)
    self.algoParaPanelLayout.addWidget(self.y1Edit, 2, 3)
    self.algoParaPanelLayout.addWidget(self.width1Label, 3, 0)
    self.algoParaPanelLayout.addWidget(self.width1Edit, 3, 1)
    self.algoParaPanelLayout.addWidget(self.height1Label, 3, 2)
    self.algoParaPanelLayout.addWidget(self.height1Edit, 3, 3)
    self.algoParaPanelLayout.addWidget(self.x2Label, 4, 0)
    self.algoParaPanelLayout.addWidget(self.x2Edit, 4, 1)
    self.algoParaPanelLayout.addWidget(self.y2Label, 4, 2)
    self.algoParaPanelLayout.addWidget(self.y2Edit, 4, 3)
    self.algoParaPanelLayout.addWidget(self.width2Label, 5, 0)
    self.algoParaPanelLayout.addWidget(self.width2Edit, 5, 1)
    self.algoParaPanelLayout.addWidget(self.height2Label, 5, 2)
    self.algoParaPanelLayout.addWidget(self.height2Edit, 5, 3)
    self.algoParaPanelLayout.addWidget(self.algo2Label, 6, 0)
    self.algoParaPanelLayout.addWidget(self.algo1List, 7, 0)
    self.algoParaPanelLayout.addWidget(self.algo3Label, 8, 0)
    self.algoParaPanelLayout.addWidget(self.algo2List, 9, 0)
    self.algoParaPanel.setLayout(self.algoParaPanelLayout)

    self.paraTitleInstruction = FormTitleWidget(125, '指令参数设置')
    self.illustrationPanel = QWidget()
    self.illustrationPanel.setObjectName('illustrationPanel')
    self.illustrationPanelLayout = QGridLayout()
    self.illustrationLabel = QLabel()
    self.illustrationLabel.setObjectName('illustrationLabel')
    self.illustrationText = '指令设置示例：6-A#B#C;7-E#F 该指令表示每检测6幅图像后串行执行A、B、C操作，' \
    '且每检测7幅图像后执行E、F操作'
    self.illustrationLabel.setText(self.illustrationText)
    self.illustrationPanelLayout.addWidget(self.illustrationLabel)
    self.illustrationPanel.setLayout(self.illustrationPanelLayout)
    self.instructionParaPanel = QWidget()
    self.instructionParaPanelLayout = QGridLayout()
    self.instructionParaPanelLayout.setSpacing(20)
    self.instructionParaPanelLayout.setAlignment(Qt.AlignLeft)
    self.instructionLabel = QLabel('缺陷检测指令')
    self.instructionLabel.setProperty('paraLabel', True)
    self.instructionLabel.setFixedWidth(120)
    self.instructionEdit = QLineEdit()
    self.instructionEdit.setProperty('paraEdit', True)
    self.instructionEdit.setFixedSize(600, 40)
    self.instructionParaPanelLayout.addWidget(self.instructionLabel, 0, 0)
    self.instructionParaPanelLayout.addWidget(self.instructionEdit, 0, 1)
    self.instructionParaPanel.setLayout(self.instructionParaPanelLayout)
    self.actionPanel = QWidget()
    self.actionPanel.setObjectName('actionPanel')
    self.actionPanelLayout = QGridLayout()
    self.actionLabel = QLabel()
    self.actionLabel.setObjectName('actionLabel')
    self.actionPanelLayout.addWidget(self.actionLabel)
    self.actionPanel.setLayout(self.actionPanelLayout)
    
    self.paraTitleOther = FormTitleWidget(125, '其他参数设置')
    self.otherParaPanel = QWidget()
    self.otherParaPanelLayout = QGridLayout()
    self.otherParaPanelLayout.setAlignment(Qt.AlignLeft)
    self.alarmLabel = QLabel('警报装置')
    self.alarmLabel.setProperty('paraLabel', True)
    self.alarmLabel.setFixedWidth(200)
    self.alarmCombox = QComboBox()
    self.alarmCombox.addItem('开启', True)
    self.alarmCombox.addItem('关闭', False)
    self.alarmCombox.setFixedSize(200, 40)
    self.alarmCombox.setCursor(Qt.PointingHandCursor)
    self.otherParaPanelLayout.addWidget(self.alarmLabel, 0, 0)
    self.otherParaPanelLayout.addWidget(self.alarmCombox, 0, 1)
    self.otherParaPanel.setLayout(self.otherParaPanelLayout)

    self.paraErrorPanel = QWidget()
    self.paraErrorPanelLayout = QGridLayout()
    self.paraErrorLabel = QLabel()
    self.paraErrorLabel.setObjectName('paraErrorLabel')
    self.paraErrorPanelLayout.addWidget(self.paraErrorLabel)
    self.paraErrorPanel.setLayout(self.paraErrorPanelLayout)

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
    
    self.paraFormLayout.addWidget(self.paraTitleBasic)
    self.paraFormLayout.addWidget(self.basicParaPanel)
    self.paraFormLayout.addWidget(self.paraTitleAlgorithm)
    self.paraFormLayout.addWidget(self.algoParaPanel)
    self.paraFormLayout.addWidget(self.paraTitleInstruction)
    self.paraFormLayout.addWidget(self.illustrationPanel)
    self.paraFormLayout.addWidget(self.instructionParaPanel)
    self.paraFormLayout.addWidget(self.actionPanel)
    self.paraFormLayout.addWidget(self.paraTitleOther)
    self.paraFormLayout.addWidget(self.otherParaPanel)
    self.paraFormLayout.addWidget(self.paraErrorPanel)
    self.paraFormLayout.addWidget(self.btnPanel)
    self.paraForm.setLayout(self.paraFormLayout)

    self.mainPanelScroll.setWidget(self.paraForm)
    self.mainPanelLayout.addWidget(self.mainPanelScroll)
    self.mainPanel.setLayout(self.mainPanelLayout)

    self.mainGridLayout.addWidget(self.menuBar)
    self.mainGridLayout.addWidget(self.mainPanel)
    self.mainWidget.setLayout(self.mainGridLayout)


  # 最小化窗口
  def changeWindowSize(self, msg):
    self.showMinimized()


  # 关闭窗口
  def closeWindow(self):
    self.close()
  

  # 移动窗口
  def move(self, pos):
    super(ParameterWindowPage, self).move(pos - QPoint(self.shadowWidth, self.shadowWidth))


  # 从服务器获取参数选项
  def getSelections(self):
    with open(configPath + '/global.dat', 'r', encoding='utf-8') as f:
      self.clientConfig = json.load(f)
    host = self.clientConfig['basic_setting']['ip_address']
    port = self.clientConfig['basic_setting']['port']
    url = QUrl('http://' + host + ':' + str(port) + '/selections')
    req = QNetworkRequest(url)
    res = self.netManager.get(req)
    res.finished.connect(lambda: self.resFinished(res))
    res.error.connect(self.resError)


  def resFinished(self, res):
    recvData = res.readAll()
    data = str(bytes(recvData.data()), encoding='utf-8')
    # 获取状态码
    statusCode = res.attribute(QNetworkRequest.HttpStatusCodeAttribute)
    if statusCode != 200:
      return
    self.fillPara(data)

  def resError(self, err):
    self.showAlertSignal.emit('请求参数错误，请检查网络连接状态')


  # 回填参数
  def fillPara(self, data):
    # 加载选项
    paraData = json.loads(data)

    # 检测模式
    checkType = paraData['checkType']
    self.patternCombox.clear()
    for i in range(0, len(checkType)):
      self.patternCombox.addItem(checkType[i]['name'], checkType[i]['value'])

    # 轮胎内外侧顺序
    tyreOrder = paraData['tyreOrder']
    self.orderCombox.clear()
    for i in range(0, len(tyreOrder)):
      self.orderCombox.addItem(tyreOrder[i]['name'], tyreOrder[i]['value'])

    # 内外侧检测算法
    algorithm1 = paraData['algorithm1']
    self.algoCombox.clear()
    for i in range(0, len(algorithm1)):
      self.algoCombox.addItem(algorithm1[i]['name'], algorithm1[i]['value'])

    # 胎冠缺陷检测算法
    head = paraData['algorithm2']['head']
    while not self.algo1ListLayout.isEmpty():
      child = self.algo1ListLayout.takeAt(0)
      child.widget().setParent(None)
      child = None
    for i in range(0, len(head)):
      checkBox = QCheckBox(head[i]['name'], self)
      checkBox.setProperty('value', head[i]['value'])
      checkBox.setCursor(Qt.PointingHandCursor)
      self.algo1ListLayout.addWidget(checkBox)

    # 胎侧缺陷检测算法
    side = paraData['algorithm2']['side']
    while not self.algo2ListLayout.isEmpty():
      child = self.algo2ListLayout.takeAt(0)
      child.widget().setParent(None)
      child = None
    for i in range(0, len(side)):
      checkBox = QCheckBox(side[i]['name'], self)
      checkBox.setProperty('value', side[i]['value'])
      checkBox.setCursor(Qt.PointingHandCursor)
      self.algo2ListLayout.addWidget(checkBox)
      
    # 指令参数选项
    instruction = paraData['instruction']
    self.actionLabel.setText('\n'.join(instruction))    

    # 从本地保存的参数文件中回填表单
    basicSetting = self.clientConfig['basic_setting']
    self.productionLineEdit.setText(basicSetting['line_number'])
    self.typeEdit.setText(basicSetting['tyre_type'])
    for i in range(0, len(checkType)):
      if checkType[i]['value'] == basicSetting['check_type']:
        self.patternCombox.setCurrentIndex(i)

    algorithmSetting = self.clientConfig['algorithm_setting']
    for i in range(0, len(tyreOrder)):
      if tyreOrder[i]['value'] == algorithmSetting['tyre_order']:
        self.orderCombox.setCurrentIndex(i)
    for i in range(0, len(algorithm1)):
      if algorithm1[i]['value'] == algorithmSetting['algorithm1']:
        self.algoCombox.setCurrentIndex(i)
    self.x1Edit.setText(algorithmSetting['top_x'])
    self.y1Edit.setText(algorithmSetting['top_y'])
    self.width1Edit.setText(algorithmSetting['top_width'])
    self.height1Edit.setText(algorithmSetting['top_height'])
    self.x2Edit.setText(algorithmSetting['bottom_x'])
    self.y2Edit.setText(algorithmSetting['bottom_y'])
    self.width2Edit.setText(algorithmSetting['bottom_width'])
    self.height2Edit.setText(algorithmSetting['bottom_height'])
    
    algorithm2 = algorithmSetting['algorithm2']
    for i in range(0, len(head)):
      checkbox = self.algo1ListLayout.itemAt(i).widget()
      for j in range(0, len(algorithm2)):
        if checkbox.property('value') == algorithm2[j]:
          checkbox.setChecked(True)
          break
    for i in range(0, len(side)):
      checkbox = self.algo2ListLayout.itemAt(i).widget()
      for j in range(0, len(algorithm2)):
        if checkbox.property('value') == algorithm2[j]:
          checkbox.setChecked(True)
          break

    instructionSetting = self.clientConfig['instruction_setting']
    self.instructionEdit.setText(instructionSetting)

    otherSetting = self.clientConfig['other_setting']
    if otherSetting['alert_enable']:
      self.alarmCombox.setCurrentIndex(0)
    else:
      self.alarmCombox.setCurrentIndex(1)


  # 保存参数
  def saveConfig(self):
    # 校验参数
    arr = [
      {
        'labelName': self.productionLineLabel.text(),
        'widget': self.productionLineEdit,
        'empty': False,
        'reg': '',
        'msg': ''
      },
      {
        'labelName': self.typeLabel.text(),
        'widget': self.typeEdit,
        'empty': False,
        'reg': '',
        'msg': ''
      },
      {
        'labelName': self.x1Label.text(),
        'widget': self.x1Edit,
        'empty': False,
        'reg': '^\d+$',
        'msg': self.x1Label.text() + '必须为正整数'
      },
      {
        'labelName': self.y1Label.text(),
        'widget': self.y1Edit,
        'empty': False,
        'reg': '^\d+$',
        'msg': self.y1Label.text() + '必须为正整数'
      },
      {
        'labelName': self.width1Label.text(),
        'widget': self.width1Edit,
        'empty': False,
        'reg': '^\d+$',
        'msg': self.width1Label.text() + '必须为正整数'
      },
      {
        'labelName': self.height1Label.text(),
        'widget': self.height1Edit,
        'empty': False,
        'reg': '^\d+$',
        'msg': self.height1Label.text() + '必须为正整数'
      },
      {
        'labelName': self.x2Label.text(),
        'widget': self.x2Edit,
        'empty': False,
        'reg': '^\d+$',
        'msg': self.x2Label.text() + '必须为正整数'
      },
      {
        'labelName': self.y2Label.text(),
        'widget': self.y2Edit,
        'empty': False,
        'reg': '^\d+$',
        'msg': self.y2Label.text() + '必须为正整数'
      },
      {
        'labelName': self.width2Label.text(),
        'widget': self.width2Edit,
        'empty': False,
        'reg': '^\d+$',
        'msg': self.width2Label.text() + '必须为正整数'
      },
      {
        'labelName': self.height2Label.text(),
        'widget': self.height2Edit,
        'empty': False,
        'reg': '^\d+$',
        'msg': self.height2Label.text() + '必须为正整数'
      },
      {
        'labelName': self.instructionLabel.text(),
        'widget': self.instructionEdit,
        'empty': True,
        'reg': '^(\d+-[A-Za-z](#[A-Za-z]){0,})(;\d+-[A-Za-z](#[A-Za-z]{1,}){0,}){0,}$',
        'msg': '指令格式错误，请参考示例，注意分号和短横线为英文字符，且两侧不能有空格'
      },
    ]
    isValid, errMsg = lineEditValidation(arr)
    
    # 胎冠算法参数
    head = []
    # 胎侧算法参数
    side = []
    # 检测checkbox是否选中
    for i in range(0, self.algo1ListLayout.count()):
      checkbox = self.algo1ListLayout.itemAt(i).widget()
      if checkbox.isChecked():
        head.append(checkbox.property('value'))
    for i in range(0, self.algo2ListLayout.count()):
      checkbox = self.algo2ListLayout.itemAt(i).widget()
      if checkbox.isChecked():
        side.append(checkbox.property('value'))
    if len(head) <= 0:
      isValid = False
      errMsg += '\n请至少选择一个胎冠缺陷检测算法'
    if len(side) <= 0:
      isValid = False
      errMsg += '\n请至少选择一个胎侧缺陷检测算法'

    if not isValid:
      return self.paraErrorLabel.setText(errMsg)

    # 将参数写入文件
    basicSetting = self.clientConfig['basic_setting']
    basicSetting['line_number'] = self.productionLineEdit.text()
    basicSetting['tyre_type'] = self.typeEdit.text()
    basicSetting['check_type'] = self.patternCombox.currentData()

    algorithmSetting = self.clientConfig['algorithm_setting']
    algorithmSetting['tyre_order'] = self.orderCombox.currentData()
    algorithmSetting['algorithm1'] = self.algoCombox.currentData()
    algorithmSetting['top_x'] = self.x1Edit.text()
    algorithmSetting['top_y'] = self.y1Edit.text()
    algorithmSetting['top_width'] = self.width1Edit.text()
    algorithmSetting['top_height'] = self.height1Edit.text()
    algorithmSetting['bottom_x'] = self.x2Edit.text()
    algorithmSetting['bottom_y'] = self.y1Edit.text()
    algorithmSetting['bottom_width'] = self.width2Edit.text()
    algorithmSetting['bottom_height'] = self.height2Edit.text()
    algorithmSetting['algorithm2'] = head + side
    
    self.clientConfig['instruction_setting'] = self.instructionEdit.text()

    other_setting = self.clientConfig['other_setting']
    other_setting['alert_enable'] = self.alarmCombox.currentData()

    self.clientConfig['sys_enable'] = True

    with open(configPath + '/global.dat', 'w', encoding='utf-8') as f:
        f.write(json.dumps(self.clientConfig))
    self.showAlertSignal.emit('系统参数保存成功')
    self.setBtnEnableSignal.emit('all')
    self.closeWindow()
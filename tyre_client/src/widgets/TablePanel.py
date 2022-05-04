import sys, os
sys.path.append(os.path.join(__file__, '../../'))

from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, \
  QDateTimeEdit, QPushButton, QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtCore import Qt, QDateTime, QTime, QDate
from widgets.TableDelegate import ReadOnlyDelegate, DownloadBtnDelegate
from common.commlib import loadQss

staticPath = os.path.join(__file__, '../../../') + '/static'

class TablePanelWidget(QWidget):
  def __init__(self):
    super().__init__()

    # 样式表
    self.qss = staticPath + '/qss/table_panel.qss'
  
    self.render()

  def render(self):
    self.setStyleSheet(loadQss(self.qss))

    self.layout = QGridLayout()
    self.layout.setContentsMargins(20, 20, 20, 20)

    self.searchBar = QWidget()
    self.searchBar.setFixedHeight(60)
    self.searchBarLayout = QHBoxLayout()
    self.searchBarLayout.setContentsMargins(0, 0, 0, 0)
    self.searchBarLayout.setAlignment(Qt.AlignLeft)

    self.condLabel = QLabel('是否合格')
    self.condLabel.setProperty('searchLabel', True)
    self.comboBox = QComboBox()
    self.comboBox.addItems(['全部', '合格', '不合格'])
    self.comboBox.setFixedWidth(120)
    self.styleLabel = QLabel('轮胎型号')
    self.styleLabel.setProperty('searchLabel', True)
    self.styleEdit = QLineEdit()
    self.styleEdit.setProperty('paraEdit', True)
    self.styleEdit.setFixedWidth(280)
    self.lineLabel = QLabel('生产线编号')
    self.lineLabel.setProperty('searchLabel', True)
    self.lineEdit = QLineEdit()
    self.lineEdit.setProperty('paraEdit', True)
    self.lineEdit.setFixedWidth(280)

    self.searchBar2 = QWidget()
    self.searchBar2.setFixedHeight(60)
    self.searchBarLayout2 = QHBoxLayout()
    self.searchBarLayout2.setContentsMargins(0, 0, 0, 0)
    self.searchBarLayout2.setAlignment(Qt.AlignLeft)

    self.condLabel2 = QLabel('开始时间')
    self.condLabel2.setProperty('searchLabel', True)
    self.dateEdit = QDateTimeEdit(QDate.currentDate())
    self.dateEdit.setCalendarPopup(True)
    self.dateEdit.setDisplayFormat('yyyy.MM.dd  HH:mm:ss')
    self.dateEdit.setFixedWidth(240)
    self.condLabel3 = QLabel('结束时间')
    self.condLabel3.setProperty('searchLabel', True)
    endDate = QDateTime.currentDateTime()
    endTime = QTime()
    endTime.setHMS(23, 59, 59)
    endDate.setTime(endTime)
    self.dateEdit2 = QDateTimeEdit(endDate)
    self.dateEdit2.setDisplayFormat('yyyy.MM.dd  HH:mm:ss')
    self.dateEdit2.setFixedWidth(240)
    self.dateEdit2.setCalendarPopup(True)
    self.condLabel4 = QLabel('每页显示条数')
    self.condLabel4.setProperty('searchLabel', True)
    self.comboBox2 = QComboBox()
    self.comboBox2.addItems(['10', '50', '100', '500', '1000'])
    self.comboBox2.setFixedWidth(100)
    self.searchBtn = QPushButton('搜索')
    self.searchBtn.setFixedSize(80, 40)
    self.searchBtn.setObjectName('searchBtn')
    self.searchBtn.setCursor(Qt.PointingHandCursor)

    self.searchBarLayout.addWidget(self.condLabel)
    self.searchBarLayout.addWidget(self.comboBox)
    self.searchBarLayout.addWidget(self.styleLabel)
    self.searchBarLayout.addWidget(self.styleEdit)
    self.searchBarLayout.addWidget(self.lineLabel)
    self.searchBarLayout.addWidget(self.lineEdit)
    self.searchBarLayout.addStretch()
    self.searchBarLayout2.addWidget(self.condLabel2)
    self.searchBarLayout2.addWidget(self.dateEdit)
    self.searchBarLayout2.addWidget(self.condLabel3)
    self.searchBarLayout2.addWidget(self.dateEdit2)
    self.searchBarLayout2.addWidget(self.condLabel4)
    self.searchBarLayout2.addWidget(self.comboBox2)
    self.searchBarLayout2.addWidget(self.searchBtn)
    self.searchBar.setLayout(self.searchBarLayout)
    self.searchBar2.setLayout(self.searchBarLayout2)

    self.dataTable = QWidget()
    self.dataTableLayout = QGridLayout()
    self.dataTableLayout.setContentsMargins(0, 0, 0, 0)
    self.dataTableView = QTableView()
    self.dataModel = QStandardItemModel()
    self.dataModel.setColumnCount(6)
    self.dataModel.setHeaderData(0, Qt.Horizontal, '轮胎编号')
    self.dataModel.setHeaderData(1, Qt.Horizontal, '生产线编号')
    self.dataModel.setHeaderData(2, Qt.Horizontal, '检测结束时间')
    self.dataModel.setHeaderData(3, Qt.Horizontal, '是否合格')
    self.dataModel.setHeaderData(4, Qt.Horizontal, '详细描述')
    self.dataModel.setHeaderData(5, Qt.Horizontal, '操作')
    

    for i in range(0, 1000):
      self.dataModel.setItem(i, 0, QStandardItem('155/651R3 73T'))
      self.dataModel.setItem(i, 1, QStandardItem('A-1'))
      self.dataModel.setItem(i, 2, QStandardItem('2022-04-05 21:45:05'))
      self.dataModel.setItem(i, 3, QStandardItem('合格'))
      self.dataModel.setItem(i, 4, QStandardItem(''))
      # self.dataModel.setItem(i, 5, QStandardItem('下载检测报告'))

    self.dataTableView.setModel(self.dataModel)

    # for i in range(0, 100):
    #   btn = QPushButton('点击下载检测报告')
    #   btn.setStyleSheet('border: 0; font-family: "Microsoft YaHei"; color: #2E9AFE; ')
    #   self.dataTableView.setIndexWidget(self.dataModel.index(i, 5), btn)

    # 设置表格不可编辑
    self.dataTableView.setItemDelegate(ReadOnlyDelegate())
    self.dataTableView.setItemDelegateForColumn(5, DownloadBtnDelegate(self.dataTableView))
    self.dataTableView.setMouseTracking(True)

    
    self.dataTableLayout.addWidget(self.dataTableView)
    self.dataTable.setLayout(self.dataTableLayout)

    self.pageBar = QWidget()
    self.pageBarLayout = QHBoxLayout()
    self.pageBarLayout.setContentsMargins(0, 0, 0, 0)
    self.pageBarLayout.setAlignment(Qt.AlignLeft)
    self.pageBar.setFixedHeight(60)
    self.pageBarLayout.addStretch()
    self.pageLabel = QLabel('1/36')
    self.pageLabel.setObjectName('pageLabel')
    self.firstBtn = QPushButton('首页')
    self.firstBtn.setProperty('pageBtn', True)
    self.firstBtn.setCursor(Qt.PointingHandCursor)
    self.preBtn = QPushButton('上一页')
    self.preBtn.setProperty('pageBtn', True)
    self.preBtn.setCursor(Qt.PointingHandCursor)
    self.nextBtn = QPushButton('下一页')
    self.nextBtn.setProperty('pageBtn', True)
    self.nextBtn.setCursor(Qt.PointingHandCursor)
    self.lastBtn = QPushButton('尾页')
    self.lastBtn.setProperty('pageBtn', True)
    self.lastBtn.setCursor(Qt.PointingHandCursor)
    self.pageBarLayout.addStretch()
    self.pageBarLayout.addWidget(self.pageLabel)
    self.pageBarLayout.addWidget(self.firstBtn)
    self.pageBarLayout.addWidget(self.preBtn)
    self.pageBarLayout.addWidget(self.nextBtn)
    self.pageBarLayout.addWidget(self.lastBtn)
    self.pageBar.setLayout(self.pageBarLayout)

    self.layout.addWidget(self.searchBar)
    self.layout.addWidget(self.searchBar2)
    self.layout.addWidget(self.dataTable)
    self.layout.addWidget(self.pageBar)
    self.setLayout(self.layout)
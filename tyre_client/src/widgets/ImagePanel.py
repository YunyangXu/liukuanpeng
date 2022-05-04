import os, sys
sys.path.append(os.path.join(__file__, '../../'))
from datetime import datetime

from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel, QScrollArea
from PyQt5.QtGui import QFont, QColor, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize
from widgets.PanelSplit import PanelSplitWidget
from common.commlib import loadQss, renderShadow

staticPath = os.path.join(__file__, '../../../') + '/static'

class ImagePanelWidget(QWidget):
  def __init__(self):
    super().__init__()

    # 标题高度
    self.titleHeight = 40
    # 图片和容器的内边距
    self.imgPadding = 5
    # 图片高宽比
    self.imgRatio = 1080 / 1920
    # 样式表
    self.qss = staticPath + '/qss/image_panel.qss'

    self.render()
      
  def render(self):
    self.setAttribute(Qt.WA_StyledBackground, True)
    self.setStyleSheet(loadQss(self.qss))

    # 布局
    self.imgPanelLayout = QGridLayout()
    self.imgPanelLayout.setContentsMargins(12, 12, 12, 6)
    self.imgPanelLayout.setSpacing(0)

    # 图片面板
    self.innerPanel = QWidget()
    self.innerPanel.setObjectName('imgInnerPanel')
    
    self.innerPanelLayout = QGridLayout()
    self.innerPanelLayout.setContentsMargins(0, 0, 0, 0)
    self.innerPanelLayout.setSpacing(0)
    self.innerTitle = QWidget()
    self.innerTitle.setObjectName('imgInnerTitle')
    self.innerTitle.setFixedHeight(self.titleHeight)
    self.innerTitleLayout = QHBoxLayout()
    self.innerTitleIcon = QLabel()
    self.innerTitleIcon.setObjectName('innerTitleIcon')
    self.innerTitleIcon.setFixedWidth(24)
    icon = QPixmap()
    icon.load(staticPath + '/icons/image.svg')
    self.innerTitleIcon.setPixmap(icon.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
    self.innerTitleText = QLabel()
    self.innerTitleText.setObjectName('innerTitleText')
    self.innerTitleText.setText('图像信息')
    self.innerTitleText.setFont(QFont('Microsoft YaHei'))
    self.innerTitleLayout.addWidget(self.innerTitleIcon)
    self.innerTitleLayout.addWidget(self.innerTitleText)
    self.innerTitle.setLayout(self.innerTitleLayout)

    self.innerBody = QWidget()
    self.innerBodyLayout = QHBoxLayout()
    self.innerBodyLayout.setContentsMargins(0, 0, 0, 0)
    self.innerBodyLayout.setSpacing(0)

    self.innerBodyLeft = QWidget()
    self.innerBodyLeft.setObjectName('imgLeft')
    self.innerBodyLeftLayout = QGridLayout()
    self.innerBodyLeftLayout.setContentsMargins(0, 0, 0, 0)
    self.innerBodyLeftLayout.setSpacing(0)
    self.innerBodyLeftTitle = QWidget()
    self.innerBodyLeftTitleLayout = QHBoxLayout()
    self.innerBodyLeftTitleLayout.setContentsMargins(10, 0, 10, 0)
    self.innerBodyLeftName = QLabel()
    self.innerBodyLeftName.setObjectName('innerBodyLeftName')
    self.innerBodyLeftName.setFixedWidth(70)
    self.innerBodyLeftName.setText('原始图像')
    self.innerBodyLeftName.setFont(QFont('Microsoft YaHei'))
    self.innerBodyLeftTime = QLabel()
    self.innerBodyLeftTime.setObjectName('innerBodyLeftTime')
    self.innerBodyLeftTime.setFont(QFont('Microsoft YaHei'))
    self.innerBodyLeftTitleLayout.addWidget(self.innerBodyLeftName)
    self.innerBodyLeftTitleLayout.addWidget(self.innerBodyLeftTime)
    self.innerBodyLeftTitle.setLayout(self.innerBodyLeftTitleLayout)
    self.innerBodyLeftTitle.setFixedHeight(30)

    self.innerBodyLeftContent = QWidget()
    self.innerBodyLeftContentLayout = QGridLayout()
    self.innerBodyLeftContentLayout.setContentsMargins(self.imgPadding, 0, self.imgPadding, self.imgPadding)

    self.innerBodyLeftContentScroll = QScrollArea()
    self.innerBodyLeftContentScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    self.innerBodyLeftContentScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.innerBodyLeftContentImage = QLabel()
    self.innerBodyLeftContentImage.setStyleSheet('background-color: #F6F6F6')
    # 图片自适应组件大小
    self.innerBodyLeftContentImage.setScaledContents(True)

    self.innerBodyLeftContentScroll.setWidget(self.innerBodyLeftContentImage)
    self.innerBodyLeftContentLayout.addWidget(self.innerBodyLeftContentScroll)
    self.innerBodyLeftContent.setLayout(self.innerBodyLeftContentLayout)
    self.innerBodyLeftLayout.addWidget(self.innerBodyLeftTitle)
    self.innerBodyLeftLayout.addWidget(self.innerBodyLeftContent)
    self.innerBodyLeft.setLayout(self.innerBodyLeftLayout)

    # 分割线
    self.innerBodySplit = PanelSplitWidget()

    self.innerBodyRight = QWidget()
    self.innerBodyRightLayout = QGridLayout()
    self.innerBodyRightLayout.setContentsMargins(0, 0, 0, 0)
    self.innerBodyRightLayout.setSpacing(0)
    self.innerBodyRightTitle = QWidget()
    self.innerBodyRightTitleLayout = QHBoxLayout()
    self.innerBodyRightTitleLayout.setContentsMargins(10, 0, 10, 0)
    self.innerBodyRightName = QLabel()
    self.innerBodyRightName.setObjectName('innerBodyRightName')
    self.innerBodyRightName.setFixedWidth(70)
    self.innerBodyRightName.setText('检测结果')
    self.innerBodyRightName.setFont(QFont('Microsoft YaHei'))
    self.innerBodyRightTime = QLabel()
    self.innerBodyRightTime.setObjectName('innerBodyRightTime')
    self.innerBodyRightTime.setFont(QFont('Microsoft YaHei'))
    self.innerBodyRightTitleLayout.addWidget(self.innerBodyRightName)
    self.innerBodyRightTitleLayout.addWidget(self.innerBodyRightTime)
    self.innerBodyRightTitle.setLayout(self.innerBodyRightTitleLayout)
    self.innerBodyRightTitle.setFixedHeight(30)
    self.innerBodyRight.setObjectName('imgRight')

    self.innerBodyRightContent = QWidget()
    self.innerBodyRightContentLayout = QGridLayout()
    self.innerBodyRightContentLayout.setContentsMargins(self.imgPadding, 0, self.imgPadding, self.imgPadding)

    self.innerBodyRightContentScroll = QScrollArea()
    self.innerBodyRightContentScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    self.innerBodyRightContentScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.innerBodyRightContentImage = QLabel()
    self.innerBodyRightContentImage.setStyleSheet('background-color: #F6F6F6')

    # 图片自适应组件大小
    self.innerBodyRightContentImage.setScaledContents(True)

    self.innerBodyRightContentScroll.setWidget(self.innerBodyRightContentImage)
    self.innerBodyRightContentLayout.addWidget(self.innerBodyRightContentScroll)
    self.innerBodyRightContent.setLayout(self.innerBodyRightContentLayout)
    self.innerBodyRightLayout.addWidget(self.innerBodyRightTitle)
    self.innerBodyRightLayout.addWidget(self.innerBodyRightContent)
    self.innerBodyRight.setLayout(self.innerBodyRightLayout)

    self.innerBodyLayout.addWidget(self.innerBodyLeft)
    self.innerBodyLayout.addWidget(self.innerBodySplit)
    self.innerBodyLayout.addWidget(self.innerBodyRight)
    self.innerBody.setLayout(self.innerBodyLayout)
    
    self.innerPanelLayout.addWidget(self.innerTitle)
    self.innerPanelLayout.addWidget(self.innerBody)
    self.innerPanel.setLayout(self.innerPanelLayout)

    # 图片面板设置阴影
    renderShadow(self, self.innerPanel, 0, 0, 10, QColor(200, 200, 200))

    self.imgPanelLayout.addWidget(self.innerPanel)
    self.setLayout(self.imgPanelLayout)


  # 更新图片面板
  def updateImgPanel(self, imgArr, dir):
    imgBytes = bytes(imgArr)
    img = QImage().fromData(imgBytes)
    pixmap = QPixmap.fromImage(img)
    print(img)
    # 更新原始图片
    if dir == 'left':
      self.innerBodyLeftTime.setText(str(datetime.now()))
      self.innerBodyLeftContentImage.setPixmap(pixmap)

    # 更新结果图片
    else:
      self.innerBodyRightTime.setText(str(datetime.now()))
      self.innerBodyRightContentImage.setPixmap(pixmap)


  # 清空图片面板
  def clearImgPanel(self, dir):
    if dir == 'left':
      self.innerBodyLeftTime.setText('')
      self.innerBodyLeftContentImage.clear()
    else:
      self.innerBodyRightTime.setText('')
      self.innerBodyRightContentImage.clear()


  def paintEvent(self, e):
    # 调整图片的大小
    self.innerBodyLeftContentImage.resize(QSize((self.innerBodyLeftContent.width() -  2 * self.imgPadding), 
      (self.innerBodyLeftContent.width() - 2 * self.imgPadding) * self.imgRatio))
    self.innerBodyRightContentImage.resize(QSize((self.innerBodyRightContent.width() -  2 * self.imgPadding), 
    (self.innerBodyRightContent.width() - 2 * self.imgPadding) * self.imgRatio))
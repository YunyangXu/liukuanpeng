import sys, os
sys.path.append(os.path.join(__file__, '../../'))

from PyQt5.QtWidgets import QItemDelegate, QPushButton, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt


# Table单元格不可编辑
class ReadOnlyDelegate(QItemDelegate):
  def __init__(self):
    super(ReadOnlyDelegate, self).__init__()
  
  def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
    return None



class DownloadBtnDelegate(QItemDelegate):
  def __init__(self, parent):
    super(DownloadBtnDelegate, self).__init__(parent)


  def paint(self, painter, option, index):
    if not self.parent().indexWidget(index):
        button_read = QPushButton(
          self.tr('下载检测报告'),
          self.parent(),
        )
        button_read.setStyleSheet('border: 0; color: #2E9AFE; background-color: #FFFFFF; font-family: Microsoft YaHei')
        button_read.setCursor(Qt.PointingHandCursor)
        button_read.index = [index.row(), index.column()]
        h_box_layout = QHBoxLayout()
        h_box_layout.addWidget(button_read)
        h_box_layout.setContentsMargins(0, 0, 0, 0)
        h_box_layout.setAlignment(Qt.AlignCenter)
        widget = QWidget()
        widget.setLayout(h_box_layout)
        self.parent().setIndexWidget(
          index,
          widget
        )


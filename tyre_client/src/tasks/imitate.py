import os
import random
from PyQt5.QtCore import QThread

imgPath = os.path.join(__file__, '../../../') + '/static/imgs'


'''
  任务模拟线程
  根据配置文件中的检测模式从对应目录循环读取图像文件，置入缓冲区中
'''
class ReadImage(QThread):

  exitFlag = False

  def __init__(self, config, buffer):

    super().__init__()
    self.config = config
    self.buffer = buffer

  
  def run(self):

    i = 0
    self.checkType = int(self.config['basic_setting']['check_type'])
    if self.checkType == 0:
      p = imgPath + '/test0/'
    else:
      p = imgPath + '/test1/'
    imgNames = os.listdir(p)
    # 随机打乱
    random.shuffle(imgNames)

    while True:
      if self.exitFlag:
        break
      # 循环读取图像文件，每2s读一张
      with open(p + imgNames[i], 'rb') as f:
        bytes = f.read()
        # 将bytes转为bytearray
        bytesArr = bytearray(bytes)
        # 置入缓冲区
        self.buffer.put(bytesArr)
      i = (i + 1) % len(imgNames)
      self.sleep(2)
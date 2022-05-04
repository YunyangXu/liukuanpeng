import cv2

from PyQt5.QtCore import QThread, pyqtSignal


class CameraCapture(QThread):

  sendImgSignal = pyqtSignal(object, bool)
  camera = None
  exitFlag = False

  def __init__(self, width, height):
    super().__init__()
    self.width = width
    self.height = height
  
  def run(self):
    # 打开摄像头
    self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
    self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.width)
    while True:
      if self.exitFlag:
        self.camera.release()
        break
      ret, frame = self.camera.read()
      try:
        b, g, r = cv2.split(frame)      
        rgbFrame = cv2.merge((r, g, b))
        self.sendImgSignal.emit(rgbFrame, True)
      except: 
        self.sendImgSignal.emit(frame, False)
        break
      


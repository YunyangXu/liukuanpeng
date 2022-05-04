'''
  与部件及业务逻辑相关的公用函数
'''

from PyQt5.QtWidgets import QGraphicsDropShadowEffect
import uuid
import re
import json


# 读取qss文件，外部加载qss
def loadQss(url):
  with open(url, 'r') as f:
    return f.read()


# 给窗口或组件设置外层阴影
def renderShadow(obj, widget, shadowX, shadowY, shadowWidth, shadowColor):
  effectShadow = QGraphicsDropShadowEffect(obj)
  effectShadow.setOffset(shadowX, shadowY)
  effectShadow.setBlurRadius(shadowWidth)
  effectShadow.setColor(shadowColor)
  obj.setGraphicsEffect(effectShadow)
  widget.setGraphicsEffect(effectShadow)


# 获取根组件
def getRootWidget(widget):
  while widget.parentWidget() != None:
    widget = widget.parentWidget()
  return widget


# 获取MAC地址
def getMACAddress():
  mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
  return ':'.join([mac[e : e + 2] for e in range(0, 11, 2)])


# 校验QLineEdit控件中的参数
def lineEditValidation(arr):
  isValid = True
  message = []
  for i in range(0, len(arr)):
    labelName = arr[i]['labelName']
    widget = arr[i]['widget']
    empty = arr[i]['empty']
    reg = arr[i]['reg']
    msg = arr[i]['msg']
    res, errMsg = editItemValidation(labelName, widget, empty, reg, msg)
    if not res:
      isValid = False
      message.append(errMsg)
  return isValid, '\n'.join(message)


def editItemValidation(labelName, widget, empty, reg, msg):
  # labelName: 标签名称
  # widget: 控件实例
  # empty: 是否允许为空
  # reg: 正则表达式字符串
  # msg: 错误提示信息
  isValid = True
  errMsg = ''
  if (not empty) and widget.text() == '':
    isValid = False
    errMsg = labelName + '不能为空'
  elif widget.text() != '' and not bool(re.match(reg, widget.text())):
    isValid = False
    errMsg = msg
  if isValid:
    widget.setStyleSheet('border-color: #D8D8D8')
  else:
    widget.setStyleSheet('border-color: red')
  return isValid, errMsg


# 将图像bytearray拆分并封装成帧，每帧数据实体长度不超过32kB
def imgToFrames(config, imgArr, dataLen=32 * 1024):
  
  resArr = []

  # 封装数据实体
  for i in range(0, int(len(imgArr) / dataLen)):
    frame = imgArr[dataLen * i : dataLen * (i + 1)]
    resArr.append(frame)
  lastFrame = imgArr[int(len(imgArr) / dataLen) * dataLen :]
  resArr.append(lastFrame)

  macAddress = getMACAddress()
  frameId = uuid.uuid1().hex

  # 封装首部
  for i in range(0, len(resArr) + 1):
    frame = bytearray()
    # 帧头 4字节 0000表示请求帧，1111表示响应帧
    frame += bytearray('0000', encoding='utf-8')
    # 客户端MAC地址 17字节
    frame += bytearray(macAddress, encoding='utf-8')
    # 帧标识 32字节 随机生成uuid
    frame += bytearray(frameId, encoding='utf-8')
    # 总帧数 4字节 大端模式存储，总帧数为图像帧数 + 请求参数1帧
    frame += bytearray((len(resArr) + 1).to_bytes(4, byteorder='big'))
    # 当前帧索引 4字节 大端模式存储
    frame += bytearray(i.to_bytes(4, byteorder='big'))
    # 状态码 2字节 200表示正常 300表示重传 400表示异常
    frame += bytearray((200).to_bytes(2, byteorder='big'))
    # 数据实体，除最后一帧外其余帧皆为图像帧，最后一帧为请求参数 
    if i != len(resArr):
      frame += resArr[i]
      resArr[i] = frame
    else:
      # 封装请求参数帧
      params = {}
      basicSetting = config['basic_setting']
      # 生产线编号
      params['line_number'] = basicSetting['line_number']
      # 轮胎型号
      params['tyre_type'] = basicSetting['tyre_type']
      # 检测模式
      params['check_type'] = basicSetting['check_type']
      # 算法参数
      params['algorithm'] = config['algorithm_setting']
      params['instruction'] = config['instruction_setting']
      frame += bytearray(json.dumps(params), encoding='utf-8')
      resArr.append(frame)

  return resArr
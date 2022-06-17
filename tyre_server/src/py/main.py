'''
  此文件为算法模块的入口文件
  接收算法参数组成的json
  从文件中读取图像并从json中提取参数，执行识别任务
  本入口文件仅作为示例，规定出入参数格式，模拟识别任务并返回随机结果
  后续应继续在py目录下补充算法模块，并在此文件中引用
'''

import sys, io
import time
import json
import base64
import random
import os


# 模拟执行任务所耗时间，后续将此语句删掉
time.sleep(1.5)


# 获取Node进程传递的参数 
params = sys.argv
# 获取文件名
fileName = params[1]
# 获取算法参数
# 这样做的目的是防止json字符串在传递过程中双引号丢失
paramsBytes = params[2].encode('ascii')
algoParams = json.loads((base64.b64decode(paramsBytes)).decode('ascii'))


# 根据文件名和任务类型从对应目录下读取图像，执行检测任务
# imgs目录下有nwc和qx两个目录，其中nwc存储内外侧检测图像，qx中存储缺陷检测图像
# 由于内外侧检测原始图像和结果图像相同，所以无子目录
# qx目录下的original目录存储原始图像，result目录存储检测后的缺陷标记图像
dirname = os.path.abspath(os.path.join(os.getcwd()))
checkType = algoParams['check_type']
if int(checkType) == 0:
  filePath = dirname + '/tyre_server/imgs/qx/original/' + fileName + '.bmp'
else:
  filePath = dirname + '/tyre_server/imgs/nwc/' + fileName + '.jpg'

with open(filePath, 'rb') as f:
  img = f.read()


# 检测结果格式为json字符串，{ res: 1, msg: [] }
# 其中res表示检测结果，0为图像有缺陷，1为图像无缺陷，2为无法检测或检测失败
# msg表示检测结果信息，用数组存储
# 例：检测模式为内外侧检测，检测后返回{ res: 0, msg: ['轮胎位置反'] }
# 例：检测模式为缺陷检测，检测后返回{ res: 0, msg: ['胎冠裂纹', '帘线稀疏'] }，msg中数组的索引 + 1对应缺陷结果图像中的标记
# 即图中标记为1的缺陷是胎冠裂纹，图中标记为2的缺陷是帘线稀疏
resNum = [0, 1, 2]
resMsg = ['胎冠裂纹', '胎侧气泡', '胎侧杂质', '帘线稀疏', '接头开']
result = {}

index = random.randint(0, 2)
result['res'] = resNum[index]
result['msg'] = []

# 模拟执行检测任务，随机返回检测结果
if int(checkType) == 0:
  # 缺陷检测
  if resNum[index] == 0:
    # 随机生成缺陷个数
    errNum = random.randint(1, 8)
    for i in range(0, errNum):
      result['msg'].append(resMsg[random.randint(0, 4)])
  elif resNum[index] == 2:
    result['msg'].append('检测失败原因')
else:
  # 内外侧检测
  if resNum[index] == 0:
    result['msg'].append('轮胎位置放反')
  elif resNum[index] == 2:
    result['msg'].append('检测失败原因')


# 检测完毕后，将结果图像写入对应目录中，检测模式为内外侧检测时不需要存储结果图像
# 仅将检测出异常的图像写入文件
if int(checkType) == 0 and result['res'] == 0:
  filePath = dirname + '/tyre_server/imgs/qx/result/' + fileName + '.bmp'


with open(filePath, 'wb') as f:
  f.write(img)


# 保证返回中文不乱码
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')


# 返回检测结果
# 返回结果时，使用print输出，Node进程接收stdout值
print(json.dumps(result, ensure_ascii=False))
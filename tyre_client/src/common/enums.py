from enum import Enum


# socket状态枚举类
class socketStateEnum(Enum):
  # 无状态
  stateNone = 0
  # 已连接
  connected = 1
  # 已断开
  disconnected = 2
  # 重连中
  reconnecting = 3
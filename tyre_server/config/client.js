// 客户端参数选项
module.exports = {
  // 检测模式
  checkType: [
    {
      name: '缺陷检测',
      value: 0,
    },
    {
      name: '内外侧检测',
      value: 1,
    }
  ],
  // 轮胎内外侧顺序
  tyreOrder: [
    {
      name: '内侧朝上',
      value: 0,
    },
    {
      name: '外侧朝上',
      value: 1,
    }
  ],
  // 内外侧检测算法
  algorithm1: [
    {
      name: 'SVM',
      value: 0,
    },
    {
      name: 'Logic',
      value: 1,
    },
  ],
  // 缺陷检测算法
  algorithm2: {
    // 胎冠缺陷检测算法
    head: [
      {
        name: '胎冠裂纹检测算法',
        value: 'a0'
      },
    ],
    // 胎侧缺陷检测算法
    side: [
      {
        name: '胎侧杂物检测算法',
        value: 'b0'
      },
      {
        name: '胎侧气泡检测算法',
        value: 'b1'
      },
      {
        name: '胎侧帘线检测算法',
        value: 'b2'
      },
    ]
  },
  // 指令参数选项
  instruction: [
    'A: 生成检测报告',
  ],
}
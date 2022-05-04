const clientConfig = require('../../config/client');


// 客户端通信测试
exports.connectionTest = (req, res) => {
  return res.json({ res: true });
}


// 获取客户端参数选项
exports.getClientSelections = (req, res) => {
  return res.json(clientConfig);
}
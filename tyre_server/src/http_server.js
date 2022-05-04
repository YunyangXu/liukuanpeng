const express = require('express');
const http = require('http');
const app = express();
const server = http.createServer(app);
const bodyParser = require('body-parser');


/* 注册中间件 */
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());


// const checkRecordsSv = require('./sv/check_records_sv');
const clientSv = require('./sv/client_sv');


// // 查询轮胎缺陷检测结论
// app.get("/setting/configs", settingSv.listConfigs);
// // 查询检测记录
// app.get("/setting/configs", settingSv.listConfigs);
// 客户端通信测试
app.get('/connection', clientSv.connectionTest)
// 获取客户端参数选项
app.get('/selections', clientSv.getClientSelections)


// 捕获全局异常
process.on('uncaughtException', err => {

});


// 启动服务器
server.listen(8080, () => {
  console.log('HTTP Server is starting');
});
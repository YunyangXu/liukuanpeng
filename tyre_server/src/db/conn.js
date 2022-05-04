const mongoose = require('mongoose');
const redis = require('redis');
const { join } = require('path');
const configDir = join(__dirname, '../../config/');
const logger = require(configDir + 'logger').databaseLogger;
const { mongo: mongoConfig, redis: redisConfig } = require(configDir + 'db');


// 连接mongoDB数据库
const { 
  uri: mongoUri, 
  port: mongoPort, 
  user: mongoUser, 
  password: mongoPassword, 
  dbName } = mongoConfig;
const mongoUrl = `mongodb://${mongoUser}:${mongoPassword}@${mongoUri}:${mongoPort}/${dbName}`;

mongoose.connect(mongoUrl, { useNewUrlParser: true, useUnifiedTopology: true }).catch(e => {
  // 连接失败，退出Node进程
  console.error(`mongoDB连接失败: ${e.message}请检查mongoDB用户权限及连接参数`);
  process.exit(1);
});

const mongoDB = mongoose.connection;

// 监听mongoDB连接事件
mongoDB.on('connected', () => {
  logger.info('mongoDB连接成功');
});


// 连接redis数据库
const { uri: redisUri, port: redisPort } = redisConfig;
const redisDB = redis.createClient(redisPort, redisUri);

redisDB.connect().catch(e => {
  console.error(`redis连接失败: ${e.message}，请检查是否开启redis-server`);
  process.exit(1);
});


module.exports = { mongoDB, redisDB };
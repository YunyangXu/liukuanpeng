const mongoose = require('mongoose');
const { mongoDB } = require('../db/conn');


const checkRecordsSchema = new mongoose.Schema({
    id: String,
    // 轮胎型号
    tyre_type: String,
    // 生产线编号
    line_number: String,
    // 客户端物理地址
    client_mac: String,
    // 检测开始时间
    start_time: Date,
    // 检测结束时间
    end_time: Date,
    // 检测模式：内外侧检测/缺陷检测
    check_type: Number,
    // 检测是否合格：1合格/0不合格/2检测失败/3算法模块执行错误
    acceptable: Number,
    // 检测结果描述
    description: [String],
});


const checkRecordsModel = mongoDB.model("ty_records", checkRecordsSchema);
module.exports = checkRecordsModel;
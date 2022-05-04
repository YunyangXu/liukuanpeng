const mongoose = require('mongoose');
const { mongoDB } = require('../db/conn');


const conslusionsSchema = new mongoose.Schema({
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
    // 检测是否合格
    acceptable: Boolean,
    // 检测结论描述
    description: [Number],
    // 检测记录id列表
    check_records_ids: [String]
});


const conslusionsModel = mongoDB.model("ty_conslusions", conslusionsSchema);
module.exports = conslusionsModel;
const mongoose = require('mongoose');
const { mongoDB } = require('../db/conn');


const tyreImgsSchema = new mongoose.Schema({
    id: String,
    // 检测记录编号
    check_record_id: String,
    // 原始图像路径
    original_path: String,
    // 检测结果图像路径
    result_path: String,
});


const tyreImgsModel = mongoDB.model("ty_images", tyreImgsSchema);
module.exports = tyreImgsModel;
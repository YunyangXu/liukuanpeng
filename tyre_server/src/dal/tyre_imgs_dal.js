const { join } = require('path');
const baseDir = join(__dirname, '../../');
const logger = require(baseDir + 'config/logger').databaseLogger;
const tyreImgsModel = require(baseDir + 'src/model/tyre_imgs');
const UUID = require("uuid");


// 增加一条轮胎图像记录
exports.store = async (params) => {
  const id = UUID.v1();
  const tyreImg = new tyreImgsModel({
    id: id,
    check_record_id: params.checkRecordId,
    original_path: params.originalPath,
    result_path: params.resultPath,
  });
  try {
    let res = await tyreImg.save();
    if (res.errors) {
      logger.error('Insert to ty_records failed: ' + res.errors)
      return { res: 'InternalError' };
    }
    return { res: true, id: id };
  } catch (err) {
    logger.error('Insert to ty_records failed: ' + err)
    return { res: 'InternalError' };
  }
}


// 聚合查询
exports.find = async (params) => {
  try {
    let tyreImgsList = await tyreImgsModel.aggregate(params);
    if (tyreImgsList == null) {
      return { res: false };
    }
    return { res: tyreImgsList };
  } catch (err) {
    logger.error('Find from ty_images failed: ' + err)
    return { res: 'InternalError' };
  }
}
const { join } = require('path');
const baseDir = join(__dirname, '../../');
const logger = require(baseDir + 'config/logger').databaseLogger;
const checkRecordsModel = require(baseDir + 'src/model/check_records');


// 增加一条检测记录
exports.store = async (params) => {
  const startTime = new Date(params.startTime);
  const endTime = new Date(params.endTime);
  startTime.setHours(startTime.getHours() + 8);
  endTime.setHours(endTime.getHours() + 8);
  const record = new checkRecordsModel({
    id: params.frameId,
    tyre_type: params.tyreType,
    line_number: params.lineNumber,
    client_mac: params.clientMac,
    start_time: startTime,
    end_time: endTime,
    check_type: params.checkType,
    acceptable: params.acceptable,
    description: params.description,
  });
  try {
    let res = await record.save();
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
    let checkRecordsList = await checkRecordsModel.aggregate(params);
    if (checkRecordsList == null) {
      return { res: false };
    }
    return { res: checkRecordsList };
  } catch (err) {
    logger.error('Find from ty_records failed: ' + err)
    return { res: 'InternalError' };
  }
}
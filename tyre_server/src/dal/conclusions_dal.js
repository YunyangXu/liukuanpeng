const { join } = require('path');
const baseDir = join(__dirname, '../../');
const logger = require(baseDir + 'config/logger').databaseLogger;
const conclusionsModel = require(baseDir + 'src/model/conclusions');
const UUID = require("uuid");


// 增加一条结论记录
exports.store = async (params) => {
  const startTime = new Date(params.startTime);
  const endTime = new Date(params.endTime);
  startTime.setHours(startTime.getHours() + 8);
  endTime.setHours(endTime.getHours() + 8);
  const id = UUID.v1();
  const conclusion = new conclusionsModel({
    id: id,
    tyre_type: params.tyreType,
    line_number: params.lineNumber,
    client_mac: params.clientMac,
    start_time: startTime,
    end_time: endTime,
    acceptable: params.acceptable,
    description: params.description,
    check_records_ids: params.checkRecordsIds,
  });
  try {
    let res = await conclusion.save();
    if (res.errors) {
      logger.error('Insert to ty_conclusions failed: ' + res.errors)
      return { res: 'InternalError' };
    }
    return { res: true, id: id };
  } catch (err) {
    logger.error('Insert to ty_conclusions failed: ' + err)
    return { res: 'InternalError' };
  }
}


// 聚合查询
exports.find = async (params) => {
  try {
    let conclusionsList = await conclusionsModel.aggregate(params);
    if (conclusionsList == null) {
      return { res: false };
    }
    return { res: conclusionsList };
  } catch (err) {
    logger.error('Find from ty_conclusions failed: ' + err)
    return { res: 'InternalError' };
  }
}
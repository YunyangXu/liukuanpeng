const moment = require("moment");
const checkRecordsDal = require('../dal/check_records_dal');


// 查询检测记录列表
exports.list = async (params) =>  {
  // 组装查询条件
  let match = {};
  // 日期查询范围：起始日期的00:00:00至结束日期的23:59:59
  let startDate = new Date(params.dateStart);
  let endDate = new Date(params.dateEnd);
  // 加8小时（mongoDB存储的是世界时，会自动减8小时）
  startDate.setHours(0 + 8);
  startDate.setMinutes(0);
  startDate.setSeconds(0);
  endDate.setHours(23 + 8);
  endDate.setMinutes(59);
  endDate.setSeconds(59);
  match['start_time'] = {
    $gte: startDate,
    $lte: endDate
  };
  if (params.keywords) {
    match['tyre_type'] = { $regex: params.tyreType };
    match['line_number'] = { $regex: params.lineNumber };
    match['check_type'] = { $regex: Number(params.checkType) };
    match['acceptable'] = { $regex: Number(params.acceptable) };
  }
  // 按照开始检测时间倒序查询
  let sort = { start_time: Number(params.display) };
  let limit = Number(params.pageSize);
  let skip = (Number(params.pageNum) - 1) * limit;

  // 默认按时间倒序排序
  let status = await checkRecordsDal.find([
    {
      $match: match
    },
    {
      $sort: sort
    },
    {
      $skip: skip
    },
    {
      $limit: limit
    }
  ]);

  // 查询对应条件的总数
  let cond2 = [
    { $match: match },
    { $sort: sort },
    { $count: "num" }
  ];
  let numStatus = await checkRecordsDal.find(cond2);
  let num = 0;
  if (numStatus.res.length > 0) {
    num = numStatus.res[0].num;
  }

  if (status.res === "InternalError") {
    return { res: false, msg: "查询检测记录失败，内部错误" };
  } else {
    // 格式化日期
    for (let i = 0; i < status.res.length; i++) {
      let startTime = new Date(status.res[i].start_time);
      let endTime = new Date(status.res[i].end_time);
      // 减去8小时
      startTime.setHours(startTime.getHours() - 8);
      endTime.setHours(endTime.getHours() - 8);
      status.res[i].start_time = moment(startTime).format("YYYY-MM-DD HH:mm:ss");
      status.res[i].end_time = moment(endTime).format("YYYY-MM-DD HH:mm:ss");
    }
    return { res: true, msg: status.res, num: num };
  }
};


// 增加一条检测记录
exports.store = async (params) => {
  let status = await checkRecordsDal.store(params);
  if (status.res === true) {
    return { res: true, msg: '新增检测记录成功' };
  } else if (status.res === 'InternalError') {
    return { res: false, msg: '新增检测记录失败，内部错误' };
  }
}
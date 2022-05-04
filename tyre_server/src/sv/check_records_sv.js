const checkRecordsBll = require("../bll/check_records_bll");


exports.list = async (req, res) => {
  let params = {};
  // 关键字：说说内容
  params.keywords = req.query.keywords;
  // 开始检测时间
  params.dateStart = req.query.dateStart || "1970-01-01";
  params.dateEnd = req.query.dateEnd || "2099-12-31";
  // 每页显示条数，默认为10
  params.pageSize = req.query.pageSize || 10;
  // 显示哪一页，默认为第1页
  params.pageNum = req.query.pageNum || 1;
  let status = await checkRecordsBll.list(params);
  return res.json(status);
}
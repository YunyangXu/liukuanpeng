const log4js = require('log4js');


log4js.configure({
  appenders: { 
    access: { 
      type: 'file', 
      filename: 'log/access.log',
      maxLogSize: 1048576000,
      layout: {
        type: 'pattern',
        pattern: '[%d] %m'
      } 
    },
    database: { 
      type: 'file', 
      filename: 'log/database.log',
      layout: {
        type: 'pattern',
        pattern: '[%d] [%p] %m'
      }
    },
    application: { 
      type: 'file', 
      filename: 'log/application.log',
      layout: {
        type: 'pattern',
        pattern: '[%d] [%p] %m'
      } 
    }
  },
  categories: {
    default: {
      appenders: ['application'], 
      level: 'info' 
    }, 
    accessLogger: { 
      appenders: ['access'], 
      level: 'info' 
    },
    databaseLogger: { 
      appenders: ['database'], 
      level: 'info' 
    },
    applicationLogger: { 
      appenders: ['application'], 
      level: 'info' 
    }
  }
});


const accessLogger = log4js.getLogger('accessLogger');
const databaseLogger = log4js.getLogger('databaseLogger');
const applicationLogger = log4js.getLogger('applicationLogger');


module.exports = {
  accessLogger: accessLogger,
  databaseLogger: databaseLogger,
  applicationLogger: applicationLogger
}
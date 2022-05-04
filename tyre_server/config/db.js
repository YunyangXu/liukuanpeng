const dbConfig = {
  mongo: {
    uri: 'localhost',
    port: 27017,
    user: 'admin',
    password: '123!!!',
    dbName: 'tyre',
  },
  redis: {
    uri: 'localhost',
    port: 6379,
  }
}

module.exports = dbConfig;
// config/database.js
const { Sequelize } = require('sequelize');

const sequelize = new Sequelize(
  process.env.DB_NAME || 'student_db',
  process.env.DB_USER || 'root', 
  process.env.DB_PASSWORD || '',
  {
    host: process.env.DB_HOST || 'localhost',  // ← YE IMPORTANT HAI!
    port: process.env.DB_PORT || 3306,
    dialect: 'mysql',
    logging: false  // Optional: logs clean rakhne ke liye
  }
);

module.exports = sequelize;
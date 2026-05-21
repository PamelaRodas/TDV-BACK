const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
      serverSelectionTimeoutMS: 5000,
      socketTimeoutMS: 45000,
    });

    console.log(`✅ MongoDB Connected: ${conn.connection.host}`);
    return conn;
  } catch (error) {
    console.warn(`⚠️ MongoDB unavailable - running in demo mode`);
    console.warn(`   Message: ${error.message}`);
    console.warn('💡 To use database: Install MongoDB locally OR configure MongoDB Atlas');
    console.warn('📝 See SETUP.md for configuration instructions');
    // Server continues without database
    return null;
  }
};

module.exports = connectDB;

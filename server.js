const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
require('dotenv').config();

const app = express();

app.use(helmet());
app.use(cors());


app.use(express.json());
app.use(express.urlencoded({ limit: '50mb', extended: true }));

app.use('/uploads', express.static('uploads'));


let dbConnected = false;
if (process.env.MONGODB_URI && process.env.MONGODB_URI !== 'mongodb://localhost:27017/manifestation-journal') {
  try {
    const connectDB = require('./config/db');
    connectDB().then((conn) => {
      if (conn) dbConnected = true;
    });
  } catch (error) {
    console.warn('⚠️ Database initialization skipped - using demo mode');
  }
}

app.use('/api/auth', require('./routes/auth'));
app.use('/api/home', require('./routes/home'));
app.use('/api/diary', require('./routes/diary'));
app.use('/api/photos', require('./routes/photos'));
app.use('/api/growth', require('./routes/growth'));
app.use('/api/sacred-space', require('./routes/sacredSpace'));
app.use('/api/studio', require('./routes/studio'));
app.use('/api/users', require('./routes/users'));
app.use('/api/analytics', require('./routes/analytics'));

app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'Backend running successfully', 
    timestamp: new Date(),
    database: dbConnected ? 'connected' : 'demo-mode'
  });
});

const demoModeHandler = require('./middleware/demoMode');
app.use(demoModeHandler);

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
  });
});

app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`✨ Manifestation Journal Backend running on port ${PORT}`);
  console.log(`📱 Environment: ${process.env.NODE_ENV}`);
  if (!dbConnected) {
    console.log('🎮 Mode: DEMO (without persistent database)');
    console.log('💡 To enable database: Configure MongoDB or MongoDB Atlas');
  }
});

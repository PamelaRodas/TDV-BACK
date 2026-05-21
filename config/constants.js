module.exports = {
  cors: {
    origin: [
      'http://localhost:3000',
      'http://localhost:3001',
      'http://127.0.0.1:3000',
      'http://127.0.0.1:3001',
      // Agregar URLs de producción aquí
      // 'https://tudominio.com'
    ],
    credentials: true,
  },

  jwt: {
    expiresIn: '30d',
  },

  upload: {
    maxFileSize: process.env.MAX_FILE_SIZE || 5242880, // 5MB
    allowedMimeTypes: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
  },

  pagination: {
    defaultLimit: 10,
    maxLimit: 100,
  },
};

const express = require('express');
const diaryController = require('../controllers/diaryController');
const authenticateToken = require('../middleware/auth');

const router = express.Router();

// Obtener todas las entradas creadas en Studio
router.get('/entries', authenticateToken, diaryController.getEntries);

// Crear nueva entrada en Studio
router.post('/entries', authenticateToken, diaryController.createEntry);

// Obtener una entrada específica
router.get('/entries/:id', authenticateToken, diaryController.getEntry);

// Actualizar entrada
router.put('/entries/:id', authenticateToken, diaryController.updateEntry);

// Eliminar entrada
router.delete('/entries/:id', authenticateToken, diaryController.deleteEntry);

module.exports = router;

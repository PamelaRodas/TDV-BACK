const express = require('express');
const diaryController = require('../controllers/diaryController');
const authenticateToken = require('../middleware/auth');

const router = express.Router();

// Obtener estadísticas del diario
router.get('/stats', authenticateToken, diaryController.getDiaryStats);

// Obtener todas las entradas
router.get('/', authenticateToken, diaryController.getEntries);

// Crear nueva entrada
router.post('/', authenticateToken, diaryController.createEntry);

// Obtener una entrada específica
router.get('/:id', authenticateToken, diaryController.getEntry);

// Actualizar entrada
router.put('/:id', authenticateToken, diaryController.updateEntry);

// Eliminar entrada
router.delete('/:id', authenticateToken, diaryController.deleteEntry);

module.exports = router;

const express = require('express');
const sacredSpaceController = require('../controllers/sacredSpaceController');
const authenticateToken = require('../middleware/auth');

const router = express.Router();

// Obtener espacios sagrados
router.get('/', sacredSpaceController.getSacredSpaces);

// Crear espacio sagrado (Admin)
router.post('/', authenticateToken, sacredSpaceController.createSacredSpace);

// Obtener un espacio específico
router.get('/:id', sacredSpaceController.getSacredSpace);

// Actualizar espacio (Admin)
router.put('/:id', authenticateToken, sacredSpaceController.updateSacredSpace);

// Eliminar espacio (Admin)
router.delete('/:id', authenticateToken, sacredSpaceController.deleteSacredSpace);

module.exports = router;

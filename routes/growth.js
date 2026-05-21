const express = require('express');
const growthController = require('../controllers/growthController');
const authenticateToken = require('../middleware/auth');

const router = express.Router();

// Obtener contenidos de growth
router.get('/', growthController.getGrowthContent);

// Crear contenido (Admin)
router.post('/', authenticateToken, growthController.createGrowthContent);

// Obtener un contenido específico
router.get('/:id', growthController.getGrowthItem);

// Actualizar contenido (Admin)
router.put('/:id', authenticateToken, growthController.updateGrowthContent);

// Eliminar contenido (Admin)
router.delete('/:id', authenticateToken, growthController.deleteGrowthContent);

module.exports = router;

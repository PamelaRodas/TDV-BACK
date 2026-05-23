const express = require('express');
const growthController = require('../controllers/growthController');
const authenticateToken = require('../middleware/auth');

const router = express.Router();

router.get('/', growthController.getGrowthContent);

router.post('/', authenticateToken, growthController.createGrowthContent);

router.get('/:id', growthController.getGrowthItem);

router.put('/:id', authenticateToken, growthController.updateGrowthContent);

// Eliminar contenido (Admin)
router.delete('/:id', authenticateToken, growthController.deleteGrowthContent);

module.exports = router;

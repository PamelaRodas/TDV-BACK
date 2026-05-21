const express = require('express');
const photoController = require('../controllers/photoController');
const authenticateToken = require('../middleware/auth');

const router = express.Router();

// Obtener todas las fotos
router.get('/', authenticateToken, photoController.getPhotos);

// Crear nueva foto
router.post('/', authenticateToken, photoController.createPhoto);

// Obtener una foto específica
router.get('/:id', authenticateToken, photoController.getPhoto);

// Actualizar foto
router.put('/:id', authenticateToken, photoController.updatePhoto);

// Eliminar foto
router.delete('/:id', authenticateToken, photoController.deletePhoto);

module.exports = router;

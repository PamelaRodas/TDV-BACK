const express = require('express');
const homeController = require('../controllers/homeController');
const authenticateToken = require('../middleware/auth');

const router = express.Router();

// Obtener datos del Home
router.get('/', homeController.getHome);

// Actualizar datos del Home (requiere autenticación - Admin)
router.put('/', authenticateToken, homeController.updateHome);

module.exports = router;

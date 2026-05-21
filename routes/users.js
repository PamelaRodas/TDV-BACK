const express = require('express');
const userController = require('../controllers/userController');
const authenticateToken = require('../middleware/auth');

const router = express.Router();

// Obtener perfil del usuario autenticado
router.get('/profile', authenticateToken, userController.getUserProfile);

// Actualizar perfil del usuario
router.put('/profile', authenticateToken, userController.updateUserProfile);

// Cambiar contraseña
router.post('/change-password', authenticateToken, userController.changePassword);

// Eliminar cuenta
router.delete('/account', authenticateToken, userController.deleteAccount);

// Obtener perfil público de un usuario
router.get('/public/:id', userController.getPublicUserProfile);

module.exports = router;

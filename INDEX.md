# 📚 ÍNDICE DE DOCUMENTACIÓN

## Guías Disponibles

### 🚀 Para Comenzar Rápido
- **[QUICKSTART.md](QUICKSTART.md)** ← Comienza aquí
  - Instalación en 5 minutos
  - Comandos esenciales
  - Primeras pruebas

### 📖 Documentación Completa
- **[README.md](README.md)** - Descripción general del proyecto
- **[SETUP.md](SETUP.md)** - Configuración detallada
- **[ENDPOINTS.md](ENDPOINTS.md)** - Todos los endpoints con ejemplos
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitectura y flujos

---

## 🗂️ Estructura del Proyecto

```
TDV BACK/
│
├── 📄 Documentación
│   ├── README.md          - Descripción general
│   ├── QUICKSTART.md      - Inicio rápido
│   ├── SETUP.md           - Configuración
│   ├── ENDPOINTS.md       - API endpoints
│   ├── ARCHITECTURE.md    - Arquitectura
│   └── INDEX.md           - Este archivo
│
├── 🔧 Configuración
│   ├── .env.example       - Variables de ejemplo
│   ├── .gitignore         - Archivos a ignorar
│   ├── package.json       - Dependencias
│   └── server.js          - Servidor principal
│
├── 📁 config/
│   ├── db.js              - Conexión MongoDB
│   └── constants.js       - Constantes
│
├── 🗄️ models/             - Esquemas MongoDB
│   ├── User.js
│   ├── Entry.js
│   ├── Photo.js
│   ├── Content.js
│   ├── SacredSpace.js
│   └── Home.js
│
├── 🛣️ routes/              - Rutas de API
│   ├── auth.js
│   ├── home.js
│   ├── diary.js
│   ├── photos.js
│   ├── growth.js
│   ├── sacredSpace.js
│   ├── studio.js
│   └── users.js
│
├── 🎛️ controllers/         - Lógica de negocio
│   ├── authController.js
│   ├── homeController.js
│   ├── diaryController.js
│   ├── photoController.js
│   ├── growthController.js
│   ├── sacredSpaceController.js
│   └── userController.js
│
├── 🔐 middleware/          - Middlewares
│   └── auth.js            - Autenticación JWT
│
└── 📜 scripts/             - Scripts útiles
    └── seed.js            - Cargar datos iniciales
```

---

## ⚡ Guía Rápida por Tarea

### Quiero...

#### ...iniciar el servidor
```bash
npm run dev
# o
npm start
```
→ Ver [QUICKSTART.md](QUICKSTART.md)

#### ...crear un usuario
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -d '{"name":"...","email":"...","password":"..."}'
```
→ Ver [ENDPOINTS.md](ENDPOINTS.md#autenticación)

#### ...crear una entrada en Studio
```bash
curl -X POST http://localhost:5000/api/studio/entries \
  -H "Authorization: Bearer {token}" \
  -d '{"title":"...","content":"..."}'
```
→ Ver [ENDPOINTS.md](ENDPOINTS.md#studio)

#### ...ver el diario con estadísticas
```bash
curl -X GET http://localhost:5000/api/diary/stats \
  -H "Authorization: Bearer {token}"
```
→ Ver [ENDPOINTS.md](ENDPOINTS.md#diario)

#### ...entender la arquitectura
→ Ver [ARCHITECTURE.md](ARCHITECTURE.md)

#### ...desplegar a producción
→ Ver [SETUP.md](SETUP.md#-despliegue-en-producción)

#### ...resolver un error
→ Ver [SETUP.md](SETUP.md#-solución-de-problemas)

---

## 🌐 Endpoints por Sección

### Autenticación (`/api/auth`)
- `POST /register` - Registrar
- `POST /login` - Iniciar sesión
- `GET /validate` - Validar token

### Home (`/api/home`)
- `GET /` - Obtener datos
- `PUT /` - Actualizar (Admin)

### Diario (`/api/diary`)
- `GET /` - Obtener entradas
- `GET /stats` - Estadísticas
- `POST /` - Crear entrada
- `PUT /:id` - Actualizar
- `DELETE /:id` - Eliminar

### Fotos (`/api/photos`)
- `GET /` - Obtener fotos
- `POST /` - Crear foto
- `PUT /:id` - Actualizar
- `DELETE /:id` - Eliminar

### Crecimiento (`/api/growth`)
- `GET /` - Obtener contenidos
- `POST /` - Crear (Admin)
- `PUT /:id` - Actualizar (Admin)

### Espacio Sagrado (`/api/sacred-space`)
- `GET /` - Obtener espacios
- `POST /` - Crear (Admin)
- `PUT /:id` - Actualizar (Admin)

### Studio (`/api/studio`)
- `GET /entries` - Obtener
- `POST /entries` - Crear
- `PUT /entries/:id` - Actualizar
- `DELETE /entries/:id` - Eliminar

### Usuarios (`/api/users`)
- `GET /profile` - Mi perfil
- `PUT /profile` - Actualizar perfil
- `POST /change-password` - Cambiar contraseña
- `DELETE /account` - Eliminar cuenta

---

## 🧪 Testing

### Tools Recomendadas
- **Postman** - Colecciones de requests
- **Thunder Client** - Extensión VS Code
- **Curl** - Terminal
- **REST Client** - Extensión VS Code

### Primeras Pruebas
1. Health check: `GET http://localhost:5000/api/health`
2. Registrarse: `POST /api/auth/register`
3. Crear entrada: `POST /api/diary`
4. Ver diario: `GET /api/diary`

---

## 🚀 Flujo de Desarrollo

1. **Setup Inicial**
   - Seguir [QUICKSTART.md](QUICKSTART.md)
   - Instalar dependencias: `npm install`
   - Configurar `.env`
   - Iniciar MongoDB

2. **Desarrollo**
   - `npm run dev` para hot reload
   - Editar controllers, models, routes
   - Probar con Postman/Curl
   - Revisar logs en consola

3. **Testing**
   - Usar [ENDPOINTS.md](ENDPOINTS.md) como referencia
   - Probar cada endpoint
   - Verificar validaciones

4. **Despliegue**
   - Seguir [SETUP.md](SETUP.md#-despliegue-en-producción)
   - Usar MongoDB Atlas
   - Configurar variables de entorno

---

## 📋 Modelos de Datos

### User
- `_id`, `name`, `email`, `password` (hashed)
- `bio`, `profileImage`, `preferences`

### Entry (Diario)
- `userId`, `title`, `content`
- `type`, `energy`, `tags`, `images`
- `isPublic`, `createdAt`, `updatedAt`

### Photo
- `userId`, `url`, `title`, `description`
- `tags`, `energy`, `isPublic`

### Content (Growth)
- `title`, `description`, `category`
- `content`, `difficulty`, `duration`

### SacredSpace
- `title`, `description`, `content`
- `ambiance` (calm, energizing, grounding, balancing)

### Home
- `title`, `subtitle`, `description`
- `tagline`, `heroImage`

---

## 🔐 Autenticación

- **Sistema**: JWT (JSON Web Tokens)
- **Expiración**: 30 días
- **Headers**: `Authorization: Bearer {token}`
- **Password**: Hasheado con Bcrypt (10 rounds)

---

## 💾 Base de Datos

- **Sistema**: MongoDB
- **Opciones**:
  - Local: `mongodb://localhost:27017/manifestation-journal`
  - Cloud: MongoDB Atlas (recomendado)

---

## 🎯 Checklist de Implementación

- [x] Estructura base del servidor
- [x] Modelos de datos
- [x] Controladores
- [x] Rutas y endpoints
- [x] Autenticación JWT
- [x] Validación de datos
- [x] CORS y seguridad
- [x] Documentación completa
- [ ] Tests unitarios (TO DO)
- [ ] Integración con Frontend (TO DO)

---

## 📞 Soporte

Si encuentras problemas:

1. **Revisa los logs** - La consola mostrará mensajes útiles
2. **Consulta [SETUP.md](SETUP.md)** - Solución de problemas
3. **Verifica ENDPOINTS.md** - Ejemplos de uso
4. **Lee ARCHITECTURE.md** - Entiende cómo funciona

---

## 🎓 Aprender Más

### Tecnologías
- [Express.js](https://expressjs.com/)
- [MongoDB](https://docs.mongodb.com/)
- [Mongoose](https://mongoosejs.com/)
- [JWT](https://jwt.io/)

### Seguridad
- [OWASP](https://owasp.org/)
- [Helmet.js](https://helmetjs.github.io/)

---

## 📝 Última Actualización

- **Fecha**: Mayo 2024
- **Versión Backend**: 1.0.0
- **Stack**: Node.js + Express + MongoDB

---

## 🌟 Estado del Proyecto

✅ Backend completamente funcional y listo para usar
⏳ Integración con Frontend próximamente
🚀 Despliegue en producción disponible

---

**¡Gracias por usar Manifestation Journal Backend!** ✨

*Creado con pasión para ayudarte a manifestar tu realidad.*

# 📔 Manifestation Journal - Backend API

Backend de la aplicación **Manifestation Journal**, un diario digital enfocado en manifestación, rituales y crecimiento personal. Construido con Node.js, Express y MongoDB.

## 🌟 Características

- ✅ Autenticación con JWT
- ✅ Gestión de usuarios con perfiles
- ✅ Diario de entradas (manifestaciones, rituales, reflexiones)
- ✅ Galería de fotos (Photo Dump)
- ✅ Contenidos de crecimiento personal
- ✅ Espacios sagrados (meditación, inspiración)
- ✅ Página de inicio personalizable (Hero/Home)
- ✅ API RESTful completa
- ✅ CORS habilitado
- ✅ Validación de datos
- ✅ Seguridad con Helmet

## 🚀 Instalación

### Requisitos previos
- Node.js (v14+)
- MongoDB (local o Atlas)
- npm o yarn

### Pasos

1. **Clonar o abrir el proyecto**
   ```bash
   cd TDV\ BACK
   ```

2. **Instalar dependencias**
   ```bash
   npm install
   ```

3. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   ```
   Edita el archivo `.env` con tus valores:
   ```
   PORT=5000
   MONGODB_URI=mongodb://localhost:27017/manifestation-journal
   JWT_SECRET=tu_clave_secreta_aqui
   NODE_ENV=development
   ```

4. **Iniciar MongoDB**
   ```bash
   mongod
   ```

5. **Iniciar el servidor**
   - **Producción:**
     ```bash
     npm start
     ```
   - **Desarrollo (con hot reload):**
     ```bash
     npm run dev
     ```

El servidor estará disponible en `http://localhost:5000`

## 📚 Estructura del Proyecto

```
TDV BACK/
├── config/
│   └── db.js                    # Configuración de MongoDB
├── controllers/
│   ├── authController.js        # Lógica de autenticación
│   ├── homeController.js        # Sección Home/Hero
│   ├── diaryController.js       # Sección Diario
│   ├── photoController.js       # Photo Dump
│   ├── growthController.js      # Growth (crecimiento)
│   ├── sacredSpaceController.js # Sacred Space
│   └── userController.js        # Gestión de usuarios
├── middleware/
│   └── auth.js                  # Middleware de autenticación JWT
├── models/
│   ├── User.js                  # Modelo de Usuario
│   ├── Entry.js                 # Modelo de Entradas del diario
│   ├── Photo.js                 # Modelo de Fotos
│   ├── Content.js               # Modelo de Contenidos
│   ├── SacredSpace.js           # Modelo de Espacios Sagrados
│   └── Home.js                  # Modelo de Home
├── routes/
│   ├── auth.js                  # Rutas de autenticación
│   ├── home.js                  # Rutas Home
│   ├── diary.js                 # Rutas Diario
│   ├── photos.js                # Rutas Fotos
│   ├── growth.js                # Rutas Growth
│   ├── sacredSpace.js           # Rutas Sacred Space
│   ├── studio.js                # Rutas Studio (creación)
│   └── users.js                 # Rutas Usuarios
├── .env.example                 # Variables de entorno ejemplo
├── server.js                    # Archivo principal
├── package.json                 # Dependencias
└── README.md                    # Este archivo
```

## 🔐 Autenticación

El backend usa **JWT (JSON Web Tokens)** para autenticación.

### Flujo de autenticación:
1. Usuario se registra: `POST /api/auth/register`
2. Usuario inicia sesión: `POST /api/auth/login`
3. Se devuelve un token JWT
4. Incluir token en header: `Authorization: Bearer {token}`

## 📡 Endpoints Principales

### Autenticación (`/api/auth`)
- `POST /register` - Registrar nuevo usuario
- `POST /login` - Iniciar sesión
- `GET /validate` - Validar token (requiere autenticación)

### Home (`/api/home`)
- `GET /` - Obtener datos del Home
- `PUT /` - Actualizar datos del Home (Admin)

### Diario (`/api/diary`)
- `GET /` - Obtener todas las entradas
- `GET /stats` - Obtener estadísticas del diario
- `POST /` - Crear nueva entrada
- `GET /:id` - Obtener una entrada
- `PUT /:id` - Actualizar entrada
- `DELETE /:id` - Eliminar entrada

### Fotos (`/api/photos`)
- `GET /` - Obtener todas las fotos
- `POST /` - Crear nueva foto
- `GET /:id` - Obtener una foto
- `PUT /:id` - Actualizar foto
- `DELETE /:id` - Eliminar foto

### Crecimiento (`/api/growth`)
- `GET /` - Obtener contenidos
- `POST /` - Crear contenido (Admin)
- `GET /:id` - Obtener contenido
- `PUT /:id` - Actualizar contenido (Admin)
- `DELETE /:id` - Eliminar contenido (Admin)

### Espacio Sagrado (`/api/sacred-space`)
- `GET /` - Obtener espacios
- `POST /` - Crear espacio (Admin)
- `GET /:id` - Obtener espacio
- `PUT /:id` - Actualizar espacio (Admin)
- `DELETE /:id` - Eliminar espacio (Admin)

### Studio (`/api/studio`)
- `GET /entries` - Obtener entradas creadas
- `POST /entries` - Crear nueva entrada
- `GET /entries/:id` - Obtener entrada
- `PUT /entries/:id` - Actualizar entrada
- `DELETE /entries/:id` - Eliminar entrada

### Usuarios (`/api/users`)
- `GET /profile` - Obtener perfil (requiere auth)
- `PUT /profile` - Actualizar perfil (requiere auth)
- `POST /change-password` - Cambiar contraseña (requiere auth)
- `DELETE /account` - Eliminar cuenta (requiere auth)
- `GET /public/:id` - Obtener perfil público

## 📋 Ejemplos de Uso

### Registrarse
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"María","email":"maria@example.com","password":"123456"}'
```

### Iniciar sesión
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"maria@example.com","password":"123456"}'
```

### Crear entrada en Studio
```bash
curl -X POST http://localhost:5000/api/studio/entries \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"title":"Mi manifestación","content":"Hoy me propongo...","type":"manifestation","energy":"high"}'
```

### Obtener diario
```bash
curl -X GET http://localhost:5000/api/diary \
  -H "Authorization: Bearer {token}"
```

## 🧪 Testing

```bash
npm test
```

## 🔧 Tecnologías

- **Node.js** - Runtime de JavaScript
- **Express** - Framework web
- **MongoDB** - Base de datos NoSQL
- **Mongoose** - ODM para MongoDB
- **JWT** - Autenticación segura
- **Bcryptjs** - Hash de contraseñas
- **Helmet** - Seguridad HTTP
- **CORS** - Compartir recursos entre orígenes

## 🛡️ Seguridad

- Contraseñas hasheadas con bcrypt
- JWT para autenticación sin estado
- Validación de entrada con express-validator
- Headers de seguridad con Helmet
- CORS configurado

## 📝 Variables de Entorno

```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/manifestation-journal
JWT_SECRET=tu_clave_muy_secreta_aqui
NODE_ENV=development
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880
```

## 🚧 Roadmap

- [ ] Carga de imágenes
- [ ] Estadísticas avanzadas
- [ ] Búsqueda y filtros mejorados
- [ ] Recomendaciones personalizadas
- [ ] Sistema de notificaciones
- [ ] Integración con Google Calendar

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Añade mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## 📄 Licencia

MIT

## 📞 Soporte

Para reportar bugs o sugerencias, abre un issue en el repositorio.

---

**Creado con ✨ para manifestar realidades hermosas**

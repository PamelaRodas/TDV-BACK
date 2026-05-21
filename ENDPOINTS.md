# 📡 Guía de Endpoints - Manifestation Journal API

## Base URL
```
http://localhost:5000/api
```

## Headers comunes
```
Content-Type: application/json
Authorization: Bearer {token}  (requerido para endpoints autenticados)
```

---

## 🔐 AUTENTICACIÓN

### 1. Registrarse
```http
POST /auth/register
Content-Type: application/json

{
  "name": "María Rodas",
  "email": "maria@example.com",
  "password": "123456"
}
```

**Respuesta exitosa (201):**
```json
{
  "message": "User registered successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "María Rodas",
    "email": "maria@example.com"
  }
}
```

### 2. Iniciar sesión
```http
POST /auth/login
Content-Type: application/json

{
  "email": "maria@example.com",
  "password": "123456"
}
```

**Respuesta exitosa (200):**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "María Rodas",
    "email": "maria@example.com"
  }
}
```

### 3. Validar token
```http
GET /auth/validate
Authorization: Bearer {token}
```

**Respuesta exitosa (200):**
```json
{
  "valid": true,
  "user": {
    "userId": "507f1f77bcf86cd799439011"
  }
}
```

---

## 🏠 HOME (Hero/Bienvenida)

### 1. Obtener datos del Home
```http
GET /home
```

**Respuesta (200):**
```json
{
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "title": "Manifestation Journal",
    "subtitle": "Tu espacio para rituales, intenciones y crecimiento personal",
    "description": "Un diario sagrado donde tus intenciones cobran vida...",
    "tagline": "Manifiesta tu realidad, cultiva tu energía",
    "heroImage": null,
    "isActive": true,
    "createdAt": "2024-05-21T10:00:00.000Z"
  },
  "message": "Home data retrieved successfully"
}
```

### 2. Actualizar datos del Home (Admin)
```http
PUT /home
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "New Title",
  "subtitle": "New Subtitle",
  "tagline": "New Tagline"
}
```

---

## 📖 DIARIO (Diary)

### 1. Obtener todas las entradas
```http
GET /diary?page=1&limit=10&type=manifestation&energy=high
Authorization: Bearer {token}
```

**Parámetros query:**
- `page` (default: 1)
- `limit` (default: 10)
- `type`: manifestation, intention, ritual, reflection
- `energy`: high, medium, low

**Respuesta (200):**
```json
{
  "data": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "userId": "507f1f77bcf86cd799439012",
      "title": "Mi primera manifestación",
      "content": "Hoy me propongo...",
      "type": "manifestation",
      "energy": "high",
      "tags": ["dinero", "abundancia"],
      "images": [],
      "isPublic": false,
      "createdAt": "2024-05-21T10:00:00.000Z"
    }
  ],
  "pagination": {
    "total": 5,
    "page": 1,
    "limit": 10,
    "pages": 1
  },
  "message": "Entries retrieved successfully"
}
```

### 2. Obtener estadísticas del diario
```http
GET /diary/stats
Authorization: Bearer {token}
```

**Respuesta (200):**
```json
{
  "data": {
    "totalEntries": 12,
    "typeBreakdown": [
      { "_id": "manifestation", "count": 6 },
      { "_id": "ritual", "count": 4 },
      { "_id": "reflection", "count": 2 }
    ],
    "energyBreakdown": [
      { "_id": "high", "count": 5 },
      { "_id": "medium", "count": 4 },
      { "_id": "low", "count": 3 }
    ]
  },
  "message": "Diary statistics retrieved successfully"
}
```

### 3. Crear nueva entrada
```http
POST /diary
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Manifestación de hoy",
  "content": "Hoy me propongo atraer abundancia en todas sus formas...",
  "type": "manifestation",
  "energy": "high",
  "tags": ["abundancia", "dinero", "prosperidad"],
  "isPublic": false
}
```

**Respuesta (201):**
```json
{
  "message": "Entry created successfully",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "userId": "507f1f77bcf86cd799439012",
    "title": "Manifestación de hoy",
    "content": "Hoy me propongo...",
    "type": "manifestation",
    "energy": "high",
    "tags": ["abundancia", "dinero", "prosperidad"],
    "isPublic": false,
    "createdAt": "2024-05-21T10:00:00.000Z"
  }
}
```

### 4. Obtener una entrada específica
```http
GET /diary/{id}
Authorization: Bearer {token}
```

### 5. Actualizar entrada
```http
PUT /diary/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Título actualizado",
  "content": "Contenido actualizado...",
  "energy": "medium"
}
```

### 6. Eliminar entrada
```http
DELETE /diary/{id}
Authorization: Bearer {token}
```

**Respuesta (200):**
```json
{
  "message": "Entry deleted successfully"
}
```

---

## 📸 FOTOS (Photo Dump)

### 1. Obtener todas las fotos
```http
GET /photos?page=1&limit=12&energy=high
Authorization: Bearer {token}
```

### 2. Crear nueva foto
```http
POST /photos
Authorization: Bearer {token}
Content-Type: application/json

{
  "url": "https://example.com/photo.jpg",
  "title": "Momento de inspiración",
  "description": "Una foto que me inspira",
  "caption": "Belleza y energía",
  "tags": ["inspiración", "naturaleza"],
  "energy": "high",
  "isPublic": false
}
```

### 3. Actualizar foto
```http
PUT /photos/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Nuevo título",
  "caption": "Nueva descripción"
}
```

### 4. Eliminar foto
```http
DELETE /photos/{id}
Authorization: Bearer {token}
```

---

## 🌱 CRECIMIENTO (Growth)

### 1. Obtener contenidos de crecimiento
```http
GET /growth?page=1&limit=10&category=meditation&difficulty=beginner
```

**Parámetros:**
- `category`: ritual, habit, meditation, affirmation, practice
- `difficulty`: beginner, intermediate, advanced

### 2. Obtener contenido específico
```http
GET /growth/{id}
```

### 3. Crear contenido (Admin)
```http
POST /growth
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Meditación de la mañana",
  "description": "Comienza tu día con claridad",
  "category": "meditation",
  "content": "Siéntate en un lugar tranquilo...",
  "author": "Nombre del autor",
  "difficulty": "beginner",
  "duration": 10
}
```

---

## ✨ ESPACIO SAGRADO (Sacred Space)

### 1. Obtener espacios sagrados
```http
GET /sacred-space?page=1&limit=10&ambiance=calm
```

**Parámetros:**
- `ambiance`: calm, energizing, grounding, balancing

### 2. Obtener espacio específico
```http
GET /sacred-space/{id}
```

### 3. Crear espacio (Admin)
```http
POST /sacred-space
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Santuario de Calma",
  "description": "Un espacio para la tranquilidad",
  "content": "Imagina una habitación con luz dorada...",
  "ambiance": "calm"
}
```

---

## 🎨 STUDIO (Creación)

### 1. Obtener entradas del Studio
```http
GET /studio/entries
Authorization: Bearer {token}
```

### 2. Crear nueva entrada en Studio
```http
POST /studio/entries
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Nueva intención",
  "content": "Contenido creativo...",
  "type": "intention",
  "energy": "high"
}
```

### 3. Actualizar entrada del Studio
```http
PUT /studio/entries/{id}
Authorization: Bearer {token}
```

### 4. Eliminar entrada del Studio
```http
DELETE /studio/entries/{id}
Authorization: Bearer {token}
```

---

## 👤 USUARIOS (Users)

### 1. Obtener perfil del usuario
```http
GET /users/profile
Authorization: Bearer {token}
```

**Respuesta (200):**
```json
{
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "name": "María Rodas",
    "email": "maria@example.com",
    "bio": "Practicante de manifestación",
    "profileImage": "https://...",
    "preferences": {
      "language": "es",
      "theme": "light"
    },
    "createdAt": "2024-05-21T10:00:00.000Z"
  }
}
```

### 2. Actualizar perfil
```http
PUT /users/profile
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Nuevo Nombre",
  "bio": "Nueva biografía",
  "preferences": {
    "theme": "dark"
  }
}
```

### 3. Cambiar contraseña
```http
POST /users/change-password
Authorization: Bearer {token}
Content-Type: application/json

{
  "currentPassword": "123456",
  "newPassword": "newpassword123"
}
```

### 4. Eliminar cuenta
```http
DELETE /users/account
Authorization: Bearer {token}
Content-Type: application/json

{
  "password": "123456"
}
```

### 5. Obtener perfil público
```http
GET /users/public/{userId}
```

---

## ⚠️ Códigos de Error Comunes

| Código | Descripción |
|--------|------------|
| 200 | OK - Solicitud exitosa |
| 201 | Created - Recurso creado |
| 400 | Bad Request - Error en datos |
| 401 | Unauthorized - Token inválido/expirado |
| 403 | Forbidden - Acceso denegado |
| 404 | Not Found - Recurso no encontrado |
| 500 | Server Error - Error del servidor |

---

## 🧪 Testing con Postman

Puedes importar esta colección en Postman o usar herramientas como `curl` o `Thunder Client`.

**Flujo típico:**
1. `POST /auth/register` - Registrarse
2. Copiar el token de la respuesta
3. Usar el token en `Authorization: Bearer {token}`
4. Crear entradas, fotos, etc.

---

**Última actualización:** Mayo 2024

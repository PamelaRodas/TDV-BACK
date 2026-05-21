# 🏗️ ARQUITECTURA - Manifestation Journal

## Diagrama General

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React/Vue)                          │
│              En: TDV FRONT/TVD                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↕
                    HTTP/REST API (CORS)
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (Node.js/Express)                     │
│              En: TDV BACK (Este proyecto)                        │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    Base de Datos (MongoDB)                       │
│         Local o MongoDB Atlas en la nube                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Flujo de Autenticación

```
┌──────────────┐
│   Usuario    │
└──────────────┘
       │
       ├─→ POST /api/auth/register
       │      ↓
       │   [Validar datos]
       │      ↓
       │   [Hash contraseña]
       │      ↓
       │   [Guardar en BD]
       │      ↓
       │   [Generar JWT]
       │      ↓
       └─← {token, user}
              │
              ├─→ POST /api/auth/login
              │      ↓
              │   [Validar email/contraseña]
              │      ↓
              │   [Generar JWT]
              │      ↓
              └─← {token, user}
                     │
                     ├─→ Guardar token localmente (Frontend)
                     │
                     └─→ Incluir en header: Authorization: Bearer {token}
```

---

## Flujo de Creación de Entrada (Studio)

```
┌──────────────────────────────────────────────────────────────┐
│ Usuario escribe en Studio (Frontend)                         │
└──────────────────────────────────────────────────────────────┘
       │
       └─→ POST /api/studio/entries
           Header: Authorization: Bearer {token}
           Body: {title, content, type, energy, tags}
              │
              ↓
         ┌─────────────────────────────────┐
         │  Middleware: authenticateToken   │
         │  Verificar JWT válido            │
         └─────────────────────────────────┘
              │
              ├─ ✅ Token válido
              │      ↓
              │  Ejecutar Controller
              │      ↓
              │  ┌──────────────────────────┐
              │  │ Validar datos            │
              │  │ Crear objeto Entry       │
              │  │ Guardar en MongoDB       │
              │  └──────────────────────────┘
              │      ↓
              │  Response 201: {message, data}
              │      ↓
              └─← Frontend actualiza UI
              │
              ├─ ❌ Token inválido/expirado
              │      ↓
              └─← Response 401/403: {error}
                     ↓
                  Frontend redirige a Login
```

---

## Estructura de Datos (Modelos)

### User
```
{
  _id: ObjectId
  name: String
  email: String (único)
  password: String (hashed)
  bio: String
  profileImage: URL
  preferences: {
    language: String
    theme: 'light' | 'dark'
  }
  createdAt: Date
  updatedAt: Date
}
```

### Entry (Diario)
```
{
  _id: ObjectId
  userId: ObjectId (ref: User)
  title: String
  content: String
  type: 'manifestation' | 'intention' | 'ritual' | 'reflection'
  energy: 'high' | 'medium' | 'low'
  tags: [String]
  images: [URL]
  isPublic: Boolean
  createdAt: Date
  updatedAt: Date
}
```

### Photo
```
{
  _id: ObjectId
  userId: ObjectId (ref: User)
  url: URL (imagen)
  title: String
  description: String
  caption: String
  tags: [String]
  energy: 'high' | 'medium' | 'low'
  isPublic: Boolean
  createdAt: Date
}
```

### Content (Growth)
```
{
  _id: ObjectId
  title: String
  description: String
  category: 'ritual' | 'habit' | 'meditation' | 'affirmation' | 'practice'
  content: String
  image: URL
  author: String
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  duration: Number (minutos)
  isActive: Boolean
  createdAt: Date
}
```

### SacredSpace
```
{
  _id: ObjectId
  title: String
  description: String
  content: String
  image: URL
  ambiance: 'calm' | 'energizing' | 'grounding' | 'balancing'
  isActive: Boolean
  createdAt: Date
}
```

### Home
```
{
  _id: ObjectId
  title: String
  subtitle: String
  description: String
  heroImage: URL
  tagline: String
  isActive: Boolean
  createdAt: Date
}
```

---

## Stack Tecnológico

```
┌─────────────────────────────────────────────────┐
│ Node.js v14+                                     │
│ ├─ Express 4.18 (Framework web)                │
│ ├─ MongoDB (Base de datos)                     │
│ ├─ Mongoose 7.0 (ODM)                          │
│ ├─ JWT (Autenticación)                         │
│ ├─ Bcrypt (Hash de contraseñas)                │
│ ├─ Helmet (Seguridad)                          │
│ ├─ CORS (Compartir recursos)                   │
│ └─ express-validator (Validación)              │
└─────────────────────────────────────────────────┘
```

---

## Ciclo de Vida de una Solicitud

```
1. Cliente envía request con auth token
   ↓
2. Express recibe y parsea JSON
   ↓
3. Helmet añade headers de seguridad
   ↓
4. CORS verifica origen permitido
   ↓
5. Router identifica ruta
   ↓
6. Middleware de autenticación verifica JWT
   ↓
7. Controller valida datos
   ↓
8. Interacción con MongoDB
   ↓
9. Generar respuesta JSON
   ↓
10. Enviar al cliente
```

---

## Flujo de Acceso a Datos

```
Frontend (React)
     ↓
  HTTP Request
     ↓
Express Router
     ↓
Middleware (Auth)
     ↓
Controller (Lógica)
     ↓
Mongoose (ODM)
     ↓
MongoDB (BD)
     ↓
Respuesta JSON
     ↓
Frontend (actualizar UI)
```

---

## Seguridad

```
┌─────────────────────────────────────┐
│ Capas de Seguridad                  │
├─────────────────────────────────────┤
│ 1. HTTPS en producción              │
│ 2. JWT con expiración               │
│ 3. Bcrypt para contraseñas          │
│ 4. Validación de entrada            │
│ 5. CORS whitelist                   │
│ 6. Helmet headers de seguridad      │
│ 7. Control de acceso (userId)       │
│ 8. Variables de entorno secretas    │
└─────────────────────────────────────┘
```

---

## Escalabilidad

### Horizontal
- Usar load balancer (Nginx)
- Múltiples instancias del backend
- Session store en Redis

### Vertical
- Índices en MongoDB
- Caché con Redis
- CDN para imágenes

---

## Despliegue

```
Desarrollo (Local)
├─ npm run dev
└─ MongoDB local

Staging
├─ npm start (Node.js)
├─ MongoDB Atlas
└─ URL: staging-api.example.com

Producción
├─ npm start (PM2/Docker)
├─ MongoDB Atlas
├─ CDN para imágenes
├─ Backup automático
└─ URL: api.manifestationjournal.com
```

---

## Monitoreo

```
Logs
├─ Console.log en desarrollo
├─ Archivo de logs en producción
└─ Servicios: New Relic, DataDog

Errores
├─ Email notifications
├─ Error tracking (Sentry)
└─ Status page

Performance
├─ Response time
├─ Database queries
└─ API usage metrics
```

---

**Arquitectura completa y lista para escalar.** 🚀

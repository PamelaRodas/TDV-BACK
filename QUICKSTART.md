# 🎯 GUÍA RÁPIDA - Backend Manifestation Journal

## ⚡ Inicio Rápido (5 minutos)

### 1️⃣ Clonar/Abrir el proyecto
```bash
cd "c:\Users\familia Rodas\OneDrive\Escritorio\DOCUMENTOS COSMOS\Nueva carpeta\PAMELA\TDV BACK"
```

### 2️⃣ Instalar dependencias
```bash
npm install
```

### 3️⃣ Configurar entorno
Copiar `.env.example` a `.env` y editar si es necesario.

### 4️⃣ Iniciar MongoDB
```bash
mongod
```

### 5️⃣ Ejecutar servidor
```bash
npm run dev
```

✅ Servidor corriendo en `http://localhost:5000`

---

## 📋 Comandos Útiles

```bash
# Desarrollo con hot reload
npm run dev

# Producción
npm start

# Cargar datos iniciales
npm run seed

# Ejecutar tests
npm test
```

---

## 🌐 Primeras Pruebas

### Verificar servidor
```bash
curl http://localhost:5000/api/health
```

### Registrarse
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tu Nombre",
    "email": "tu@email.com",
    "password": "123456"
  }'
```

### Crear entrada en Studio
```bash
curl -X POST http://localhost:5000/api/studio/entries \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi manifestación",
    "content": "Hoy me propongo...",
    "type": "manifestation",
    "energy": "high"
  }'
```

---

## 📁 Estructura Importante

```
TDV BACK/
├── server.js                # Punto de entrada
├── package.json             # Dependencias
├── .env.example             # Configuración (copiar a .env)
├── config/
│   ├── db.js               # Conexión MongoDB
│   └── constants.js        # Constantes
├── models/                 # Esquemas MongoDB
├── routes/                 # Rutas de API
├── controllers/            # Lógica de negocio
├── middleware/             # Autenticación JWT
├── scripts/
│   └── seed.js            # Datos iniciales
├── README.md              # Documentación
├── ENDPOINTS.md           # Guía de endpoints
├── SETUP.md               # Configuración
└── QUICKSTART.md          # Este archivo
```

---

## 🔑 Tokens JWT

1. Registrarse/Loguearse → Recibir `token`
2. Guardar el token
3. En cada request autenticado, incluir:
   ```
   Authorization: Bearer {token}
   ```

El token expira en **30 días**.

---

## 🛣️ Rutas Principales

| Método | Ruta | Auth | Descripción |
|--------|------|------|------------|
| POST | `/api/auth/register` | ❌ | Registrarse |
| POST | `/api/auth/login` | ❌ | Iniciar sesión |
| GET | `/api/home` | ❌ | Ver Home |
| GET | `/api/diary` | ✅ | Ver diario |
| POST | `/api/diary` | ✅ | Crear entrada |
| GET | `/api/photos` | ✅ | Ver fotos |
| POST | `/api/photos` | ✅ | Añadir foto |
| GET | `/api/growth` | ❌ | Ver contenidos |
| GET | `/api/sacred-space` | ❌ | Ver espacios |
| GET/POST | `/api/studio/entries` | ✅ | Studio |
| GET | `/api/users/profile` | ✅ | Mi perfil |

---

## 🧪 Herramientas de Testing

### Opción 1: Postman
1. Importar endpoints de `ENDPOINTS.md`
2. Usar colección para probar

### Opción 2: Thunder Client (VS Code)
1. Instalar extensión "Thunder Client"
2. Crear requests manualmente

### Opción 3: Curl (terminal)
```bash
curl -X GET http://localhost:5000/api/health
```

### Opción 4: REST Client (VS Code)
1. Instalar "REST Client"
2. Crear archivo `.http` con requests

---

## ⚠️ Errores Comunes

| Error | Solución |
|-------|----------|
| "Cannot connect to MongoDB" | Verificar `mongod` corriendo |
| "Connection refused on port 5000" | Cambiar PORT en `.env` |
| "token required" | Incluir header `Authorization: Bearer {token}` |
| "Invalid credentials" | Verificar email/contraseña |

---

## 📖 Documentación Completa

- **README.md** - Descripción general
- **ENDPOINTS.md** - Todos los endpoints con ejemplos
- **SETUP.md** - Configuración detallada
- **QUICKSTART.md** - Este archivo

---

## 🚀 Próximos Pasos

1. ✅ Backend corriendo
2. ⏳ Conectar con Frontend en `TDV FRONT`
3. ⏳ Configurar CORS
4. ⏳ Desplegar en producción

---

## 💡 Tips

- Lee los comentarios en los controladores
- Consulta `ENDPOINTS.md` para ejemplos completos
- Usa Postman para probar endpoints
- Revisa logs en la consola para debugging
- `.env` nunca debe commitirse a Git

---

**¿Preguntas? Revisa la documentación o verifica los logs del servidor.** 🌟

# 🔧 GUÍA DE CONFIGURACIÓN DEL BACKEND

## Configuración Local

### 1. Base de datos (MongoDB)

**Opción A: MongoDB Local**
```bash
# Instalar MongoDB desde: https://www.mongodb.com/try/download/community
# Iniciar MongoDB
mongod
```

**Opción B: MongoDB Atlas (Cloud)**
1. Ir a https://www.mongodb.com/cloud/atlas
2. Crear cuenta gratuita
3. Crear cluster
4. Generar connection string
5. Usar en `.env`:
```
MONGODB_URI=mongodb+srv://usuario:contraseña@cluster.mongodb.net/manifestation-journal?retryWrites=true&w=majority
```

### 2. Variables de Entorno (.env)

Copiar `.env.example` a `.env` y configurar:

```env
# Puerto
PORT=5000

# MongoDB
MONGODB_URI=mongodb://localhost:27017/manifestation-journal
# O para Atlas:
# MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/manifestation-journal

# JWT Secret - CAMBIAR EN PRODUCCIÓN
JWT_SECRET=tu_clave_muy_secreta_aqui_cambiala

# Entorno
NODE_ENV=development

# Almacenamiento
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880
```

### 3. Instalación de Dependencias

```bash
npm install
```

### 4. (Opcional) Cargar datos iniciales

```bash
npm run seed
```

Este comando crea:
- Datos de Home
- Contenidos de Growth (meditaciones, rituales, etc.)
- Espacios Sagrados

### 5. Iniciar el servidor

**Desarrollo (con hot reload):**
```bash
npm run dev
```

**Producción:**
```bash
npm start
```

El servidor estará en: `http://localhost:5000`

Verificar con:
```bash
curl http://localhost:5000/api/health
```

---

## 🚀 Despliegue en Producción

### Heroku

1. Crear app en Heroku
2. Conectar repositorio Git
3. Añadir variables de entorno:
```
PORT=5000
NODE_ENV=production
JWT_SECRET=clave_super_secreta
MONGODB_URI=mongodb+srv://...
```
4. Desplegar

### Railway / Render

Seguir documentación similar.

---

## 🔑 Seguridad

- ✅ Cambiar `JWT_SECRET` en producción
- ✅ Usar HTTPS en producción
- ✅ Configurar CORS apropiadamente
- ✅ Variables de entorno no en versión control
- ✅ Usar MongoDB Atlas con contraseñas seguras

---

## 📚 Verificación del Setup

1. **MongoDB conectado:**
   ```
   La consola debe mostrar: "✅ MongoDB Connected"
   ```

2. **Servidor corriendo:**
   ```
   La consola debe mostrar: "✨ Manifestation Journal Backend running on port 5000"
   ```

3. **Health check:**
   ```bash
   curl http://localhost:5000/api/health
   ```
   Debe retornar JSON con status OK.

---

## 🐛 Solución de Problemas

### "Connection refused" en MongoDB
- Verificar que MongoDB está corriendo
- Verificar connection string en `.env`

### "Cannot find module"
- Ejecutar `npm install`
- Verificar que los archivos están en el lugar correcto

### Puerto 5000 en uso
- Cambiar PORT en `.env`
- O liberar el puerto

---

**¡Setup completado! Listo para desarrollar.** ✨

# 🔧 GUÍA DE CONFIGURACIÓN COMPLETA - TDV Backend & Analytics

## 📋 Requisitos del Sistema

### Requerimientos Previos
- **Node.js** v14+ 
- **Python** 3.8+
- **npm** o **yarn**
- **pip** (gestor de paquetes Python)
- **MongoDB** (opcional - funciona en demo mode sin él)

### Verificar Instalación

```bash
# Node.js
node --version
npm --version

# Python
python --version
pip --version
```

---

## 🚀 Instalación Completa

### PASO 1: Instalar Dependencias Node.js

```bash
# Navegar al directorio
cd TDV-BACK

# Instalar dependencias (incluye axios para integración Python)
npm install
```

Verifica que se instaló:
```bash
npm list --depth=0
```

### PASO 2: Instalar Dependencias Python

```bash
# Ir a módulo Python
cd python-analytics

# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
pip list | grep pandas  # Debe mostrar pandas
```

---

## 🔑 Configuración de Variables de Entorno

### 1. Backend Node.js (.env)

```bash
# Ir al directorio raíz
cd TDV-BACK

# Crear archivo .env
cp .env.example .env
```

**Contenido de .env:**
```env
# Servidor
PORT=5000
NODE_ENV=development

# Base de Datos MongoDB (opcional)
MONGODB_URI=mongodb://localhost:27017/manifestation-journal

# JWT
JWT_SECRET=tu_clave_muy_secreta_aqui_cambiar_en_produccion

# Almacenamiento
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880

# Integración con API Python
PYTHON_API_URL=http://localhost:8000
```

### 2. API Python (opcional - configure en archivo)

### 2. API Python (opcional - configure en archivo)

Los parámetros de la API Python se configuran en `api.py`:
```python
PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8000'
```

### Opción B: MongoDB Atlas (Cloud) - Recomendado

```env
MONGODB_URI=mongodb+srv://usuario:contraseña@cluster.mongodb.net/manifestation-journal?retryWrites=true&w=majority
```

### Opción C: Demo Mode (Sin Base de Datos)

Si dejas `MONGODB_URI` en blanco o con localhost sin MongoDB ejecutándose, 
el backend usará **Demo Mode**:
```
🎮 Mode: DEMO (without persistent database)
```

---

## ▶️ INICIANDO LOS SERVICIOS

### Opción 1: Terminales Separadas (Recomendado)

**Terminal 1 - API Python:**
```bash
cd python-analytics
venv\Scripts\activate
python -m uvicorn api:app --reload --port 8000
```

**Terminal 2 - Backend Node.js:**
```bash
cd TDV-BACK
npm run dev
```

### Opción 2: Procesos en Segundo Plano (Windows)

```bash
# En PowerShell
# Terminal 1
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m", "uvicorn", "api:app", "--reload", "--port", "8000"

# Terminal 2
npm run dev
```

---

## ✅ VERIFICACIÓN

### 1. API Python

```bash
# Debe responder en segundos
curl http://localhost:8000/health

# Documentación Swagger:
# Abre en navegador: http://localhost:8000/docs
```

### 2. Backend Node.js

```bash
# Debe responder en segundos
curl http://localhost:5000/api/health
```

### 3. Integración Completa

```bash
# Verifica que Python está disponible desde Node.js
curl http://localhost:5000/api/analytics/health
```

---

## 📊 TESTING RÁPIDO

```bash
# Crear archivo con datos de ejemplo
cat > test_data.json << 'EOF'
{
  "registros": [
    {"categoria": "A", "valor": 10, "fecha": "2024-01-01"},
    {"categoria": "B", "valor": 20, "fecha": "2024-01-02"}
  ]
}
EOF

# Analizar datos
curl -X POST http://localhost:5000/api/analytics/analizar \
  -H "Content-Type: application/json" \
  -d @test_data.json
```

---

## 🧪 EJECUTAR EJEMPLOS

```bash
# Ve a módulo Python
cd python-analytics

# Activa venv si no está activado
venv\Scripts\activate

# Ejecuta ejemplos
python ejemplo.py
```

---

## 📁 ESTRUCTURA DE DIRECTORIOS

Después de la configuración, deberías tener:

```
TDV-BACK/
├── node_modules/        # Dependencias Node.js
├── python-analytics/
│   ├── venv/           # Entorno virtual Python
│   ├── reportes/       # Gráficos generados
│   ├── *.py            # Módulos Python
│   └── requirements.txt
├── .env                 # Variables de entorno (GITIGNORE)
├── package.json
└── server.js
```

---

## 🔧 TROUBLESHOOTING

### Puerto 8000/5000 ocupado

```bash
# Windows - Encontrar proceso
netstat -ano | findstr :8000

# Terminar proceso
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### ModuleNotFoundError en Python

```bash
cd python-analytics
pip install -r requirements.txt
```

### CORS Error

Verifica que:
- Backend en `http://localhost:5000`
- API Python en `http://localhost:8000`
- Variable `PYTHON_API_URL=http://localhost:8000` en .env

### venv no se activa

```bash
# Recrear venv
cd python-analytics
Remove-Item -Recurse venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🎯 PRÓXIMOS PASOS

1. **Ir a [QUICKSTART.md](QUICKSTART.md)** para guía rápida de inicio
2. **Ir a [GITFLOW.md](GITFLOW.md)** para crear Pull Request
3. **Ir a [REACT_INTEGRATION.md](REACT_INTEGRATION.md)** para integrar con React
4. **Consulta [ENTREGABLES.md](ENTREGABLES.md)** para lista completa

---

## 📚 DOCUMENTACIÓN

- **README.md** - Documentación general
- **ARCHITECTURE.md** - Arquitectura del sistema
- **ENDPOINTS.md** - Todos los endpoints
- **python-analytics/README.md** - Documentación módulo Python
- **REACT_INTEGRATION.md** - Guía de integración React

---

## ✨ ¡Listo para Desarrollar!

Si todo funciona correctamente, tienes un sistema completo:
- ✅ Backend Node.js
- ✅ API Python
- ✅ Análisis de datos
- ✅ Gráficos en Base64
- ✅ Integración completa

**¡Ahora integra con React y despliega!** 🚀

---

## 💾 Configuración de Base de Datos

### Opción A: MongoDB Local (Demo Mode Deshabilitado)

```bash
# Descargar MongoDB Community
# https://www.mongodb.com/try/download/community

# Iniciar MongoDB
mongod
```

Luego en `.env`:
```env
MONGODB_URI=mongodb://localhost:27017/manifestation-journal
```

### Opción B: MongoDB Atlas (Cloud) - Recomendado

1. Ir a https://www.mongodb.com/cloud/atlas
2. Crear cuenta gratuita
3. Crear cluster
4. Obtener connection string
5. En `.env`:
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

# 🚀 Instrucciones de Ejecución Completas
## Manifestation Journal - Backend con Análisis Visual

**Última actualización**: 23 de Mayo de 2026  
**Versión**: 1.0.0  

---

## 📋 Requisitos Previos

Asegurar que tienes instalado:
- **Node.js** v14+ ([descargar](https://nodejs.org/))
- **Python** 3.8+ ([descargar](https://www.python.org/))
- **MongoDB** (local o [Atlas Cloud](https://www.mongodb.com/cloud/atlas))
- **Git** ([descargar](https://git-scm.com/))

### Verificar instalación:
```bash
node --version      # Debe mostrar v14+
npm --version       # Debe mostrar 6+
python --version    # Debe mostrar 3.8+
git --version       # Debe mostrar 2.30+
```

---

## 🔧 Instalación Paso a Paso

### **PASO 1: Clonar o abrir el repositorio**

```bash
# Si es nuevo
git clone <tu-repositorio> TDV-BACK
cd TDV-BACK

# Si ya tienes el repositorio
cd "ruta/a/TDV-BACK"
```

### **PASO 2: Configurar variables de entorno**

Crear archivo `.env` en la raíz del proyecto:

```bash
# Opción A: Copiar desde template
cp .env.example .env

# Opción B: Crear manualmente
cat > .env << EOF
PORT=5000
MONGODB_URI=mongodb://localhost:27017/manifestation-journal
JWT_SECRET=tu_clave_super_secreta_aqui_cambiar_en_produccion
NODE_ENV=development
PYTHON_API_URL=http://localhost:8000
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880
EOF
```

**Importante**: Editar `.env` con tus valores reales.

### **PASO 3: Instalar dependencias Node.js**

```bash
npm install
```

Verificar que se instaló `axios`:
```bash
npm list axios
```

### **PASO 4: Configurar y instalar módulo Python**

#### A. Crear entorno virtual

**Windows:**
```bash
cd python-analytics
python -m venv venv
venv\Scripts\activate
cd ..
```

**Linux/Mac:**
```bash
cd python-analytics
python3 -m venv venv
source venv/bin/activate
cd ..
```

Verificar que está activado (debe aparecer `(venv)` en el terminal).

#### B. Instalar dependencias Python

```bash
# Asegurar que estás en python-analytics
cd python-analytics

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

Deberías ver:
- pandas>=2.2.0
- matplotlib>=3.8.0
- seaborn>=0.13.0
- fastapi>=0.109.0
- uvicorn>=0.27.0

```bash
# Volver a la raíz
cd ..
```

---

## 🏃 Ejecutar la Aplicación

### **Escenario A: Ejecución Local (Desarrollo)**

Abrir **4 terminales** diferentes:

#### Terminal 1: Base de Datos MongoDB

```bash
# Windows
mongod

# O si usas MongoDB Atlas, configura MONGODB_URI en .env
```

#### Terminal 2: Backend Node.js

```bash
# Asegurar que el entorno virtual de Python NO está activado
npm run dev
```

Esperado:
```
✅ Backend running on http://localhost:5000
✅ MongoDB connected (o Demo mode)
```

#### Terminal 3: API Python

```bash
# Activar entorno virtual primero
cd python-analytics

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Iniciar la API
python -m uvicorn api:app --reload --port 8000
```

Esperado:
```
✅ Uvicorn running on http://127.0.0.1:8000
✅ API docs: http://localhost:8000/docs
```

#### Terminal 4: Ejecutar ejemplos (Opcional)

```bash
cd python-analytics

# Activar entorno virtual
# (Windows) venv\Scripts\activate
# (Linux/Mac) source venv/bin/activate

# Ejecutar ejemplos
python ejemplo.py
```

---

### **Escenario B: Ejecución en Producción**

```bash
# Backend Node.js (sin hot reload)
npm start

# En otra terminal - API Python
cd python-analytics
source venv/bin/activate  # o venv\Scripts\activate en Windows
python -m uvicorn api:app --port 8000
```

---

## ✅ Verificar que Todo Funciona

### 1️⃣ Verificar Backend Node.js

```bash
curl http://localhost:5000/api/health
```

Respuesta esperada:
```json
{
  "status": "Backend running successfully",
  "timestamp": "2026-05-23T...",
  "database": "connected" // o "demo-mode"
}
```

### 2️⃣ Verificar API Python

```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "API running",
  "timestamp": "2026-05-23T..."
}
```

### 3️⃣ Probar Endpoint de Análisis

```bash
curl -X POST http://localhost:5000/api/analytics/analizar \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [
      {"categoria": "A", "valor": 10},
      {"categoria": "B", "valor": 20},
      {"categoria": "C", "valor": 15}
    ]
  }'
```

Respuesta esperada:
```json
{
  "success": true,
  "data": {
    "total_registros": 3,
    "estadisticas": {...}
  }
}
```

### 4️⃣ Generar Gráfico

```bash
curl -X POST http://localhost:5000/api/analytics/graficar \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [
      {"categoria": "Manifestación", "valor": 10},
      {"categoria": "Gratitud", "valor": 20},
      {"categoria": "Meditación", "valor": 15}
    ],
    "tipo": "frecuencia",
    "columna": "categoria"
  }'
```

Respuesta esperada:
```json
{
  "success": true,
  "grafico": {
    "tipo": "barras",
    "imagen_base64": "iVBORw0KGgoAAAANSUh...",
    "descripcion": "..."
  }
}
```

---

## 📡 API Endpoints Principales

### Análisis Visual (`/api/analytics`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/analizar` | Análisis estadístico de datos |
| POST | `/graficar` | Generar gráfico específico |
| POST | `/reporte` | Reporte completo con gráficos |
| POST | `/cargar-csv` | Cargar archivo CSV |
| POST | `/outliers` | Detectar valores atípicos |
| POST | `/tendencias` | Analizar tendencias temporales |
| POST | `/columnas-info` | Info detallada de columnas |
| GET | `/health` | Health check |

### Autenticación (`/api/auth`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/register` | Registrar usuario |
| POST | `/login` | Iniciar sesión |
| GET | `/validate` | Validar token |

### Diario (`/api/diary`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Obtener entradas |
| POST | `/` | Crear entrada |
| GET | `/:id` | Obtener entrada |
| PUT | `/:id` | Actualizar entrada |
| DELETE | `/:id` | Eliminar entrada |

---

## 🧪 Testing

### Ejecutar tests Node.js

```bash
npm test
```

### Ejecutar ejemplos Python

```bash
cd python-analytics

# Activar venv
# (Windows) venv\Scripts\activate
# (Linux/Mac) source venv/bin/activate

python ejemplo.py
```

---

## 📚 Documentación de la API

### FastAPI Docs (Interactivo)

```
http://localhost:8000/docs
```

Aquí puedes:
- Ver todos los endpoints
- Probar endpoints directamente
- Ver esquemas de entrada/salida

### OpenAPI JSON

```
http://localhost:8000/openapi.json
```

---

## 🔧 Solución de Problemas

### Error: "No module named 'fastapi'"

```bash
# Asegurar que estás en el venv
cd python-analytics

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Instalar de nuevo
pip install -r requirements.txt
```

### Error: "EADDRINUSE :::5000"

El puerto 5000 ya está en uso.

```bash
# Encontrar proceso usando puerto 5000
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000

# Matar proceso (con PID del resultado anterior)
# Windows
taskkill /PID <PID> /F

# Linux/Mac
kill -9 <PID>
```

### Error: "MongoDB connection failed"

Opciones:
1. Iniciar MongoDB local: `mongod`
2. Usar MongoDB Atlas (actualizar `MONGODB_URI` en `.env`)
3. La app funciona en modo demo aunque MongoDB falle

### Error: "Python API not responding"

```bash
# Verificar que Python API está corriendo
curl http://localhost:8000/health

# Si no responde, iniciar en otra terminal
cd python-analytics
venv\Scripts\activate  # o source venv/bin/activate
python -m uvicorn api:app --reload --port 8000
```

---

## 📁 Estructura del Proyecto

```
TDV-BACK/
├── python-analytics/           # 🆕 Módulo de análisis
│   ├── analisis.py            # Análisis estadístico
│   ├── visualizacion.py       # Generación de gráficos
│   ├── reporte.py             # Generador de reportes
│   ├── api.py                 # API FastAPI
│   ├── ejemplo.py             # Ejemplos ejecutables
│   ├── requirements.txt       # Dependencias Python
│   ├── README.md              # Documentación
│   ├── venv/                  # Entorno virtual
│   └── reportes/              # Gráficos generados
│
├── routes/                    # Rutas Express
│   ├── analytics.js          # 🆕 Proxy a API Python
│   ├── auth.js
│   ├── diary.js
│   └── ...
│
├── controllers/              # Controladores
├── models/                   # Modelos MongoDB
├── middleware/               # Middleware
│
├── .env                      # Variables de entorno
├── .env.example              # Template de .env
├── server.js                 # Punto de entrada
├── package.json              # Dependencias Node.js
├── README.md                 # Documentación principal
├── ENTREGABLES.md            # Entrega - Momento 3
├── GITFLOW.md                # Flujo de ramas
├── REACT_INTEGRATION.md      # Integración React
├── INSTRUCCIONES_EJECUCION.md # Este archivo
└── TEST_ENTREGA.md           # Verificación de entrega
```

---

## 🚀 Próximos Pasos

1. **Crear rama feature**:
   ```bash
   git checkout -b feature/reporte-visual
   ```

2. **Hacer cambios y commits**:
   ```bash
   git add .
   git commit -m "feat: Análisis visual completado"
   ```

3. **Empujar rama**:
   ```bash
   git push origin feature/reporte-visual
   ```

4. **Crear Pull Request** a `develop`

---

## 🎓 Ejemplos de Uso Completo

### Ejemplo 1: Registrarse y crear entrada

```bash
# 1. Registrarse
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "María",
    "email": "maria@example.com",
    "password": "123456"
  }'

# Copiar el token devuelto
TOKEN="eyJhbGc..."

# 2. Crear entrada de diario
curl -X POST http://localhost:5000/api/diary \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi Manifestación",
    "content": "Hoy me propongo atraer prosperidad",
    "type": "manifestation",
    "category": "Manifestación"
  }'

# 3. Obtener entradas
curl -X GET http://localhost:5000/api/diary \
  -H "Authorization: Bearer $TOKEN"

# 4. Analizar entradas
curl -X POST http://localhost:5000/api/analytics/reporte \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [
      {"categoria": "Manifestación", "puntuacion": 8},
      {"categoria": "Gratitud", "puntuacion": 9}
    ],
    "titulo": "Mi Análisis"
  }'
```

---

## 📞 Soporte

Para problemas o preguntas:

1. **Ver documentación**:
   - `README.md` - Descripción general
   - `python-analytics/README.md` - Detalles del módulo
   - `REACT_INTEGRATION.md` - Integración frontend

2. **Ver ejemplos**:
   - `python-analytics/ejemplo.py` - Ejemplos Python
   - `TEST_ENTREGA.md` - Ejemplos de API

3. **Documentación interactiva**:
   - http://localhost:8000/docs - FastAPI
   - http://localhost:5000/api/health - Backend

---

## ✅ Checklist Final

Antes de considerar completada la instalación:

- [ ] Node.js instalado y funcionando
- [ ] Python 3.8+ instalado
- [ ] Repositorio clonado
- [ ] `.env` configurado
- [ ] `npm install` completado
- [ ] Entorno virtual Python creado
- [ ] `pip install -r requirements.txt` completado
- [ ] MongoDB corriendo (o usando Atlas)
- [ ] Backend Node.js inicia sin errores
- [ ] API Python inicia sin errores
- [ ] `http://localhost:5000/api/health` responde
- [ ] `http://localhost:8000/health` responde
- [ ] Endpoint de analytics responde con datos

¡Si todo está ✅, estás listo para usar la aplicación!

---

**Creado con ✨ para manifestar realidades hermosas**

# ⚡ Quick Start - Inicia en 5 minutos

## 🏃 Ejecución Rápida

### 1️⃣ Instalar (3 comandos)
```bash
npm install
cd python-analytics && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && cd ..
```

### 2️⃣ Crear .env
```bash
echo PORT=5000 > .env
echo MONGODB_URI=mongodb://localhost:27017/manifestation-journal >> .env
echo JWT_SECRET=cambiar-en-produccion >> .env
echo PYTHON_API_URL=http://localhost:8000 >> .env
```

### 3️⃣ Ejecutar 3 Terminales

**Terminal 1:**
```bash
mongod
```

**Terminal 2:**
```bash
npm run dev
```

**Terminal 3:**
```bash
cd python-analytics && venv\Scripts\activate && python -m uvicorn api:app --reload --port 8000
```

### 4️⃣ Verificar
```bash
curl http://localhost:5000/api/health
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Abre en navegador
```

---

## 🧪 Test Rápido

### Generar Gráfico en Base64
```bash
curl -X POST http://localhost:5000/api/analytics/graficar \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [
      {"tipo": "A", "valor": 10},
      {"tipo": "B", "valor": 20},
      {"tipo": "C", "valor": 15}
    ],
    "tipo": "frecuencia",
    "columna": "tipo"
  }'
```

Busca en la respuesta: `"imagen_base64": "iVBORw0K..."`

### Generar Reporte Completo
```bash
curl -X POST http://localhost:5000/api/analytics/reporte \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [
      {"fecha": "2024-01-01", "categoria": "Manifestación", "valor": 8},
      {"fecha": "2024-01-02", "categoria": "Gratitud", "valor": 9}
    ],
    "titulo": "Mi Análisis"
  }'
```

---

## 📊 7 Gráficos Disponibles

1. **Barras** - Frecuencias
2. **Histograma** - Distribuciones
3. **Pastel** - Proporciones
4. **Box Plot** - Cuartiles
5. **Heatmap** - Correlaciones
6. **Línea** - Tendencias temporales
7. **Combo** - Reporte completo

---

## 🚀 URL Importantes

| Servicio | URL | Descripción |
|----------|-----|------------|
| Backend | http://localhost:5000 | API Node.js |
| API Python | http://localhost:8000 | API Analytics |
| Docs | http://localhost:8000/docs | Documentación interactiva |
| Health | http://localhost:5000/api/health | Estado backend |
| Analytics | http://localhost:5000/api/analytics | Todos los endpoints |

---

## 📚 Documentación Completa

Ver archivos:
- `README.md` - Descripción general
- `INSTRUCCIONES_EJECUCION.md` - Guía detallada
- `REACT_INTEGRATION.md` - Integración React
- `ENTREGABLES.md` - Qué se entrega
- `python-analytics/README.md` - Módulo Python

---

## ✅ Verificación Rápida

```bash
# Todos estos deben responder
curl http://localhost:5000/api/health
curl http://localhost:8000/health
curl -X POST http://localhost:5000/api/analytics/analizar -d '{"registros":[{"x":1}]}' -H "Content-Type: application/json"
```

Si todo responde con `"success": true` ✅ estás listo!

---

## 🔧 Troubleshooting Rápido

| Error | Solución |
|-------|----------|
| Puerto 5000 en uso | Cambiar PORT en .env |
| Python no encuentra módulos | Activar venv: `venv\Scripts\activate` |
| MongoDB error | Usar MongoDB Atlas (cambiar MONGODB_URI) |
| API Python no responde | Verificar: `curl http://localhost:8000/` |
| Gráfico vacío | Revisar estructura de datos en request |

---

**¡Listo para analizar datos! 🚀**

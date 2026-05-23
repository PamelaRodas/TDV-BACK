# 🔄 Git Flow - Flujo de Entrega Momento 3

## Descripción
Este documento describe el proceso de Git Flow para la entrega de "Nuevas Tecnologías - Momento 3" con integración de análisis visual y visualización de datos.

## 📋 Estructura de Ramas

```
main (producción)
  ↑
develop (desarrollo)
  ↑
feature/reporte-visual (esta rama)
  ├── analisis-datos
  ├── visualizaciones
  ├── api-integracion
  └── documentacion
```

## 🚀 Pasos para la Entrega

### 1️⃣ Crear Rama Feature

```bash
# Actualizar rama develop
git checkout develop
git pull origin develop

# Crear rama feature
git checkout -b feature/reporte-visual
```

### 2️⃣ Hacer Commits Significativos

**A. Módulo de Análisis**
```bash
git add python-analytics/analisis.py
git commit -m "feat: Módulo de análisis estadístico de datos"
```

**B. Módulo de Visualización**
```bash
git add python-analytics/visualizacion.py
git commit -m "feat: Módulo de visualización con Matplotlib y Seaborn"
```

**C. Generador de Reportes**
```bash
git add python-analytics/reporte.py
git commit -m "feat: Generador de reportes en JSON y HTML"
```

**D. API FastAPI**
```bash
git add python-analytics/api.py
git commit -m "feat: API FastAPI para análisis y visualización"
```

**E. Integración Node.js**
```bash
git add routes/analytics.js server.js package.json
git commit -m "feat: Integración API Python con backend Express"
```

**F. Documentación**
```bash
git add python-analytics/README.md python-analytics/requirements.txt python-analytics/ejemplo.py
git commit -m "docs: Documentación completa del módulo Python"
```

**G. Configuración**
```bash
git add python-analytics/__init__.py
git commit -m "chore: Configuración de módulo Python"
```

### 3️⃣ Subir rama al repositorio

```bash
git push origin feature/reporte-visual
```

### 4️⃣ Crear Pull Request (PR)

**En GitHub/GitLab:**

1. Ir a la página del repositorio
2. Click en "Pull requests"
3. Click en "New pull request"
4. Seleccionar:
   - Base: `develop`
   - Compare: `feature/reporte-visual`
5. Crear el PR con descripción:

```markdown
## 📊 Integración de Análisis Visual - Momento 3

### Descripción
Implementación completa de módulo Python para análisis y visualización de datos
con integración al backend Node.js y frontend React.

### ✨ Cambios

#### 🔍 Análisis de Datos
- Estadísticas descriptivas (media, mediana, desv. std)
- Limpieza automática de datos (duplicados, valores nulos)
- Detección de outliers (métodos IQR y Z-Score)
- Análisis de tendencias temporales
- Matriz de correlaciones

#### 📈 Visualizaciones
- Gráficos de barras (frecuencia)
- Histogramas (distribución)
- Gráficos de pastel (proporciones)
- Box plots (análisis estadístico)
- Heatmaps (correlaciones)
- Gráficos de tendencia temporal

#### 📋 Reportes
- Exportación a JSON con Base64
- Reportes HTML interactivos
- Integración con API REST

#### 🔌 API
- 7 endpoints REST
- CORS configurado
- Documentación automática Swagger

#### 🔗 Integración
- Ruta Node.js `/api/analytics`
- Proxy a API Python
- Validación de datos

### 📁 Archivos Añadidos
- `python-analytics/analisis.py`
- `python-analytics/visualizacion.py`
- `python-analytics/reporte.py`
- `python-analytics/api.py`
- `python-analytics/ejemplo.py`
- `python-analytics/README.md`
- `python-analytics/requirements.txt`
- `python-analytics/__init__.py`
- `routes/analytics.js`
- Actualización de `server.js` y `package.json`

### 🎯 Entregables

✅ Módulo visualizacion.py con funciones:
  - graficar_frecuencia()
  - graficar_distribucion()
  - graficar_correlacion()
  - graficar_pastel()
  - graficar_box()
  - graficar_tendencia_temporal()

✅ Exportación a Base64 para integración con React

✅ API REST para consumir desde el frontend

✅ Documentación completa

✅ Ejemplos de uso

### 🚀 Cómo Usar

**Instalar dependencias Python:**
```bash
cd python-analytics
pip install -r requirements.txt
```

**Ejecutar ejemplos:**
```bash
python ejemplo.py
```

**Iniciar API Python:**
```bash
python -m uvicorn api:app --reload --port 8000
```

**Usar desde Node.js:**
```javascript
POST /api/analytics/graficar
{
  "registros": [...],
  "tipo": "frecuencia",
  "columna": "categoria"
}
```

### 📊 Ejemplo de Respuesta

```json
{
  "success": true,
  "grafico": {
    "tipo": "frecuencia",
    "imagen_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAA...",
    "nombre": "frecuencia_categoria_20231122.png"
  }
}
```

### 🔄 Git Flow
- Rama: `feature/reporte-visual`
- Base: `develop`
- Destino final: `main` (vía `develop`)

### ✅ Checklist

- [x] Análisis de datos implementado
- [x] Visualizaciones creadas (6+ tipos)
- [x] API FastAPI funcionando
- [x] Integración Node.js completa
- [x] Base64 implementado para React
- [x] Ejemplos de uso
- [x] Documentación completa
- [x] README actualizado

### 🔗 Conexión con Repositorios

- **Backend**: TDV-BACK (actual)
- **Frontend**: TDV-BACK-2 (a integrar)

### 📞 Notas

Asegúrate de tener ambas APIs ejecutándose:
- Backend Node.js: puerto 5000
- API Python: puerto 8000

### Relacionados
Closes #TODO (reemplazar con número de issue si aplica)
```

### 5️⃣ Revisión y Merge

**Proceso:**
1. Code review (si es necesario)
2. Resolver conflictos (si los hay)
3. Merge a `develop`
4. Eliminar rama `feature/reporte-visual`

```bash
# Después del merge aprobado
git checkout develop
git pull origin develop

# Eliminar rama local
git branch -d feature/reporte-visual

# Eliminar rama remota
git push origin --delete feature/reporte-visual
```

## 📋 Historial de Commits Esperado

```
commit abc123 - chore: Configuración de módulo Python
commit def456 - docs: Documentación completa del módulo Python
commit ghi789 - feat: Integración API Python con backend Express
commit jkl012 - feat: API FastAPI para análisis y visualización
commit mno345 - feat: Generador de reportes en JSON y HTML
commit pqr678 - feat: Módulo de visualización con Matplotlib y Seaborn
commit stu901 - feat: Módulo de análisis estadístico de datos
```

## 🔍 Verificación Antes de Merge

- [ ] Todos los tests pasan
- [ ] Sin conflictos de merge
- [ ] Código bien documentado
- [ ] README actualizado
- [ ] Ejemplos funcionando
- [ ] CHANGELOG actualizado

## 📝 Actualizar CHANGELOG.md

```markdown
## [1.1.0] - 2024-01-22

### Added
- Módulo Python para análisis de datos (analisis.py)
- Módulo de visualización con 6+ tipos de gráficos (visualizacion.py)
- Generador de reportes en JSON y HTML (reporte.py)
- API FastAPI con 7 endpoints para análisis
- Integración Node.js con ruta /api/analytics
- Exportación de gráficos a Base64 para React
- Documentación completa y ejemplos

### Changed
- Actualizado server.js para incluir ruta analytics
- Actualizado package.json con dependencia axios

### Fixed
- N/A

## Instalación de dependencias Python
```bash
pip install -r python-analytics/requirements.txt
```
```

## 🎯 Entrega Final

Después del merge a `develop`:

1. **Crear tag de release** (opcional):
```bash
git tag -a v1.1.0-analytics -m "Release: Momento 3 - Analytics"
git push origin v1.1.0-analytics
```

2. **Crear release en GitHub** (opcional):
   - Draft Release → v1.1.0-analytics
   - Agregar descripción y archivos

3. **Merge a main** (cuando está listo para producción):
```bash
git checkout main
git pull origin main
git merge develop
git push origin main
```

## 📚 Recursos Adicionales

- [Git Flow Modelo](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Express Routing](https://expressjs.com/en/guide/routing.html)

## ❓ Preguntas Frecuentes

**P: ¿Qué pasa si hay conflictos?**
R: Resolver manualmente en el editor, hacer commit y push.

**P: ¿Puedo hacer commits en main directamente?**
R: No, siempre usar rama feature y hacer PR.

**P: ¿Qué hacer después del merge?**
R: Actualizar documentación y crear release si es necesario.

---

✅ **Flujo completado** - Listo para entrega

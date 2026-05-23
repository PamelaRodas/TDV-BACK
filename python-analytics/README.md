# 📊 TDV Analytics - Módulo Python

## Descripción
Módulo completo de análisis y visualización de datos para **Manifestation Journal**. Genera gráficos interactivos en Base64/SVG para integración con React/Frontend.

## 🎯 Características

### ✨ Análisis de Datos
- **Estadísticas descriptivas**: Media, mediana, desviación estándar
- **Limpieza automática**: Eliminación de duplicados, manejo de valores nulos
- **Detección de outliers**: Métodos IQR y Z-Score
- **Análisis de tendencias**: Tendencias temporales y evolución de datos
- **Correlaciones**: Matriz de correlación entre variables

### 📈 Visualizaciones
- **Gráficos de barras**: Frecuencia de elementos
- **Histogramas**: Distribución de datos numéricos
- **Gráficos de pastel**: Proporciones y segmentación
- **Box plots**: Análisis de distribución con cuartiles
- **Heatmaps**: Correlación entre variables
- **Gráficos de tendencia**: Evolución temporal

### 📋 Reportes
- **JSON**: Datos estructurados con gráficos en Base64
- **HTML interactivo**: Reportes visuales listos para compartir
- **Base64**: Imágenes codificadas para envío vía API

### 🔌 API FastAPI
- Endpoints RESTful para análisis y visualización
- CORS configurado para múltiples orígenes
- Documentación automática en `/docs`
- Validación de datos

## 📁 Estructura

```
python-analytics/
├── __init__.py              # Módulo principal
├── analisis.py              # Análisis estadístico
├── visualizacion.py         # Generación de gráficos
├── reporte.py               # Generador de reportes
├── api.py                   # API FastAPI
├── ejemplo.py               # Ejemplos de uso
├── requirements.txt         # Dependencias Python
└── reportes/               # Gráficos y reportes generados
```

## 🚀 Instalación

### Requisitos
- Python 3.8+
- pip

### Pasos

1. **Navegar al directorio**
```bash
cd python-analytics
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 💻 Uso

### Opción 1: Ejecutar Ejemplos

```bash
python ejemplo.py
```

Esto generará:
- Análisis de datos
- 4 gráficos diferentes
- Reporte HTML interactivo
- Detección de outliers

### Opción 2: Usar como Librería

```python
from analisis import crear_analizador
from visualizacion import crear_visualizador
from reporte import crear_generador
import pandas as pd

# Cargar datos
df = pd.read_csv('datos.csv')

# Análisis
analizador = crear_analizador()
analizador.cargar_datos(dataframe=df)
analizador.limpiar_datos()
stats = analizador.obtener_estadisticas_descriptivas()

# Visualización
visualizador = crear_visualizador()
resultado = visualizador.graficar_frecuencia(df, 'columna')

# Reporte
generador = crear_generador()
reporte = generador.crear_respuesta_api(df, 'Mi Análisis')
```

### Opción 3: Ejecutar API

```bash
python -m uvicorn api:app --reload --port 8000
```

API disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

## 🔌 Endpoints de la API

### POST `/analizar`
Analizar datos en formato JSON

```bash
curl -X POST "http://localhost:8000/analizar" \
  -H "Content-Type: application/json" \
  -d '{"registros": [{"nombre": "John", "edad": 30}, {"nombre": "Jane", "edad": 25}]}'
```

### POST `/graficar`
Generar un gráfico específico

```bash
curl -X POST "http://localhost:8000/graficar" \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [...],
    "tipo": "frecuencia",
    "columna": "categoria",
    "titulo": "Mi Gráfico"
  }'
```

**Tipos disponibles:** `frecuencia`, `distribucion`, `correlacion`, `pastel`, `box`, `tendencia`

### POST `/reporte`
Generar reporte completo

```bash
curl -X POST "http://localhost:8000/reporte" \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [...],
    "titulo": "Análisis Visual",
    "formato": "json"
  }'
```

### POST `/cargar-csv`
Cargar y analizar archivo CSV

```bash
curl -X POST "http://localhost:8000/cargar-csv" \
  -F "file=@datos.csv"
```

### POST `/outliers`
Detectar valores atípicos

```bash
curl -X POST "http://localhost:8000/outliers" \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [...],
    "columna": "precio",
    "metodo": "iqr"
  }'
```

### POST `/tendencias`
Analizar tendencias temporales

```bash
curl -X POST "http://localhost:8000/tendencias" \
  -H "Content-Type: application/json" \
  -d '{
    "registros": [...],
    "fecha_columna": "createdAt",
    "valor_columna": "puntuacion"
  }'
```

## 🎨 Respuesta de Gráficos

Todos los gráficos se devuelven en Base64-PNG:

```json
{
  "success": true,
  "grafico": {
    "tipo": "frecuencia",
    "imagen_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAA...",
    "nombre": "frecuencia_categoria_20231122_143022.png"
  }
}
```

**Para usar en React/JavaScript:**
```javascript
const imagenSrc = `data:image/png;base64,${respuesta.grafico.imagen_base64}`;
<img src={imagenSrc} alt="Gráfico" />
```

## 📊 Ejemplos de Análisis

### Análisis de Diario Personal

```python
from reporte import crear_generador

datos_diario = [
    {"fecha": "2024-01-01", "categoria": "Manifestación", "estado": "completado", "puntuacion": 8},
    {"fecha": "2024-01-02", "categoria": "Gratitud", "estado": "completado", "puntuacion": 9},
    # ...
]

generador = crear_generador()
reporte = generador.crear_respuesta_api(datos_diario, "Análisis de Enero")
```

### Gráfico de Tendencia Semanal

```python
from visualizacion import crear_visualizador
import pandas as pd

visualizador = crear_visualizador()
df = pd.DataFrame(datos)
resultado = visualizador.graficar_tendencia_temporal(
    df, 
    fecha_columna='createdAt',
    valor_columna=None,  # Contar registros
    titulo='Registros por Día'
)
```

## 🔄 Integración con Backend Node.js

El módulo está diseñado para funcionar con el backend Express.js:

1. **Backend Node.js** (`puerto 5000`): Maneja autenticación y datos de usuarios
2. **API Python** (`puerto 8000`): Procesa análisis y gráficos
3. **Frontend React** (TDV-BACK-2): Consume ambas APIs

**Flujo:**
```
React → Node.js API (datos) → Python API (análisis) → Gráficos Base64 → React
```

## 🔐 Seguridad

- CORS habilitado (personalizar en producción)
- Validación de entrada en todos los endpoints
- Manejo de errores con traceback
- Datos procesados en memoria (no persistencia)

## 📝 Notas Importantes

- Los gráficos se generan en formato PNG y se codifican en Base64
- Los archivos también se guardan en el directorio `reportes/`
- El módulo maneja automáticamente valores nulos y duplicados
- Soporta análisis con múltiples tipos de datos (numéricos, categóricos, fechas)

## 🆘 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install -r requirements.txt
```

### Error de CORS
Asegurate de que ambas APIs (Node.js y Python) estén ejecutándose:
- Node.js: `http://localhost:5000`
- Python: `http://localhost:8000`

### Gráficos no se generan
Verifica que el directorio `reportes/` exista:
```bash
mkdir reportes
```

## 📚 Documentación Completa

Para más información sobre cada módulo, revisa los comentarios en:
- `analisis.py`: Análisis estadístico
- `visualizacion.py`: Generación de gráficos
- `reporte.py`: Reportes e integración
- `api.py`: Endpoints REST

## 🤝 Contribuciones

Sugerencias y mejoras bienvenidas.

## 📄 Licencia

MIT

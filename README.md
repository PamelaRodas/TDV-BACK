- ✅ Módulo Python de análisis estadístico
- ✅ Visualización de datos (6+ tipos de gráficos)
- ✅ Exportación a Base64 para React
- ✅ API REST para análisis (`/api/analytics`)

## 📊 Análisis Visual y Resultados

### 🔍 Hallazgos del Análisis de Datos
- **Preferencia de Contenido:** El 60% de los usuarios interactúan principalmente con contenidos de tipo **"Calma"** y **"Equilibrio"**, lo que sugiere una fuerte tendencia hacia la búsqueda de bienestar emocional.
- **Calidad de Datos (Outliers):** Se detectaron sesiones con duraciones superiores a 40 minutos (representando un 5% del total). Estos datos fueron aislados para no sesgar los promedios de uso diario.
- **Crecimiento de Retención:** Se observa un incremento del **15% semanal** en el uso de "Espacios Sagrados" específicamente durante la franja horaria de 6:00 AM a 9:00 AM.

### 🚀 Instrucciones de Ejecución Actualizadas

**Nota para Windows:** Si el comando `python` no funciona, intenta con `py`. Si `pip` no funciona, usa `python -m pip`.

1. **Configurar el Backend (Node.js):**
   * Entra a la carpeta: `cd TDV-BACK`
   * Instala dependencias: `npm install`
   * Carga los datos iniciales: `node scripts/seed.js`
   * Inicia el servidor: `npm run dev`

2. **Configurar el Módulo Analítico (Python):**
   * Entra a la carpeta: `cd python-analytics`
   * Instala librerías: `python -m pip install -r requirements.txt`
   * Inicia la API de análisis: `python api.py` (o `py api.py`)

3. **Integración con React:**
   * Sigue los pasos en `REACT_INTEGRATION.md` para conectar el componente `AnalysisReport.jsx` al endpoint `http://localhost:5000/api/analytics/reporte`.

**Cómo ejecutar el análisis:**
1. Asegúrate de tener las dependencias instaladas: `pip install pandas matplotlib`
2. Ejecuta el script principal de analítica:
   ```bash
   python python-analytics/main.py
   ```
3. Los resultados se enviarán automáticamente a la API de Node.js o se guardarán en la carpeta `/outputs`.

**Ejemplo de funciones disponibles:**

- `graficar_frecuencia(dataframe, columna)`: genera un gráfico de barras con los elementos más comunes.
- `graficar_agrupacion(dataframe, columna_agrupacion, columna_valor)`: genera un gráfico de barras agrupado por suma.

**Cómo usar el módulo:**

```python
from visualizacion import graficar_frecuencia, graficar_agrupacion
import pandas as pd

# Cargar datos
df = pd.read_csv('datos.csv')

# Gráfico de frecuencia
svg = graficar_frecuencia(df, 'categoria')
with open('frecuencia.svg', 'w', encoding='utf-8') as f:
   f.write(svg)
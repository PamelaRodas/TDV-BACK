# 🔗 Integración React - Guía Completa

## 📌 Resumen
Instrucciones para integrar el módulo de análisis visual con React (TDV-BACK-2).

## 🎯 Arquitectura

```
┌─────────────────┐
│   React App     │
│  (TDV-BACK-2)   │
└────────┬────────┘
         │
         ├── /api/diary (datos)
         ├── /api/analytics (análisis)
         │
┌─────────────────────────────────┐
│   Node.js Backend (5000)        │
│   - Autenticación               │
│   - Datos (diary, photos, etc)  │
│   - Proxy a Python API          │
└────────┬────────────────────────┘
         │
┌─────────────────────────────────┐
│   Python API (8000)             │
│   - Análisis de datos           │
│   - Generación de gráficos      │
│   - Exportación Base64          │
└─────────────────────────────────┘
```

## 🚀 Paso 1: Configuración Base

### 1.1 Variables de entorno (.env)

```env
# Backend Node.js
REACT_APP_API_URL=http://localhost:5000
REACT_APP_ANALYTICS_URL=http://localhost:5000/api/analytics

# O directamente a Python (si se requiere)
REACT_APP_PYTHON_API_URL=http://localhost:8000
```

### 1.2 Crear servicio API

**`src/services/analyticsService.js`**

```javascript
// Servicio para comunicarse con API de análisis
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const analyticsService = {
  /**
   * Analizar datos
   * @param {Array} registros - Datos a analizar
   * @returns {Promise} Resultado del análisis
   */
  async analizar(registros) {
    const response = await fetch(`${API_URL}/api/analytics/analizar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ registros })
    });
    return response.json();
  },

  /**
   * Generar gráfico
   * @param {Array} registros - Datos
   * @param {String} tipo - Tipo de gráfico
   * @param {String} columna - Columna a graficar
   * @param {String} titulo - Título del gráfico
   * @returns {Promise} Gráfico en Base64
   */
  async generarGrafico(registros, tipo, columna, titulo) {
    const response = await fetch(`${API_URL}/api/analytics/graficar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ registros, tipo, columna, titulo })
    });
    return response.json();
  },

  /**
   * Generar reporte completo
   * @param {Array} registros - Datos
   * @param {String} titulo - Título del reporte
   * @returns {Promise} Reporte con gráficos
   */
  async generarReporte(registros, titulo = 'Análisis Visual') {
    const response = await fetch(`${API_URL}/api/analytics/reporte`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ registros, titulo, formato: 'json' })
    });
    return response.json();
  },

  /**
   * Detectar outliers
   * @param {Array} registros - Datos
   * @param {String} columna - Columna a analizar
   * @param {String} metodo - 'iqr' o 'zscore'
   * @returns {Promise} Outliers encontrados
   */
  async detectarOutliers(registros, columna, metodo = 'iqr') {
    const response = await fetch(`${API_URL}/api/analytics/outliers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ registros, columna, metodo })
    });
    return response.json();
  },

  /**
   * Analizar tendencias
   * @param {Array} registros - Datos
   * @param {String} fechaColumna - Columna con fechas
   * @param {String} valorColumna - Columna con valores
   * @returns {Promise} Tendencias
   */
  async analizarTendencias(registros, fechaColumna = 'createdAt', valorColumna = null) {
    const response = await fetch(`${API_URL}/api/analytics/tendencias`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ registros, fecha_columna: fechaColumna, valor_columna: valorColumna })
    });
    return response.json();
  },

  /**
   * Obtener información de columnas
   * @param {Array} registros - Datos
   * @returns {Promise} Información de columnas
   */
  async obtenerColumnasInfo(registros) {
    const response = await fetch(`${API_URL}/api/analytics/columnas-info`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ registros })
    });
    return response.json();
  },

  /**
   * Verificar estado de API Python
   * @returns {Promise} Estado
   */
  async verificarSalud() {
    const response = await fetch(`${API_URL}/api/analytics/health`);
    return response.json();
  }
};
```

## 🎨 Paso 2: Componentes React

### 2.1 Componente de Gráfico Simple

**`src/components/AnalysisChart.jsx`**

```jsx
import React, { useState, useEffect } from 'react';
import { analyticsService } from '../services/analyticsService';

export function AnalysisChart({ datos, tipo = 'frecuencia', columna, titulo }) {
  const [grafico, setGrafico] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    generarGrafico();
  }, [datos, tipo, columna]);

  const generarGrafico = async () => {
    if (!datos || datos.length === 0) return;

    setCargando(true);
    setError(null);

    try {
      const resultado = await analyticsService.generarGrafico(
        datos,
        tipo,
        columna,
        titulo
      );

      if (resultado.success && resultado.grafico?.imagen_base64) {
        setGrafico(resultado.grafico.imagen_base64);
      } else {
        setError('Error al generar gráfico');
      }
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="analysis-chart">
      <h3>{titulo || `${tipo} de ${columna}`}</h3>
      
      {cargando && <p>Generando gráfico...</p>}
      {error && <p className="error">{error}</p>}
      
      {grafico && (
        <img 
          src={`data:image/png;base64,${grafico}`}
          alt={titulo}
          style={{ maxWidth: '100%', height: 'auto' }}
        />
      )}
    </div>
  );
}
```

### 2.2 Componente de Reporte Completo

**`src/components/AnalysisReport.jsx`**

```jsx
import React, { useState } from 'react';
import { analyticsService } from '../services/analyticsService';
import { AnalysisChart } from './AnalysisChart';

export function AnalysisReport({ datos, titulo = 'Análisis Visual' }) {
  const [reporte, setReporte] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState(null);

  const generarReporte = async () => {
    if (!datos || datos.length === 0) {
      setError('No hay datos para analizar');
      return;
    }

    setCargando(true);
    setError(null);

    try {
      const resultado = await analyticsService.generarReporte(datos, titulo);
      setReporte(resultado.reporte);
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    } finally {
      setCargando(false);
    }
  };

  if (!reporte) {
    return (
      <div className="analysis-report">
        <h2>{titulo}</h2>
        <p>Registros: {datos?.length || 0}</p>
        <button onClick={generarReporte} disabled={cargando}>
          {cargando ? 'Generando...' : 'Generar Reporte'}
        </button>
        {error && <p className="error">{error}</p>}
      </div>
    );
  }

  return (
    <div className="analysis-report">
      <h2>{reporte.id}</h2>
      
      <div className="stats">
        <h3>📊 Estadísticas Generales</h3>
        <div className="stats-grid">
          <div className="stat-item">
            <label>Total de Registros</label>
            <strong>{reporte.estadisticas.resumen.total_registros}</strong>
          </div>
          <div className="stat-item">
            <label>Columnas</label>
            <strong>{reporte.estadisticas.resumen.total_columnas}</strong>
          </div>
          <div className="stat-item">
            <label>Duplicados</label>
            <strong>{reporte.estadisticas.resumen.duplicados}</strong>
          </div>
          <div className="stat-item">
            <label>Memoria (MB)</label>
            <strong>{reporte.estadisticas.resumen.memoria_mb}</strong>
          </div>
        </div>
      </div>

      <div className="graficos">
        <h3>📈 Gráficos</h3>
        <div className="graficos-grid">
          {Object.entries(reporte.graficos).map(([key, grafico]) => (
            <div key={key} className="grafico-item">
              <h4>{grafico.descripcion}</h4>
              {grafico.imagen_base64 && (
                <img 
                  src={`data:image/png;base64,${grafico.imagen_base64}`}
                  alt={grafico.descripcion}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      <button onClick={generarReporte}>Regenerar Reporte</button>
    </div>
  );
}
```

### 2.3 Componente de Panel de Análisis

**`src/components/AnalysisPanel.jsx`**

```jsx
import React, { useState, useEffect } from 'react';
import { analyticsService } from '../services/analyticsService';
import { AnalysisChart } from './AnalysisChart';

export function AnalysisPanel({ datos }) {
  const [columnas, setColumnas] = useState([]);
  const [columnasSeleccionadas, setColumnasSeleccionadas] = useState([]);
  const [tipoGrafico, setTipoGrafico] = useState('frecuencia');
  const [error, setError] = useState(null);

  useEffect(() => {
    cargarColumnasInfo();
  }, [datos]);

  const cargarColumnasInfo = async () => {
    if (!datos || datos.length === 0) return;

    try {
      const resultado = await analyticsService.obtenerColumnasInfo(datos);
      const columnasDisponibles = Object.keys(resultado.columnas_info || {});
      setColumnas(columnasDisponibles);
    } catch (err) {
      setError(err.message);
    }
  };

  const tiposGraficosDisponibles = [
    { valor: 'frecuencia', etiqueta: 'Frecuencia' },
    { valor: 'distribucion', etiqueta: 'Distribución' },
    { valor: 'pastel', etiqueta: 'Pastel' },
    { valor: 'box', etiqueta: 'Box Plot' },
    { valor: 'correlacion', etiqueta: 'Correlación' },
    { valor: 'tendencia', etiqueta: 'Tendencia' }
  ];

  return (
    <div className="analysis-panel">
      <h2>🔍 Panel de Análisis</h2>
      
      {error && <p className="error">{error}</p>}

      <div className="controles">
        <div className="control-group">
          <label>Tipo de Gráfico:</label>
          <select 
            value={tipoGrafico} 
            onChange={(e) => setTipoGrafico(e.target.value)}
          >
            {tiposGraficosDisponibles.map(tipo => (
              <option key={tipo.valor} value={tipo.valor}>
                {tipo.etiqueta}
              </option>
            ))}
          </select>
        </div>

        <div className="control-group">
          <label>Columnas a Analizar:</label>
          <div className="columnas-checkboxes">
            {columnas.map(columna => (
              <label key={columna}>
                <input 
                  type="checkbox"
                  checked={columnasSeleccionadas.includes(columna)}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setColumnasSeleccionadas([...columnasSeleccionadas, columna]);
                    } else {
                      setColumnasSeleccionadas(
                        columnasSeleccionadas.filter(c => c !== columna)
                      );
                    }
                  }}
                />
                {columna}
              </label>
            ))}
          </div>
        </div>
      </div>

      <div className="graficos-generados">
        {columnasSeleccionadas.map(columna => (
          <AnalysisChart
            key={columna}
            datos={datos}
            tipo={tipoGrafico}
            columna={columna}
            titulo={`${tipoGrafico} de ${columna}`}
          />
        ))}
      </div>
    </div>
  );
}
```

## 🎯 Paso 3: Uso en Páginas

### 3.1 Página de Análisis de Diario

**`src/pages/DiaryAnalysis.jsx`**

```jsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { AnalysisReport } from '../components/AnalysisReport';
import { AnalysisPanel } from '../components/AnalysisPanel';

export function DiaryAnalysis() {
  const { token } = useAuth();
  const [entries, setEntries] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);
  const [vista, setVista] = useState('report'); // 'report' o 'panel'

  useEffect(() => {
    cargarDatos();
  }, [token]);

  const cargarDatos = async () => {
    try {
      const response = await fetch(
        'http://localhost:5000/api/diary',
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      );
      const datos = await response.json();
      setEntries(datos);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  };

  if (cargando) return <div>Cargando...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="diary-analysis">
      <h1>📊 Análisis de tu Diario</h1>

      <div className="vista-selector">
        <button 
          className={vista === 'report' ? 'activa' : ''}
          onClick={() => setVista('report')}
        >
          Reporte Completo
        </button>
        <button 
          className={vista === 'panel' ? 'activa' : ''}
          onClick={() => setVista('panel')}
        >
          Panel de Análisis
        </button>
      </div>

      {vista === 'report' ? (
        <AnalysisReport 
          datos={entries}
          titulo="Análisis de mi Diario"
        />
      ) : (
        <AnalysisPanel datos={entries} />
      )}
    </div>
  );
}
```

## 🎨 Paso 4: Estilos CSS

**`src/styles/analysis.css`**

```css
/* Panel de Análisis */
.analysis-panel {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.controles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.control-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 8px;
}

.control-group select,
.control-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.columnas-checkboxes {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.columnas-checkboxes label {
  display: flex;
  align-items: center;
  font-weight: normal;
}

.columnas-checkboxes input {
  margin-right: 8px;
}

/* Gráficos */
.graficos-generados {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.analysis-chart {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #eee;
}

.analysis-chart img {
  max-width: 100%;
  height: auto;
  margin-top: 15px;
  border-radius: 4px;
}

/* Reporte */
.analysis-report {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
}

.stats {
  margin: 30px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.stat-item {
  padding: 15px;
  background: #f0f0f0;
  border-radius: 8px;
  text-align: center;
}

.stat-item label {
  display: block;
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
}

.stat-item strong {
  display: block;
  font-size: 24px;
  color: #667eea;
}

/* Botones */
button {
  padding: 10px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

button:hover {
  background: #5568d3;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Estado activo */
button.activa {
  background: #667eea;
  font-weight: bold;
}

/* Errores */
.error {
  color: #d32f2f;
  padding: 10px;
  background: #ffebee;
  border-radius: 4px;
  margin: 10px 0;
}
```

## ✅ Checklist de Integración

- [ ] Crear archivo `analyticsService.js`
- [ ] Importar servicio en componentes
- [ ] Crear componentes de análisis
- [ ] Agregar estilos CSS
- [ ] Crear página de análisis
- [ ] Verificar CORS entre React y Node.js
- [ ] Verificar conexión a API Python
- [ ] Hacer pruebas de análisis
- [ ] Documentar uso en README

## 🔍 Pruebas

### Test de Conexión

```javascript
// En la consola del navegador
const testAnalytics = async () => {
  const datos = [
    { categoria: 'A', valor: 10 },
    { categoria: 'B', valor: 20 }
  ];
  
  const resultado = await fetch('http://localhost:5000/api/analytics/analizar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ registros: datos })
  });
  
  console.log(await resultado.json());
};

testAnalytics();
```

## 🚀 Deployment

Para producción, actualiza las URLs:

```env
REACT_APP_API_URL=https://api.tudominio.com
REACT_APP_PYTHON_API_URL=https://api-analytics.tudominio.com
```

---

✅ **Integración completada** - Listo para usar en React

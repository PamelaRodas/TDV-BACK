/**
 * Rutas de Analytics
 * Conecta con la API Python para análisis y visualización
 */

const express = require('express');
const router = express.Router();
const axios = require('axios');

const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8000';

/**
 * POST /api/analytics/analizar
 * Analizar datos enviados desde el frontend
 */
router.post('/analizar', async (req, res) => {
  try {
    const { registros, titulo } = req.body;

    if (!registros || !Array.isArray(registros)) {
      return res.status(400).json({
        error: 'Se requiere un array de registros',
      });
    }

    const response = await axios.post(`${PYTHON_API_URL}/analizar`, {
      registros,
    });

    res.json({
      success: true,
      data: response.data,
      source: 'python-analytics',
    });
  } catch (error) {
    console.error('Error en /analizar:', error.message);
    res.status(500).json({
      error: 'Error al analizar datos',
      details: error.message,
    });
  }
});

/**
 * POST /api/analytics/graficar
 * Generar un gráfico específico
 */
router.post('/graficar', async (req, res) => {
  try {
    const { registros, tipo, columna, titulo } = req.body;

    if (!registros || !Array.isArray(registros)) {
      return res.status(400).json({
        error: 'Se requiere un array de registros',
      });
    }

    if (!tipo) {
      return res.status(400).json({
        error: 'Se requiere especificar tipo de gráfico',
        tiposDisponibles: [
          'frecuencia',
          'distribucion',
          'correlacion',
          'pastel',
          'box',
          'tendencia',
        ],
      });
    }

    // Llamar a la API Python
    const response = await axios.post(`${PYTHON_API_URL}/graficar`, {
      registros,
      tipo,
      columna,
      titulo,
    });

    res.json({
      success: true,
      grafico: response.data.grafico,
      timestamp: response.data.timestamp,
    });
  } catch (error) {
    console.error('Error en /graficar:', error.message);
    res.status(500).json({
      error: 'Error al generar gráfico',
      details: error.message,
    });
  }
});

/**
 * POST /api/analytics/reporte
 * Generar reporte completo con múltiples gráficos
 */
router.post('/reporte', async (req, res) => {
  try {
    const { registros, titulo = 'Análisis Visual', formato = 'json' } =
      req.body;

    if (!registros || !Array.isArray(registros)) {
      return res.status(400).json({
        error: 'Se requiere un array de registros',
      });
    }

    // Llamar a la API Python
    const response = await axios.post(`${PYTHON_API_URL}/reporte`, {
      registros,
      titulo,
      formato,
    });

    res.json({
      success: true,
      reporte: response.data.reporte,
      estadisticas: response.data.estadisticas,
      timestamp: response.data.timestamp,
    });
  } catch (error) {
    console.error('Error en /reporte:', error.message);
    res.status(500).json({
      error: 'Error al generar reporte',
      details: error.message,
    });
  }
});

/**
 * POST /api/analytics/outliers
 * Detectar valores atípicos
 */
router.post('/outliers', async (req, res) => {
  try {
    const { registros, columna, metodo = 'iqr' } = req.body;

    if (!registros || !Array.isArray(registros)) {
      return res.status(400).json({
        error: 'Se requiere un array de registros',
      });
    }

    if (!columna) {
      return res.status(400).json({
        error: 'Se requiere especificar una columna',
      });
    }

    // Llamar a la API Python
    const response = await axios.post(`${PYTHON_API_URL}/outliers`, {
      registros,
      columna,
      metodo,
    });

    res.json({
      success: true,
      outliers: response.data.outliers,
      timestamp: response.data.timestamp,
    });
  } catch (error) {
    console.error('Error en /outliers:', error.message);
    res.status(500).json({
      error: 'Error al detectar outliers',
      details: error.message,
    });
  }
});

/**
 * POST /api/analytics/tendencias
 * Analizar tendencias temporales
 */
router.post('/tendencias', async (req, res) => {
  try {
    const {
      registros,
      fecha_columna = 'createdAt',
      valor_columna,
    } = req.body;

    if (!registros || !Array.isArray(registros)) {
      return res.status(400).json({
        error: 'Se requiere un array de registros',
      });
    }

    // Llamar a la API Python
    const response = await axios.post(`${PYTHON_API_URL}/tendencias`, {
      registros,
      fecha_columna,
      valor_columna,
    });

    res.json({
      success: true,
      tendencias: response.data.tendencias,
      timestamp: response.data.timestamp,
    });
  } catch (error) {
    console.error('Error en /tendencias:', error.message);
    res.status(500).json({
      error: 'Error al analizar tendencias',
      details: error.message,
    });
  }
});

/**
 * POST /api/analytics/columnas-info
 * Obtener información sobre todas las columnas
 */
router.post('/columnas-info', async (req, res) => {
  try {
    const { registros } = req.body;

    if (!registros || !Array.isArray(registros)) {
      return res.status(400).json({
        error: 'Se requiere un array de registros',
      });
    }

    // Llamar a la API Python
    const response = await axios.post(`${PYTHON_API_URL}/columnas-info`, {
      registros,
    });

    res.json({
      success: true,
      columnas: response.data.columnas_info,
      total_columnas: response.data.total_columnas,
      timestamp: response.data.timestamp,
    });
  } catch (error) {
    console.error('Error en /columnas-info:', error.message);
    res.status(500).json({
      error: 'Error al obtener información de columnas',
      details: error.message,
    });
  }
});

/**
 * GET /api/analytics/health
 * Verificar estado de la API Python
 */
router.get('/health', async (req, res) => {
  try {
    const response = await axios.get(`${PYTHON_API_URL}/health`);

    res.json({
      success: true,
      pythonApi: response.data,
      nodeApi: 'healthy',
      timestamp: new Date(),
    });
  } catch (error) {
    console.warn('⚠️ API Python no disponible:', error.message);
    res.status(503).json({
      success: false,
      nodeApi: 'healthy',
      pythonApi: 'unavailable',
      message: 'Asegúrate de que la API Python esté ejecutándose en ' + PYTHON_API_URL,
    });
  }
});

module.exports = router;

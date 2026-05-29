"""
Re-export del módulo visualizacion desde python-analytics para uso interno
"""
from pathlib import Path
import sys
import importlib.util

src = Path(__file__).resolve().parents[3] / 'python-analytics' / 'visualizacion.py'
spec = importlib.util.spec_from_file_location('pa_visualizacion', str(src))
pa_visualizacion = importlib.util.module_from_spec(spec)
import sys
# Register the module under a stable short name so that other python-analytics
# modules that do `from visualizacion import ...` can find it when loaded via
# importlib.spec_from_file_location.
sys.modules['visualizacion'] = pa_visualizacion
spec.loader.exec_module(pa_visualizacion)

# Re-export classes/functions used by py_backend
VisualizadorDatos = pa_visualizacion.VisualizadorDatos
# Some helper functions are module-level in the original package; others
# are methods of `VisualizadorDatos`. Expose only what's available at
# module level and rely on the class for instance methods.
graficar_frecuencia = getattr(pa_visualizacion, "graficar_frecuencia", None)
graficar_agrupacion = getattr(pa_visualizacion, "graficar_agrupacion", None)

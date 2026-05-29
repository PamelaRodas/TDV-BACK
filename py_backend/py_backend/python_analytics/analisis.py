from pathlib import Path
import sys
import importlib.util

src = Path(__file__).resolve().parents[3] / 'python-analytics' / 'analisis.py'
spec = importlib.util.spec_from_file_location('pa_analisis', str(src))
pa_analisis = importlib.util.module_from_spec(spec)
# Register a stable name used by `python-analytics/reporte.py`
sys.modules['analisis'] = pa_analisis
spec.loader.exec_module(pa_analisis)

AnalizadorDatos = pa_analisis.AnalizadorDatos

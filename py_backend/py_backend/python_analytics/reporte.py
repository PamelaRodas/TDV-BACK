from pathlib import Path
import importlib.util

# Ensure legacy absolute imports inside python-analytics/reporte.py can resolve.
from . import visualizacion as _visualizacion  # noqa: F401
from . import analisis as _analisis  # noqa: F401

src = Path(__file__).resolve().parents[3] / 'python-analytics' / 'reporte.py'
spec = importlib.util.spec_from_file_location('pa_reporte', str(src))
pa_reporte = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pa_reporte)

GeneradorReportes = pa_reporte.GeneradorReportes

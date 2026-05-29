# TDV-BACK Python scaffold

Scaffolded FastAPI backend with route skeletons mirroring the existing Node.js routes.

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Run the app:

```bash
uvicorn py_backend.main:app --reload --port 8000
```

Environment variables can be set in a `.env` file at `py_backend/.env` (MONGO_URI, MONGO_DB, SECRET_KEY).

Resultados / Análisis Visual
-----------------------------
Este backend incluye un módulo de análisis y visualización que genera gráficos (PNG/base64) y reportes HTML.

- Endpoints principales:
	- `POST /api/analytics/analizar` — Ejecuta limpieza y análisis descriptivo sobre los registros JSON.
	- `POST /api/analytics/graficar` — Genera un gráfico y devuelve la imagen en `imagen_base64`.
	- `POST /api/analytics/reporte` — Genera un reporte completo; si se solicita `formato=html` devuelve un archivo HTML con los gráficos.

Integración con React
---------------------
El `imagen_base64` devuelto por `/api/analytics/graficar` puede insertarse directamente en un `img` en React como `src={`data:image/png;base64,${base64}`}`.

Rama y Pull Request
--------------------
Por favor crea una rama para esta funcionalidad y genera un PR a `develop` siguiendo:

```bash
git checkout -b feature/reporte-visual
git add .
git commit -m "feat: add analytics visual reports (python)"
git push origin feature/reporte-visual
# Crear PR desde la plataforma GitHub hacia develop
```

"""
API FastAPI para integración de análisis visual
Conecta Node.js Backend con módulo Python de visualización
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import json
from datetime import datetime
from pathlib import Path
import traceback

from visualizacion import VisualizadorDatos
from analisis import AnalizadorDatos
from reporte import GeneradorReportes

# Crear aplicación FastAPI
app = FastAPI(
    title="TDV Analytics API",
    description="API de análisis y visualización para Manifestation Journal",
    version="1.0.0"
)

# Configurar CORS para conectar con React y Node.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear instancias
visualizador = VisualizadorDatos()
analizador = AnalizadorDatos()
generador = GeneradorReportes()

# ===== RUTAS DE SALUD =====
@app.get("/")
def root():
    """Ruta raíz"""
    return {
        "message": "TDV Analytics API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": [
            "/analizar",
            "/graficar",
            "/reporte",
            "/cargar-csv"
        ]
    }


@app.get("/health")
def health():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


# ===== RUTAS DE ANÁLISIS =====
@app.post("/analizar")
async def analizar_datos(datos: dict):
    """
    Analizar datos en formato JSON
    
    Body: {
        "registros": [{...}, {...}]
    }
    """
    try:
        if not datos.get("registros"):
            raise HTTPException(status_code=400, detail="Se requiere campo 'registros'")
        
        df = pd.DataFrame(datos["registros"])
        analizador.cargar_datos(dataframe=df)
        analizador.limpiar_datos()
        
        estadisticas = analizador.obtener_estadisticas_descriptivas()
        
        return {
            "success": True,
            "estadisticas": estadisticas,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "traceback": traceback.format_exc()}
        )


@app.post("/graficar")
async def generar_grafico(datos: dict):
    """
    Generar un gráfico específico
    
    Body: {
        "registros": [{...}, {...}],
        "tipo": "frecuencia|distribucion|correlacion|pastel|box",
        "columna": "nombre_columna",
        "titulo": "Título opcional"
    }
    """
    try:
        if not datos.get("registros"):
            raise HTTPException(status_code=400, detail="Se requiere 'registros'")
        
        tipo_grafico = datos.get("tipo", "frecuencia")
        columna = datos.get("columna")
        titulo = datos.get("titulo")
        
        df = pd.DataFrame(datos["registros"])
        
        if tipo_grafico == "frecuencia":
            if not columna:
                raise HTTPException(status_code=400, detail="Se requiere 'columna' para frecuencia")
            resultado = visualizador.graficar_frecuencia(df, columna, titulo)
        
        elif tipo_grafico == "distribucion":
            if not columna:
                raise HTTPException(status_code=400, detail="Se requiere 'columna' para distribución")
            resultado = visualizador.graficar_distribucion(df, columna, titulo)
        
        elif tipo_grafico == "correlacion":
            resultado = visualizador.graficar_correlacion(df, titulo)
        
        elif tipo_grafico == "pastel":
            if not columna:
                raise HTTPException(status_code=400, detail="Se requiere 'columna' para pastel")
            resultado = visualizador.graficar_pastel(df, columna, titulo)
        
        elif tipo_grafico == "box":
            if not columna:
                raise HTTPException(status_code=400, detail="Se requiere 'columna' para box plot")
            resultado = visualizador.graficar_box(df, columna, titulo=titulo)
        
        elif tipo_grafico == "tendencia":
            fecha_col = datos.get("fecha_columna", "createdAt")
            valor_col = datos.get("valor_columna")
            resultado = visualizador.graficar_tendencia_temporal(df, fecha_col, valor_col, titulo)
        
        else:
            raise HTTPException(status_code=400, detail=f"Tipo de gráfico desconocido: {tipo_grafico}")
        
        if resultado.get("error"):
            raise HTTPException(status_code=400, detail=resultado["error"])
        
        return {
            "success": True,
            "grafico": {
                "tipo": tipo_grafico,
                "imagen_base64": resultado["base64"],
                "nombre": resultado.get("nombre"),
                "ruta_archivo": resultado.get("path")
            },
            "timestamp": datetime.now().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "traceback": traceback.format_exc()}
        )


@app.post("/reporte")
async def generar_reporte(datos: dict):
    """
    Generar reporte completo con múltiples gráficos
    
    Body: {
        "registros": [{...}, {...}],
        "titulo": "Título del reporte",
        "formato": "json|html"
    }
    """
    try:
        if not datos.get("registros"):
            raise HTTPException(status_code=400, detail="Se requiere 'registros'")
        
        titulo = datos.get("titulo", "Análisis Visual")
        formato = datos.get("formato", "json")
        
        df = pd.DataFrame(datos["registros"])
        
        if formato == "html":
            archivo = generador.exportar_como_html_interactivo(df)
            return FileResponse(archivo, media_type="text/html")
        else:
            reporte = generador.crear_respuesta_api(df, titulo)
            return {
                "success": True,
                "reporte": reporte["data"]["reporte"],
                "estadisticas": reporte["data"]["estadisticas_generales"],
                "timestamp": datetime.now().isoformat()
            }
    
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ===== RUTAS DE CARGA DE DATOS =====
@app.post("/cargar-csv")
async def cargar_csv(file: UploadFile = File(...)):
    """
    Cargar archivo CSV y obtener análisis
    """
    try:
        contenido = await file.read()
        df = pd.read_csv(io.BytesIO(contenido))
        
        analizador.cargar_datos(dataframe=df)
        analizador.limpiar_datos()
        
        estadisticas = analizador.obtener_estadisticas_descriptivas()
        
        return {
            "success": True,
            "archivo": file.filename,
            "registros_cargados": len(df),
            "estadisticas": estadisticas,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ===== RUTAS DE DETECCIÓN DE OUTLIERS =====
@app.post("/outliers")
async def detectar_outliers(datos: dict):
    """
    Detectar valores atípicos en una columna
    
    Body: {
        "registros": [{...}, {...}],
        "columna": "nombre_columna",
        "metodo": "iqr|zscore"
    }
    """
    try:
        if not datos.get("registros"):
            raise HTTPException(status_code=400, detail="Se requiere 'registros'")
        
        if not datos.get("columna"):
            raise HTTPException(status_code=400, detail="Se requiere 'columna'")
        
        df = pd.DataFrame(datos["registros"])
        analizador.cargar_datos(dataframe=df)
        
        metodo = datos.get("metodo", "iqr")
        resultado = analizador.detectar_outliers(datos["columna"], metodo)
        
        return {
            "success": True,
            "outliers": resultado,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ===== RUTAS DE TENDENCIAS =====
@app.post("/tendencias")
async def analizar_tendencias(datos: dict):
    """
    Analizar tendencias temporales
    
    Body: {
        "registros": [{...}, {...}],
        "fecha_columna": "createdAt",
        "valor_columna": "campo_valor"
    }
    """
    try:
        if not datos.get("registros"):
            raise HTTPException(status_code=400, detail="Se requiere 'registros'")
        
        df = pd.DataFrame(datos["registros"])
        analizador.cargar_datos(dataframe=df)
        
        fecha_col = datos.get("fecha_columna", "createdAt")
        valor_col = datos.get("valor_columna")
        
        tendencias = analizador.analizar_tendencias(fecha_col, valor_col)
        
        return {
            "success": True,
            "tendencias": tendencias,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ===== RUTAS DE INFORMACIÓN =====
@app.post("/columnas-info")
async def info_columnas(datos: dict):
    """
    Obtener información sobre todas las columnas
    
    Body: {
        "registros": [{...}, {...}]
    }
    """
    try:
        if not datos.get("registros"):
            raise HTTPException(status_code=400, detail="Se requiere 'registros'")
        
        df = pd.DataFrame(datos["registros"])
        analizador.cargar_datos(dataframe=df)
        
        stats = analizador.obtener_estadisticas_descriptivas()
        
        return {
            "success": True,
            "columnas_info": stats["por_columna"],
            "total_columnas": stats["total_columnas"],
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

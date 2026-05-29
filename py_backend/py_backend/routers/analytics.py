
from fastapi import APIRouter, Request, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from datetime import datetime
import pandas as pd
import traceback

from ..python_analytics.visualizacion import VisualizadorDatos
from ..python_analytics.analisis import AnalizadorDatos
from ..python_analytics.reporte import GeneradorReportes

router = APIRouter()


visualizador = VisualizadorDatos()
analizador = AnalizadorDatos()
generador = GeneradorReportes()


@router.post("/analizar")
async def analizar_datos(datos: dict):
    try:
        if not datos.get("registros"):
            raise HTTPException(status_code=400, detail="Se requiere campo 'registros'")
        df = pd.DataFrame(datos["registros"])
        analizador.cargar_datos(dataframe=df)
        analizador.limpiar_datos()
        estadisticas = analizador.obtener_estadisticas_descriptivas()
        return {"success": True, "estadisticas": estadisticas, "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})


@router.post("/graficar")
async def generar_grafico(datos: dict):
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
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})


@router.post("/reporte")
async def generar_reporte(datos: dict):
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
            return {"success": True, "reporte": reporte["data"]["reporte"], "estadisticas": reporte["data"]["estadisticas_generales"], "timestamp": datetime.now().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})


@router.post("/cargar-csv")
async def cargar_csv(file: UploadFile):
    # This endpoint is optional when frontend uploads CSV directly to python-analytics
    raise HTTPException(status_code=501, detail="Use dedicated python-analytics service for CSV uploads")

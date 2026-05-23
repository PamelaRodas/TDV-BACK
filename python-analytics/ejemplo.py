"""
Ejemplo de uso del módulo Python Analytics
Demuestra cómo utilizar análisis y visualización de datos
"""

import pandas as pd
from datetime import datetime, timedelta
import random
from analisis import crear_analizador
from visualizacion import crear_visualizador
from reporte import crear_generador


def generar_datos_ejemplo():
    """Generar datos de ejemplo para demostración"""
    
    print("🔄 Generando datos de ejemplo...")
    
    datos = []
    fecha_inicio = datetime.now() - timedelta(days=30)
    
    categorias = ['Manifestación', 'Gratitud', 'Reflexión', 'Ritual', 'Meditación']
    estados = ['completado', 'en_progreso', 'pendiente']
    niveles_animo = ['muy_bajo', 'bajo', 'neutral', 'alto', 'muy_alto']
    
    for i in range(50):
        fecha = fecha_inicio + timedelta(days=random.randint(0, 30))
        datos.append({
            'id': i + 1,
            'categoria': random.choice(categorias),
            'contenido': f'Entrada {i+1} del diario',
            'estado': random.choice(estados),
            'nivel_animo': random.choice(niveles_animo),
            'duracion_minutos': random.randint(5, 60),
            'puntuacion': random.uniform(1, 10),
            'createdAt': fecha.isoformat(),
            'tags': ', '.join(random.sample(['amor', 'salud', 'dinero', 'éxito', 'paz'], 2))
        })
    
    return pd.DataFrame(datos)


def ejemplo_1_analisis_basico():
    """Ejemplo 1: Análisis básico de datos"""
    
    print("\n" + "="*60)
    print("EJEMPLO 1: ANÁLISIS BÁSICO DE DATOS")
    print("="*60)
    
    # Generar datos
    df = generar_datos_ejemplo()
    
    # Crear analizador
    analizador = crear_analizador()
    analizador.cargar_datos(dataframe=df)
    analizador.limpiar_datos()
    
    # Obtener estadísticas
    stats = analizador.obtener_estadisticas_descriptivas()
    
    print(f"\n📊 Estadísticas Generales:")
    print(f"   Total de registros: {stats['total_registros']}")
    print(f"   Total de columnas: {stats['total_columnas']}")
    print(f"   Duplicados: {stats['duplicados']}")
    
    print(f"\n📋 Información por columna:")
    for col, info in list(stats['por_columna'].items())[:3]:
        print(f"\n   {col}:")
        if info['tipo'] == 'numérica':
            print(f"      - Tipo: Numérica")
            print(f"      - Media: {info['media']:.2f}")
            print(f"      - Desv. Est.: {info['std']:.2f}")
        else:
            print(f"      - Tipo: Categórica")
            print(f"      - Valores únicos: {info['valores_unicos']}")
            print(f"      - Más común: {info['valor_mas_comun']}")
    
    return df


def ejemplo_2_visualizaciones(df):
    """Ejemplo 2: Generar visualizaciones"""
    
    print("\n" + "="*60)
    print("EJEMPLO 2: GENERAR VISUALIZACIONES")
    print("="*60)
    
    visualizador = crear_visualizador()
    
    # Gráfico de frecuencia
    print("\n📈 Generando gráfico de frecuencia...")
    resultado = visualizador.graficar_frecuencia(df, 'categoria', 'Frecuencia de Categorías')
    if resultado['base64']:
        print(f"   ✅ Gráfico guardado en: {resultado['path']}")
        print(f"   📸 Imagen convertida a Base64 (primeros 100 caracteres):")
        print(f"   {resultado['base64'][:100]}...")
    
    # Gráfico de distribución
    print("\n📊 Generando gráfico de distribución...")
    resultado = visualizador.graficar_distribucion(df, 'puntuacion', 'Distribución de Puntuación')
    if resultado['base64']:
        print(f"   ✅ Gráfico guardado en: {resultado['path']}")
    
    # Gráfico de pastel
    print("\n🥧 Generando gráfico de pastel...")
    resultado = visualizador.graficar_pastel(df, 'estado', 'Estados de Tareas')
    if resultado['base64']:
        print(f"   ✅ Gráfico guardado en: {resultado['path']}")
    
    # Gráfico de tendencia temporal
    print("\n📈 Generando gráfico de tendencia temporal...")
    resultado = visualizador.graficar_tendencia_temporal(df, 'createdAt', None, 'Tendencia de Registros')
    if resultado['base64']:
        print(f"   ✅ Gráfico guardado en: {resultado['path']}")


def ejemplo_3_reporte_completo(df):
    """Ejemplo 3: Generar reporte completo"""
    
    print("\n" + "="*60)
    print("EJEMPLO 3: REPORTE COMPLETO")
    print("="*60)
    
    generador = crear_generador()
    
    # Procesar datos para frontend
    print("\n🔄 Procesando datos para frontend...")
    reporte = generador.procesar_datos_para_frontend(datos=df.to_dict('records'))
    
    print(f"\n📋 Información del Reporte:")
    print(f"   ID: {reporte['id']}")
    print(f"   Gráficos generados: {len(reporte['graficos'])}")
    print(f"   Total de registros: {reporte['estadisticas']['resumen']['total_registros']}")
    
    # Exportar como HTML
    print("\n📄 Generando HTML interactivo...")
    archivo_html = generador.exportar_como_html_interactivo(df, 'reporte_ejemplo.html')
    print(f"   ✅ Archivo HTML guardado en: {archivo_html}")
    
    # Crear respuesta API
    print("\n🔌 Generando respuesta para API...")
    respuesta_api = generador.crear_respuesta_api(df, 'Análisis de Ejemplo')
    print(f"   ✅ Respuesta API preparada")
    print(f"   - Status: {respuesta_api['success']}")
    print(f"   - Gráficos: {len(respuesta_api['data']['reporte']['graficos'])}")
    
    return reporte


def ejemplo_4_deteccion_outliers(df):
    """Ejemplo 4: Detectar valores atípicos"""
    
    print("\n" + "="*60)
    print("EJEMPLO 4: DETECCIÓN DE OUTLIERS")
    print("="*60)
    
    analizador = crear_analizador()
    analizador.cargar_datos(dataframe=df)
    
    print("\n🔍 Detectando outliers en 'puntuacion'...")
    
    # Método IQR
    outliers_iqr = analizador.detectar_outliers('puntuacion', 'iqr')
    print(f"\n   Método IQR:")
    print(f"   - Outliers encontrados: {outliers_iqr['total_outliers']}")
    print(f"   - Porcentaje: {outliers_iqr['porcentaje']:.2f}%")
    
    # Método Z-Score
    outliers_zscore = analizador.detectar_outliers('puntuacion', 'zscore', 2)
    print(f"\n   Método Z-Score:")
    print(f"   - Outliers encontrados: {outliers_zscore['total_outliers']}")
    print(f"   - Porcentaje: {outliers_zscore['porcentaje']:.2f}%")


def main():
    """Función principal"""
    
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + "  TDV ANALYTICS - EJEMPLOS DE USO".center(58) + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    
    try:
        # Ejecutar ejemplos
        df = ejemplo_1_analisis_basico()
        ejemplo_2_visualizaciones(df)
        ejemplo_3_reporte_completo(df)
        ejemplo_4_deteccion_outliers(df)
        
        print("\n" + "="*60)
        print("✅ TODOS LOS EJEMPLOS COMPLETADOS EXITOSAMENTE")
        print("="*60)
        
        print("\n📁 Archivos generados guardados en: ./reportes/")
        print("\n💡 Próximos pasos:")
        print("   1. Revisar los gráficos generados en ./reportes/")
        print("   2. Abrir reporte_ejemplo.html en un navegador")
        print("   3. Ejecutar la API con: python api.py")
        print("   4. Integrar con React/Frontend")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

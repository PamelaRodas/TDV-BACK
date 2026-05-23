"""
Módulo de Análisis de Datos
Análisis estadístico y limpieza de datos del Manifestation Journal
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
from pathlib import Path


class AnalizadorDatos:
    """Clase para análisis estadístico de datos"""
    
    def __init__(self):
        """Inicializar el analizador"""
        self.df = None
        self.estadisticas = {}
    
    def cargar_datos(self, ruta_csv=None, dataframe=None):
        """
        Cargar datos desde CSV o DataFrame
        
        Args:
            ruta_csv (str): Ruta al archivo CSV
            dataframe (pd.DataFrame): DataFrame directamente
            
        Returns:
            pd.DataFrame: Datos cargados
        """
        if dataframe is not None:
            self.df = dataframe.copy()
        elif ruta_csv:
            self.df = pd.read_csv(ruta_csv)
        else:
            raise ValueError('Debe proporcionar ruta_csv o dataframe')
        
        return self.df
    
    def limpiar_datos(self, eliminar_duplicados=True, llenar_nulos=True):
        """
        Limpiar datos: eliminar duplicados y manejar valores nulos
        
        Args:
            eliminar_duplicados (bool): Eliminar filas duplicadas
            llenar_nulos (bool): Llenar valores nulos
            
        Returns:
            pd.DataFrame: Datos limpios
        """
        if self.df is None:
            raise ValueError('No hay datos cargados')
        
        df_limpio = self.df.copy()
        
        # Registrar limpieza
        registros_iniciales = len(df_limpio)
        
        if eliminar_duplicados:
            df_limpio = df_limpio.drop_duplicates()
        
        if llenar_nulos:
            # Para columnas numéricas, usar la media
            for col in df_limpio.select_dtypes(include=[np.number]).columns:
                df_limpio[col].fillna(df_limpio[col].mean(), inplace=True)
            
            # Para columnas categóricas, usar el modo o 'Sin especificar'
            for col in df_limpio.select_dtypes(include=['object']).columns:
                if df_limpio[col].isna().any():
                    moda = df_limpio[col].mode()
                    if not moda.empty:
                        df_limpio[col].fillna(moda[0], inplace=True)
                    else:
                        df_limpio[col].fillna('Sin especificar', inplace=True)
        
        self.estadisticas['limpieza'] = {
            'registros_iniciales': registros_iniciales,
            'registros_finales': len(df_limpio),
            'duplicados_eliminados': registros_iniciales - len(df_limpio),
            'timestamp': datetime.now().isoformat()
        }
        
        self.df = df_limpio
        return self.df
    
    def obtener_estadisticas_descriptivas(self):
        """
        Calcular estadísticas descriptivas
        
        Returns:
            dict: Estadísticas del dataset
        """
        if self.df is None:
            raise ValueError('No hay datos cargados')
        
        stats = {
            'total_registros': len(self.df),
            'total_columnas': len(self.df.columns),
            'columnas': list(self.df.columns),
            'tipos_datos': self.df.dtypes.to_dict(),
            'valores_nulos': self.df.isnull().sum().to_dict(),
            'duplicados': self.df.duplicated().sum(),
            'memoria_uso_mb': self.df.memory_usage(deep=True).sum() / 1024**2
        }
        
        # Estadísticas por columna
        stats['por_columna'] = {}
        
        for col in self.df.columns:
            if self.df[col].dtype in ['int64', 'float64']:
                stats['por_columna'][col] = {
                    'tipo': 'numérica',
                    'media': float(self.df[col].mean()),
                    'mediana': float(self.df[col].median()),
                    'std': float(self.df[col].std()),
                    'min': float(self.df[col].min()),
                    'max': float(self.df[col].max()),
                    'q25': float(self.df[col].quantile(0.25)),
                    'q75': float(self.df[col].quantile(0.75))
                }
            else:
                stats['por_columna'][col] = {
                    'tipo': 'categórica',
                    'valores_unicos': int(self.df[col].nunique()),
                    'valor_mas_comun': str(self.df[col].mode()[0]) if not self.df[col].mode().empty else None,
                    'frecuencia_max': int(self.df[col].value_counts().iloc[0]) if not self.df[col].value_counts().empty else 0
                }
        
        self.estadisticas['descriptivas'] = stats
        return stats
    
    def analizar_tendencias(self, columna_fecha='createdAt', columna_valor=None):
        """
        Analizar tendencias temporales
        
        Args:
            columna_fecha (str): Nombre de la columna con fechas
            columna_valor (str): Columna a analizar (None = contar registros)
            
        Returns:
            dict: Análisis de tendencias
        """
        if self.df is None:
            raise ValueError('No hay datos cargados')
        
        if columna_fecha not in self.df.columns:
            return {'error': f'Columna {columna_fecha} no encontrada'}
        
        df_copy = self.df.copy()
        df_copy[columna_fecha] = pd.to_datetime(df_copy[columna_fecha], errors='coerce')
        df_copy = df_copy.dropna(subset=[columna_fecha])
        
        tendencias = {
            'fecha_inicio': str(df_copy[columna_fecha].min()),
            'fecha_fin': str(df_copy[columna_fecha].max()),
            'dias_totales': (df_copy[columna_fecha].max() - df_copy[columna_fecha].min()).days,
        }
        
        if columna_valor and columna_valor in self.df.columns:
            agrupado = df_copy.groupby(df_copy[columna_fecha].dt.date)[columna_valor].sum()
            tendencias['valor_total'] = float(agrupado.sum())
            tendencias['valor_promedio_diario'] = float(agrupado.mean())
        else:
            agrupado = df_copy.groupby(df_copy[columna_fecha].dt.date).size()
            tendencias['total_registros'] = int(agrupado.sum())
            tendencias['promedio_diario'] = float(agrupado.mean())
        
        self.estadisticas['tendencias'] = tendencias
        return tendencias
    
    def detectar_outliers(self, columna, metodo='iqr', threshold=1.5):
        """
        Detectar valores atípicos
        
        Args:
            columna (str): Columna a analizar
            metodo (str): 'iqr' o 'zscore'
            threshold (float): Umbral para detección
            
        Returns:
            dict: Información sobre outliers
        """
        if self.df is None or columna not in self.df.columns:
            return {'error': 'Columna no encontrada'}
        
        datos = self.df[columna].dropna()
        
        if metodo == 'iqr':
            Q1 = datos.quantile(0.25)
            Q3 = datos.quantile(0.75)
            IQR = Q3 - Q1
            limite_inf = Q1 - threshold * IQR
            limite_sup = Q3 + threshold * IQR
            
            outliers = datos[(datos < limite_inf) | (datos > limite_sup)]
        else:  # zscore
            from scipy import stats
            z_scores = np.abs(stats.zscore(datos))
            outliers = datos[z_scores > threshold]
        
        return {
            'metodo': metodo,
            'total_outliers': len(outliers),
            'porcentaje': (len(outliers) / len(datos) * 100) if len(datos) > 0 else 0,
            'valores': outliers.tolist()[:10]  # Primeros 10
        }
    
    def correlaciones(self):
        """
        Calcular matriz de correlaciones
        
        Returns:
            pd.DataFrame: Matriz de correlación
        """
        if self.df is None:
            raise ValueError('No hay datos cargados')
        
        df_numeric = self.df.select_dtypes(include=[np.number])
        if df_numeric.empty:
            return None
        
        correlacion = df_numeric.corr()
        self.estadisticas['correlacion'] = correlacion.to_dict()
        return correlacion
    
    def exportar_resultados(self, archivo_salida='analisis_resultados.json'):
        """
        Exportar resultados del análisis a JSON
        
        Args:
            archivo_salida (str): Ruta del archivo de salida
            
        Returns:
            str: Ruta del archivo creado
        """
        resultados = {
            'fecha_analisis': datetime.now().isoformat(),
            'estadisticas': self.estadisticas
        }
        
        # Convertir tipos de numpy a tipos nativos de Python
        def convertir_tipos(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convertir_tipos(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convertir_tipos(item) for item in obj]
            return obj
        
        resultados = convertir_tipos(resultados)
        
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)
        
        return archivo_salida
    
    def obtener_resumen(self):
        """
        Obtener resumen completo del análisis
        
        Returns:
            dict: Resumen de análisis
        """
        return {
            'estadisticas_descriptivas': self.obtener_estadisticas_descriptivas(),
            'tendencias': self.estadisticas.get('tendencias', {}),
            'limpieza': self.estadisticas.get('limpieza', {}),
            'timestamp': datetime.now().isoformat()
        }


def crear_analizador():
    """Factory para crear instancia del analizador"""
    return AnalizadorDatos()

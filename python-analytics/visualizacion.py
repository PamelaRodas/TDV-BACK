# visualizacion.py
"""
Módulo para la generación de gráficos y visualizaciones.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

def graficar_frecuencia(dataframe, columna, titulo="Frecuencia de elementos", xlabel="Elemento", ylabel="Frecuencia"):
    plt.figure(figsize=(10, 6))
    conteo = dataframe[columna].value_counts()
    ax = sns.barplot(x=conteo.index, y=conteo.values)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='svg')
    plt.close()
    buf.seek(0)
    return buf.getvalue().decode('utf-8')


def graficar_agrupacion(dataframe, columna_agrupacion, columna_valor, titulo="Agrupación", xlabel="Grupo", ylabel="Valor"):
    plt.figure(figsize=(10, 6))
    agrupado = dataframe.groupby(columna_agrupacion)[columna_valor].sum().sort_values(ascending=False)
    ax = sns.barplot(x=agrupado.index, y=agrupado.values)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='svg')
    plt.close()
    buf.seek(0)
    return buf.getvalue().decode('utf-8')

# ---

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from datetime import datetime
import json
from pathlib import Path

# Configurar estilo de gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class VisualizadorDatos:
    """Clase para generar visualizaciones de datos del diario"""
    
    def __init__(self, output_dir='reportes'):
        """
        Inicializar el visualizador
        
        Args:
            output_dir (str): Directorio para guardar reportes
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def graficar_frecuencia(self, dataframe, columna, titulo=None, top_n=10):
        """
        Generar gráfico de barras mostrando elementos más comunes
        
        Args:
            dataframe (pd.DataFrame): DataFrame con los datos
            columna (str): Nombre de la columna a analizar
            titulo (str): Título del gráfico
            top_n (int): Top N elementos a mostrar
            
        Returns:
            dict: Contiene 'base64' (imagen en base64) y 'path' (ruta del archivo)
        """
        if dataframe.empty:
            return {'base64': None, 'path': None, 'error': 'DataFrame vacío'}
        
        # Contar frecuencias
        frecuencias = dataframe[columna].value_counts().head(top_n)
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 6))
        frecuencias.plot(kind='bar', ax=ax, color='#8B7BA8', edgecolor='black')
        
        # Configurar etiquetas
        ax.set_xlabel(columna, fontsize=12, fontweight='bold')
        ax.set_ylabel('Frecuencia', fontsize=12, fontweight='bold')
        ax.set_title(titulo or f'Frecuencia de {columna}', fontsize=14, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        
        # Guardar en archivo y en base64
        return self._guardar_grafico(fig, f'frecuencia_{columna}_{self.timestamp}')
    
    def graficar_tendencia_temporal(self, dataframe, fecha_columna='createdAt', 
                                   valor_columna=None, titulo=None):
        """
        Generar gráfico de tendencia temporal
        
        Args:
            dataframe (pd.DataFrame): DataFrame con los datos
            fecha_columna (str): Nombre de la columna de fecha
            valor_columna (str): Nombre de la columna con valores (si es None, cuenta registros)
            titulo (str): Título del gráfico
            
        Returns:
            dict: Contiene 'base64' y 'path'
        """
        if dataframe.empty:
            return {'base64': None, 'path': None, 'error': 'DataFrame vacío'}
        
        # Convertir a datetime
        df_copy = dataframe.copy()
        df_copy[fecha_columna] = pd.to_datetime(df_copy[fecha_columna])
        df_copy = df_copy.sort_values(fecha_columna)
        
        # Agrupar por fecha
        if valor_columna:
            tendencia = df_copy.groupby(df_copy[fecha_columna].dt.date)[valor_columna].sum()
        else:
            tendencia = df_copy.groupby(df_copy[fecha_columna].dt.date).size()
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(tendencia.index, tendencia.values, marker='o', linestyle='-', 
                color='#6B4C9A', linewidth=2, markersize=6)
        ax.fill_between(range(len(tendencia)), tendencia.values, alpha=0.3, color='#6B4C9A')
        
        # Configurar etiquetas
        ax.set_xlabel('Fecha', fontsize=12, fontweight='bold')
        ax.set_ylabel('Cantidad' if not valor_columna else valor_columna, 
                     fontsize=12, fontweight='bold')
        ax.set_title(titulo or 'Tendencia Temporal', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return self._guardar_grafico(fig, f'tendencia_{self.timestamp}')
    
    def graficar_distribucion(self, dataframe, columna, titulo=None):
        """
        Generar gráfico de distribución (histograma)
        
        Args:
            dataframe (pd.DataFrame): DataFrame con los datos
            columna (str): Nombre de la columna numérica
            titulo (str): Título del gráfico
            
        Returns:
            dict: Contiene 'base64' y 'path'
        """
        if dataframe.empty:
            return {'base64': None, 'path': None, 'error': 'DataFrame vacío'}
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 6))
        df_clean = dataframe[columna].dropna()
        
        ax.hist(df_clean, bins=20, color='#8B7BA8', edgecolor='black', alpha=0.7)
        ax.set_xlabel(columna, fontsize=12, fontweight='bold')
        ax.set_ylabel('Frecuencia', fontsize=12, fontweight='bold')
        ax.set_title(titulo or f'Distribución de {columna}', fontsize=14, fontweight='bold')
        
        # Añadir línea de media
        media = df_clean.mean()
        ax.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Media: {media:.2f}')
        ax.legend()
        
        plt.tight_layout()
        return self._guardar_grafico(fig, f'distribucion_{columna}_{self.timestamp}')
    
    def graficar_correlacion(self, dataframe, titulo=None):
        """
        Generar mapa de calor de correlación
        
        Args:
            dataframe (pd.DataFrame): DataFrame con datos numéricos
            titulo (str): Título del gráfico
            
        Returns:
            dict: Contiene 'base64' y 'path'
        """
        if dataframe.empty:
            return {'base64': None, 'path': None, 'error': 'DataFrame vacío'}
        
        # Seleccionar solo columnas numéricas
        df_numeric = dataframe.select_dtypes(include=['number'])
        
        if df_numeric.empty or len(df_numeric.columns) < 2:
            return {'base64': None, 'path': None, 'error': 'No hay suficientes columnas numéricas'}
        
        # Calcular correlación
        correlacion = df_numeric.corr()
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlacion, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, ax=ax, cbar_kws={'label': 'Correlación'})
        ax.set_title(titulo or 'Matriz de Correlación', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        return self._guardar_grafico(fig, f'correlacion_{self.timestamp}')
    
    def graficar_pastel(self, dataframe, columna, titulo=None, top_n=8):
        """
        Generar gráfico de pastel
        
        Args:
            dataframe (pd.DataFrame): DataFrame con los datos
            columna (str): Nombre de la columna a analizar
            titulo (str): Título del gráfico
            top_n (int): Top N elementos a mostrar
            
        Returns:
            dict: Contiene 'base64' y 'path'
        """
        if dataframe.empty:
            return {'base64': None, 'path': None, 'error': 'DataFrame vacío'}
        
        # Contar valores
        conteos = dataframe[columna].value_counts().head(top_n)
        otros = dataframe[columna].value_counts()[top_n:].sum()
        
        if otros > 0:
            conteos = pd.concat([conteos, pd.Series({'Otros': otros})])
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = plt.cm.Set3(range(len(conteos)))
        wedges, texts, autotexts = ax.pie(conteos.values, labels=conteos.index, 
                                           autopct='%1.1f%%', colors=colors,
                                           startangle=90)
        
        # Mejorar formato
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
        
        ax.set_title(titulo or f'Distribución de {columna}', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        return self._guardar_grafico(fig, f'pastel_{columna}_{self.timestamp}')
    
    def graficar_box(self, dataframe, columna_y, columna_x=None, titulo=None):
        """
        Generar gráfico de caja (box plot)
        
        Args:
            dataframe (pd.DataFrame): DataFrame con los datos
            columna_y (str): Columna con valores numéricos
            columna_x (str): Columna de agrupación (opcional)
            titulo (str): Título del gráfico
            
        Returns:
            dict: Contiene 'base64' y 'path'
        """
        if dataframe.empty:
            return {'base64': None, 'path': None, 'error': 'DataFrame vacío'}
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if columna_x:
            sns.boxplot(data=dataframe, x=columna_x, y=columna_y, ax=ax, palette='Set2')
        else:
            sns.boxplot(data=dataframe, y=columna_y, ax=ax, palette='Set2')
        
        ax.set_title(titulo or f'Box Plot de {columna_y}', fontsize=14, fontweight='bold')
        if columna_x:
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        return self._guardar_grafico(fig, f'box_{columna_y}_{self.timestamp}')
    
    def _guardar_grafico(self, fig, nombre_base):
        """
        Guardar gráfico en archivo y convertir a base64
        
        Args:
            fig: Figura de matplotlib
            nombre_base (str): Nombre base del archivo
            
        Returns:
            dict: Contiene 'base64' (string) y 'path' (ruta del archivo)
        """
        try:
            # Guardar como PNG
            png_path = self.output_dir / f'{nombre_base}.png'
            fig.savefig(png_path, dpi=150, bbox_inches='tight', facecolor='white')
            
            # Convertir a base64
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            
            plt.close(fig)
            
            return {
                'base64': image_base64,
                'path': str(png_path),
                'nombre': f'{nombre_base}.png'
            }
        except Exception as e:
            plt.close(fig)
            return {'base64': None, 'path': None, 'error': str(e)}
    
    def generar_reporte_completo(self, dataframe, titulo_reporte='Reporte de Análisis'):
        """
        Generar reporte múltiple con varios gráficos
        
        Args:
            dataframe (pd.DataFrame): DataFrame con los datos
            titulo_reporte (str): Título del reporte
            
        Returns:
            dict: Contiene información de todos los gráficos generados
        """
        reporte = {
            'titulo': titulo_reporte,
            'timestamp': datetime.now().isoformat(),
            'estadisticas': {
                'total_registros': len(dataframe),
                'columnas': list(dataframe.columns)
            },
            'graficos': {}
        }
        
        # Generar gráficos para cada columna categórica
        for columna in dataframe.select_dtypes(include=['object']).columns:
            if dataframe[columna].nunique() <= 20:
                reporte['graficos'][f'frecuencia_{columna}'] = \
                    self.graficar_frecuencia(dataframe, columna, 
                                           titulo=f'Análisis: {columna}')
        
        # Generar gráficos para columnas numéricas
        for columna in dataframe.select_dtypes(include=['number']).columns:
            if dataframe[columna].nunique() > 1:
                reporte['graficos'][f'distribucion_{columna}'] = \
                    self.graficar_distribucion(dataframe, columna,
                                              titulo=f'Distribución: {columna}')
        
        # Gráfico de correlación si hay múltiples numéricas
        if len(dataframe.select_dtypes(include=['number']).columns) >= 2:
            reporte['graficos']['correlacion'] = self.graficar_correlacion(dataframe)
        
        return reporte


def crear_visualizador():
    """Factory para crear instancia del visualizador"""
    return VisualizadorDatos()

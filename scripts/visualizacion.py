import re
import json
import os
import io
import base64
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')


def load_js_array(js_path):
    """Carga un arreglo exportado desde un fichero JS (export const name = [ ... ]) y devuelve una lista de dicts."""
    txt = open(js_path, 'r', encoding='utf-8').read()
    # Extraer desde el primer '[' hasta el correspondiente '];' final
    start = txt.find('[')
    end = txt.rfind(']')
    if start == -1 or end == -1:
        raise ValueError(f'No se encontró un arreglo en {js_path}')
    arr_text = txt[start:end+1]
    # Intentar parsear directamente como JSON
    try:
        return json.loads(arr_text)
    except Exception:
            fixed = re.sub(r'([\{\,\s])(\w+)\s*:', r'\1"\2":', arr_text)
            try:
                data = json.loads(fixed)
                return data
            except Exception:
                # Último recurso: parseo manual por objetos (más tolerante a comillas internas)
                objs = re.finditer(r'\{(.*?)\}', arr_text, re.DOTALL)
                results = []
                for m in objs:
                    txt = m.group(1)
                    obj = {}
                    for line in txt.splitlines():
                        line = line.strip().rstrip(',')
                        if not line or ':' not in line:
                            continue
                        k, v = line.split(':', 1)
                        key = k.strip().strip('"').strip("'")
                        val = v.strip()
                        # quitar comillas externas si existen
                        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                            val = val[1:-1]
                        obj[key] = val
                    if obj:
                        results.append(obj)
                return results


def df_from_js(js_path):
    data = load_js_array(js_path)
    return pd.DataFrame(data)


def fig_to_data_uri(fig, fmt='png'):
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    return f"data:image/{fmt};base64,{img_b64}"


def graficar_frecuencia(df, column='label', title='Frecuencia de elementos'):
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, 'count']
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=counts, x='count', y=column, palette='viridis', ax=ax)
    ax.set_title(title)
    ax.set_xlabel('Cantidad')
    ax.set_ylabel(column.capitalize())
    return fig_to_data_uri(fig)


def graficar_longitud_texto(df, text_col='text', title='Distribución de longitud de texto'):
    if text_col not in df.columns:
        raise ValueError(f'Columna {text_col} no encontrada')
    df = df.copy()
    df['length'] = df[text_col].astype(str).map(len)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df['length'], bins=10, kde=False, color='#6a2c70', ax=ax)
    ax.set_title(title)
    ax.set_xlabel('Longitud (caracteres)')
    ax.set_ylabel('Frecuencia')
    return fig_to_data_uri(fig)


def df_to_group_table_html(df, group_by='label'):
    grp = df.groupby(group_by).size().reset_index(name='count')
    return grp.to_html(index=False, classes='dataframe', table_id='group-table')


def photos_table_html(df):
    df2 = df.copy()
    # Insertar imagenes como tags HTML
    df2['image'] = df2['image'].apply(lambda url: f'<img src="{url}" alt="img" style="max-width:120px;">')
    return df2.to_html(index=False, escape=False, classes='dataframe', table_id='photos-table')

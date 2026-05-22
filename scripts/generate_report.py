import os
import sys
# Asegurar que el directorio del script esté en sys.path para importar el módulo local
sys.path.insert(0, os.path.dirname(__file__))
from visualizacion import df_from_js, graficar_frecuencia, graficar_longitud_texto, df_to_group_table_html, photos_table_html

HERE = os.path.dirname(__file__)

# Intentar localizar los datos en el frontend adjunto (posibles rutas)
possible_diary = [
  os.path.normpath(os.path.join(HERE, '..', '..', 'TVD', 'src', 'data', 'diaryEntries.js')),
  os.path.normpath(os.path.join(HERE, '..', '..', '..', 'TDV FRONT', 'TVD', 'src', 'data', 'diaryEntries.js')),
  os.path.normpath(os.path.join(HERE, '..', '..', '..', 'TDV-FRONT', 'TVD', 'src', 'data', 'diaryEntries.js')),
  os.path.normpath(os.path.join(HERE, '..', '..', '..', 'TDV FRONT', 'src', 'data', 'diaryEntries.js')),
]
possible_photos = [p.replace('diaryEntries.js', 'photoMoments.js') for p in possible_diary]

DIARY_JS = next((p for p in possible_diary if os.path.exists(p)), None)
PHOTOS_JS = next((p for p in possible_photos if os.path.exists(p)), None)

if not DIARY_JS or not PHOTOS_JS:
  # Ruta absoluta alternativa (cuando el front fue pasado como carpeta adjunta en el mismo nivel)
  alt1 = os.path.normpath(r'c:\Users\CESDE\Desktop\TDV FRONT\TVD\src\data\diaryEntries.js')
  alt2 = os.path.normpath(r'c:\Users\CESDE\Desktop\TDV FRONT\TVD\src\data\photoMoments.js')
  if os.path.exists(alt1) and os.path.exists(alt2):
    DIARY_JS = alt1
    PHOTOS_JS = alt2


OUTPUT = os.path.join(HERE, 'reporte.html')
ESTILOS_PATH = os.path.join(HERE, 'estilos.css')


def generate_report(output_path=OUTPUT):
    df_diary = df_from_js(DIARY_JS)
    df_photos = df_from_js(PHOTOS_JS)

    img1 = graficar_frecuencia(df_diary, column='label', title='Frecuencia por etiqueta (diarios)')
    img2 = graficar_longitud_texto(df_diary, text_col='text', title='Longitud de entradas de diario')

    table_html = df_to_group_table_html(df_diary, group_by='label')
    photos_html = photos_table_html(df_photos)

    # Leer estilos
    css = ''
    if os.path.exists(ESTILOS_PATH):
        css = open(ESTILOS_PATH, 'r', encoding='utf-8').read()

    html = f"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Reporte Visual - TDV</title>
  <style>
  {css}
  </style>
  <!-- DataTables (CDN) -->
  <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
  <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
  <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
</head>
<body>
  <div class="container">
    <h1>Reporte Visual - TDV</h1>
    <section>
      <h2>Gráficos</h2>
      <div class="fig">
        <h3>Frecuencia por etiqueta</h3>
        <img src="{img1}" alt="frecuencia">
      </div>
      <div class="fig">
        <h3>Distribución de longitud de texto</h3>
        <img src="{img2}" alt="longitud">
      </div>
    </section>

    <section>
      <h2>Tabla: Conteo por etiqueta</h2>
      {table_html}
    </section>

    <section>
      <h2>Fotos (muestra)</h2>
      {photos_html}
    </section>
  </div>

  <script>
    $(document).ready(function(){{
      $('#group-table').DataTable();
      $('#photos-table').DataTable();
    }});
  </script>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Reporte generado en', output_path)


if __name__ == '__main__':
    generate_report()

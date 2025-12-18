import pandas as pd

# 1. Cargar el archivo CSV (detectando automáticamente el separador correcto)
# Nota: El archivo subido 'fires_all_transformado.csv' usa comas, no punto y coma.
df = pd.read_csv('..data/fires_all_transformado.csv')

# 2. Agrupar por municipio y calcular el centroide (promedio de coordenadas)
# Esto cumple tu petición de usar la lat/lng del municipio y no de un incendio suelto.
df_resultado = df.groupby('municipio')[['lat', 'lng']].mean().reset_index()

# 3. Crear la columna con la URL funcional de Google Maps
df_resultado['url_maps'] = df_resultado.apply(
    lambda fila: f"https://www.google.com/maps?q=...8{fila['lat']},{fila['lng']}",
    axis=1
)

# 4. Guardar el resultado
nombre_salida = 'municipios_incendios_maps.csv'
df_resultado.to_csv(nombre_salida, index=False, sep=';')

print(f"Archivo generado: {nombre_salida}")
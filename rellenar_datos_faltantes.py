import pandas as pd

# Leer CSV interpretando '' como NaN
df = pd.read_csv(
    './data/datos_climatologicos_por_provincia.csv',
    delimiter=';',
    na_values=['', ' ', 'NA', 'null']
)

# Calcular medias
media_max = df['Temperatura_Maxima'].mean()
media_min = df['Temperatura_Minima'].mean()

# Truncar medias a 1 decimal
media_max = int(media_max * 10) / 10
media_min = int(media_min * 10) / 10

# Rellenar faltantes
df['Temperatura_Maxima'] = df['Temperatura_Maxima'].fillna(media_max)
df['Temperatura_Minima'] = df['Temperatura_Minima'].fillna(media_min)

# Guardar resultado
df.to_csv('datos_climatologicos_por_provincia_rellenados.csv', index=False)

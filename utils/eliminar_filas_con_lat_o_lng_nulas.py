import pandas as pd

# Leer el CSV
df = pd.read_csv('fires_all_transformado.csv', sep=';')

# Eliminar filas con valores faltantes en lat o lng
df = df.dropna(subset=['lat', 'lng'])

# Guardar resultado (opcional)
df.to_csv('fires_all_transformado.csv', sep=",", index=False)
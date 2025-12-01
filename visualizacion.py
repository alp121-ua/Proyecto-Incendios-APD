import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
import os

# Nombre del archivo (asegúrate de que esté en la misma carpeta o ajusta la ruta)
archivo_datos = 'data/fires_all_transformado.csv'

# 1. CARGAR DATOS
# ---------------------------------------------------------
if os.path.exists(archivo_datos):
    print(f"Cargando datos de {archivo_datos}...")
    # CORRECCIÓN: Este archivo usa comas (sep=',') por defecto
    df = pd.read_csv(archivo_datos)
else:
    # Intento de cargar desde carpeta data/ si no está en la raíz
    df = pd.read_csv(f'data/{archivo_datos}')

# CORRECCIÓN: dayfirst=True es crucial para fechas europeas (DD/MM/YYYY)
df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True)

# Configurar el estilo de los gráficos
sns.set_theme(style="whitegrid")
plt.figure(figsize=(15, 12))

# 2. GRÁFICO 1: TOP 10 MUNICIPIOS CON MÁS INCENDIOS
# ---------------------------------------------------------
print("Generando gráfico de municipios...")
plt.subplot(2, 1, 1)

top_municipios = df['municipio'].value_counts().head(10)

# Graficar
barplot = sns.barplot(
    x=top_municipios.values, 
    y=top_municipios.index, 
    hue=top_municipios.index, 
    palette="viridis", 
    legend=False # Si da error en versiones antiguas, borrar esta línea
)
plt.title('Top 10 Municipios con más Incendios', fontsize=16)
plt.xlabel('Número de Incendios')
plt.ylabel('Municipio')

# Etiquetas de valor
for i, v in enumerate(top_municipios.values):
    barplot.text(v + 0.5, i, str(v), color='black', va='center')


# 3. GRÁFICO 2: EVOLUCIÓN TEMPORAL
# ---------------------------------------------------------
print("Generando gráfico temporal...")
plt.subplot(2, 1, 2)

# Agrupar por mes ('ME' es Month End en pandas nuevo, 'M' en antiguos)
try:
    incendios_por_mes = df.set_index('fecha').resample('ME').size()
except ValueError:
    incendios_por_mes = df.set_index('fecha').resample('M').size()

incendios_por_mes.plot(kind='line', color='#d62728', linewidth=2, marker='o')
plt.title('Evolución de Incendios a lo largo del tiempo', fontsize=16)
plt.xlabel('Fecha')
plt.ylabel('Cantidad de Incendios')
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('estadisticas_incendios.png')
print("Gráfico 'estadisticas_incendios.png' guardado.")


# 4. GRÁFICO 3: MAPA DE CALOR INTERACTIVO
# ---------------------------------------------------------
print("Generando mapa interactivo...")

# Limpiar datos: eliminar filas sin coordenadas
df_map = df.dropna(subset=['lat', 'lng'])

if not df_map.empty:
    # Centrar el mapa en el promedio de las coordenadas de los incendios
    mapa = folium.Map(location=[df_map['lat'].mean(), df_map['lng'].mean()], zoom_start=9)

    # Capa de Calor
    heat_data = df_map[['lat', 'lng']].values.tolist()
    HeatMap(heat_data, radius=15, blur=10).add_to(mapa)

    # Opcional: Marcadores (limitado a los últimos 500 para no saturar el mapa si son muchos)
    # Si quieres ver TODOS, quita el .head(500)
    for _, row in df_map.head(500).iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lng']],
            radius=2,
            color='red',
            fill=True,
            popup=f"{row['municipio']} ({row['fecha'].date()})"
        ).add_to(mapa)

    mapa.save('mapa_incendios.html')
    print("Mapa 'mapa_incendios.html' guardado.")
else:
    print("No hay datos de coordenadas válidos.")
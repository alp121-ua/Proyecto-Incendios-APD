import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap, FastMarkerCluster
import os


archivo_datos = 'data/fires_all_transformado.csv'
nombre_graficos = 'estadisticas_incendios_completo.png'
nombre_mapa = 'mapa_incendios_final.html'


print(f"Cargando datos de {archivo_datos}...")

if not os.path.exists(archivo_datos):
    print(f"ERROR: No encuentro el archivo '{archivo_datos}'. Verifica la ruta.")
    exit()

try:
    df = pd.read_csv(archivo_datos)
    df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True)
    
    df_map = df.dropna(subset=['lat', 'lng'])
    print(f"Datos cargados correctamente: {len(df)} registros total.")

except Exception as e:
    print(f"Error crítico cargando datos: {e}")
    exit()


print("Generando panel de estadísticas...")

sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 18)) 


plt.subplot(3, 1, 1)
top_municipios = df['municipio'].value_counts().head(10)
barplot = sns.barplot(
    x=top_municipios.values, 
    y=top_municipios.index, 
    hue=top_municipios.index, 
    palette="viridis", 
    legend=False
)
plt.title('Top 10 Municipios con más Incendios', fontsize=15)
plt.xlabel('Cantidad de Incendios')
plt.bar_label(barplot.containers[0], padding=3)


plt.subplot(3, 1, 2)

try:
    incendios_mes = df.set_index('fecha').resample('ME').size()
except ValueError:
    incendios_mes = df.set_index('fecha').resample('M').size()

incendios_mes.plot(kind='line', color='#d62728', linewidth=1.5)
plt.title('Evolución Histórica de Incendios', fontsize=15)
plt.xlabel('Fecha')
plt.ylabel('Cantidad')
plt.grid(True, linestyle='--', alpha=0.5)

plt.subplot(3, 1, 3)


conteo_estacion = df['estacion'].value_counts()

sns.barplot(
    x=conteo_estacion.index, 
    y=conteo_estacion.values, 
    hue=conteo_estacion.index,
    palette="magma", 
    legend=False
)
plt.title('Distribución de Incendios por Estación del Año', fontsize=15)
plt.xlabel('Estación')
plt.ylabel('Cantidad de Incendios')


for i, v in enumerate(conteo_estacion.values):
    plt.text(i, v + 50, str(v), ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig(nombre_graficos)
print(f"Gráficos guardados en '{nombre_graficos}'")


print("Generando mapa interactivo...")

if not df_map.empty:
    centro_lat = df_map['lat'].mean()
    centro_lng = df_map['lng'].mean()
    
    mapa = folium.Map(location=[centro_lat, centro_lng], zoom_start=8, tiles='CartoDB positron')

    
    print(" - Añadiendo capa de calor...")
    heat_data = df_map[['lat', 'lng']].values.tolist()
    HeatMap(heat_data, radius=14, blur=18, name="Mapa de Calor").add_to(mapa)

    
    print(f" - Añadiendo {len(df_map)} puntos al mapa...")
    puntos_cluster = df_map[['lat', 'lng']].values.tolist()
    
    FastMarkerCluster(
        puntos_cluster,
        name="Puntos (Agrupados)",
    ).add_to(mapa)

    folium.LayerControl().add_to(mapa)
    mapa.save(nombre_mapa)
    print(f"Mapa guardado en '{nombre_mapa}'.")
else:
    print("No hay datos válidos para el mapa.")
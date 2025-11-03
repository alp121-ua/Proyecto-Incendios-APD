import pandas as pd
import os

# --- MODIFICACIÓN DE RUTA PARA ROBUSTEZ ---
# Obtiene el directorio donde se encuentra este script ('unir_csv.py').
script_dir = os.path.dirname(os.path.abspath(__file__))

# Rutas completas a los archivos
path_viento = os.path.join(script_dir, "viento_pontevedra.csv")
path_temp = os.path.join(script_dir, "temperaturas_diarias_pontevedra.csv")
output_path = os.path.join(script_dir, "datos_pontevedra.csv") # Ruta para el archivo unido

print("Iniciando carga y procesamiento de datos...")

# --- 1. CARGAR Y MODIFICAR DATOS DE VIENTO ---
try:
    df_viento = pd.read_csv(path_viento)
    
    # Aplicar solicitud anterior: Eliminar 'Año'
    df_viento = df_viento.drop(columns=['Año'])
    
    # Preparar la columna de unión y convertir a formato datetime
    df_viento['Fecha'] = pd.to_datetime(df_viento['Fecha'], format='%d-%m-%Y', errors='coerce')
    print("Viento: Columna 'Año' eliminada.")
    
except FileNotFoundError:
    print(f"ERROR: No se encontró 'datos_lugo_viento_2000_2025.csv' en la ruta: {path_viento}")
    exit()

# --- 2. CARGAR Y MODIFICAR DATOS DE TEMPERATURA ---
try:
    df_temp = pd.read_csv(path_temp)

    # Limpieza: Eliminar la fila 'FECHA' duplicada si existe
    df_temp = df_temp[df_temp['Fecha'] != 'FECHA']
    
    # Conversión de tipos de datos para las temperaturas
    df_temp['Temperatura_Maxima'] = pd.to_numeric(df_temp['Temperatura_Maxima'], errors='coerce')
    df_temp['Temperatura_Minima'] = pd.to_numeric(df_temp['Temperatura_Minima'], errors='coerce')

    # Aplicar solicitud anterior: Poner temperaturas primero
    df_temp = df_temp[['Fecha', 'Temperatura_Maxima', 'Temperatura_Minima']]
    
    # Preparar la columna de unión y convertir a formato datetime
    df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha'], format='%d-%m-%Y', errors='coerce')
    print("Temperatura: Reordenado y listo para unir.")
    
except FileNotFoundError:
    print(f"ERROR: No se encontró 'temperaturas_diarias_lugo.csv' en la ruta: {path_temp}")
    exit()

# --- 3. UNIR Y ORDENAR EL DATAFRAME FINAL ---

# Unir usando la columna 'Fecha'
df_unido = pd.merge(df_temp, df_viento, on='Fecha', how='inner')

# Reordenar el DataFrame final para que las TEMPERATURAS VAYAN PRIMERO
column_order = [
    'Fecha',
    'Temperatura_Maxima', 
    'Temperatura_Minima',  
    'Racha_Max_Km_h', 
    'Hora_Racha', 
    'Velocidad_Media_Km_h'
]
df_unido = df_unido[column_order]

# --- 4. GUARDAR EL RESULTADO ---
df_unido.to_csv(output_path, index=False)

print("\n¡Proceso completado!")
print(f"Archivos unidos, modificados y guardados en '{output_path}'")
print(f"El DataFrame final tiene {len(df_unido)} filas.")
import pandas as pd
import numpy as np
import os

# --- 1. DEFINICIÓN DE ARCHIVOS Y ORDEN FINAL ---
FILE_VIENTO_TEMP = "datos_pontevedra.csv"
FILE_PRECIP_SOL = "precipitaciones_pontevedra_2000_actualidad.csv"
OUTPUT_FILE = "datos_pontevedra_unidos.csv"

COLUMN_ORDER = [
    'Fecha', 'Temperatura_Maxima', 'Temperatura_Minima', 'Racha_Max_Km_h', 
    'Hora_Racha', 'Velocidad_Media_Km_h', 'Precipitacion_lm2', 'Horas_de_sol'
]

# --- 2. CARGAR Y PROCESAR DATOS DE VIENTO/TEMPERATURA ---
df_viento_temp = pd.read_csv(FILE_VIENTO_TEMP)
df_viento_temp['Fecha'] = pd.to_datetime(df_viento_temp['Fecha'], errors='coerce', format='%Y-%m-%d')
df_viento_temp.dropna(subset=['Fecha'], inplace=True)
df_viento_temp.drop_duplicates(subset=['Fecha'], keep='first', inplace=True)

# --- 3. CARGAR Y PROCESAR DATOS DE PRECIPITACIÓN/SOL ---
df_precip_sol = pd.read_csv(FILE_PRECIP_SOL)
df_precip_sol = df_precip_sol.rename(columns={
    'Horas de Sol': 'Horas_de_sol',
    'Precipitacion_l_m2': 'Precipitacion_lm2'
})

# Se omite la eliminación de 'Año' ya que no está presente en este archivo.
df_precip_sol['Fecha'] = pd.to_datetime(df_precip_sol['Fecha'], errors='coerce', format='%d-%m-%Y')
df_precip_sol.dropna(subset=['Fecha'], inplace=True)

# --- 4. UNIR DATAFRAMES ---
df_unido = pd.merge(df_viento_temp, df_precip_sol, on='Fecha', how='inner')

# Reordenar las columnas
df_unido = df_unido[COLUMN_ORDER]

# --- 5. GUARDAR EL RESULTADO ---
df_unido.to_csv(OUTPUT_FILE, index=False)
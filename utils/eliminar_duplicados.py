import pandas as pd
import os

# Lista de nombres de archivo CSV originales
archivos_csv = [
    'datos_acoruna_unidos.csv',
    'datos_lugo_unidos.csv',
    'datos_pontevedra_unidos.csv'
]

# Lista para guardar los nombres de los nuevos archivos
nuevos_archivos = []

print("Procesando archivos...")

for nombre_archivo in archivos_csv:
    # Comprobar si el archivo existe antes de procesarlo
    if not os.path.exists(nombre_archivo):
        print(f"ADVERTENCIA: El archivo {nombre_archivo} no se encontró. Omitiendo.")
        continue

    try:
        # Leer el archivo CSV
        df = pd.read_csv(nombre_archivo)
        
        filas_originales = df.shape[0]
        
        # Eliminar filas duplicadas
        df_sin_duplicados = df.drop_duplicates()
        
        filas_nuevas = df_sin_duplicados.shape[0]
        filas_eliminadas = filas_originales - filas_nuevas
        
        print(f"\nArchivo: {nombre_archivo}")
        print(f"  - Filas originales: {filas_originales}")
        print(f"  - Filas eliminadas: {filas_eliminadas}")
        print(f"  - Filas restantes: {filas_nuevas}")
        
        # Crear el nuevo nombre de archivo
        # Divide el nombre en la última aparición de '.' y añade el sufijo
        partes_nombre = nombre_archivo.rsplit('.', 1)
        nuevo_nombre = f"{partes_nombre[0]}_sin_duplicados.csv"
        
        # Guardar el DataFrame sin duplicados en un nuevo archivo CSV
        df_sin_duplicados.to_csv(nuevo_nombre, index=False)
        
        nuevos_archivos.append(nuevo_nombre)
        print(f"  - Guardado como: {nuevo_nombre}")

    except Exception as e:
        print(f"Ocurrió un error procesando {nombre_archivo}: {e}")

print("\nProceso completado.")
print("Se generaron los siguientes archivos:")
for f in nuevos_archivos:
    print(f"- {f}")
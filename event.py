import pandas as pd
import unicodedata
import re
from datetime import datetime

# --- FUNCIONES DE SOPORTE ---

def crear_slug(text):
    """
    Genera un slug (URI-friendly string) a partir de una cadena de texto.
    Convierte a minúsculas, normaliza acentos y reemplaza espacios por guiones bajos.
    """
    if pd.isna(text) or text is None:
        return ""
    
    # 1. Normalizar el texto (elimina tildes/acentos)
    text = str(text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    
    # 2. Convertir a minúsculas
    text = text.lower()
    
    # 3. Reemplazar caracteres no alfanuméricos por un guion bajo
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    
    # 4. Reemplazar espacios y guiones con un solo guion bajo
    text = re.sub(r'[\s-]+', '_', text)
    
    # 5. Eliminar guiones bajos al inicio o al final
    text = text.strip('_')
    
    return text

def sanitize_date(date_str):
    """
    Intenta convertir la cadena de fecha al formato ISO 8601 (xsd:date o xsd:dateTime)
    si es posible. Devuelve la cadena original si falla.
    """
    if pd.isna(date_str):
        return None
    try:
        # Asume que la columna 'fecha' contiene solo la fecha (AAAA-MM-DD)
        # Si contiene hora, se cambiaría a datetime.fromisoformat(date_str).isoformat()
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        # Intenta parsear como datetime si incluye hora
        try:
             date_obj = datetime.fromisoformat(date_str)
             return date_obj.isoformat()
        except ValueError:
            return date_str # Devuelve la cadena original si el formato es desconocido

# ----------------------------------------------------------------------
# BLOQUE PRINCIPAL DE GENERACIÓN DE RDF
# ----------------------------------------------------------------------

# 1. Cargar y procesar INCENDIOS
# ATENCIÓN: Asegúrate de que el archivo 'incendios-filtrado.csv' está en el mismo directorio.

df_incendios = pd.read_csv('data/fires_all_transformado.csv', sep=';')
    
# Inicialización de la cadena RDF
RDF_INCENDIOS = """@prefix schema: <https://schema.org/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix fire: <http://example/fire/> .
@prefix place: <http://example/place/> .

"""
# Conjunto para rastrear y evitar duplicados de municipios (para la definición de Place)
municipios_a_definir = set()
aux = 0
# 2. Generación de las tripletas de EVENTO
for _, row in df_incendios.iterrows():
    # Usamos el ID del incendio para su URI
    fire_id = aux
    
    # Creamos el slug del municipio
    slug_municipio = crear_slug(row['municipio'])
    
    # 3. Sanitizar datos
    fecha_sanitizada = sanitize_date(row['fecha'])
    
    
    if row['intencionado']:
        inten = 'Intencionado'
    else:
        inten = 'Causas naturales'
    # Añadimos el slug a la lista de municipios a definir
    municipios_a_definir.add((slug_municipio, row['municipio']))
    
    # Nota: Usaremos schema:Event como lo más genérico, 
    # y schema:name, about, description para los campos de texto
    
    # Construcción de la entrada del Evento
    ENTRY = f"""
    fire:{fire_id}
        a schema:Event ;
        schema:about "Incendio" ;
        schema:location "{row['municipio']}";
        schema:identifier "{row['id']}" ;
        schema:startDate "{row['fecha']}";
        schema:description "{inten}";
        schema:geo [
            a schema:GeoCoordinates ;
            schema:latitude "{row['lat']}";
            schema:longitude "{row['lng']}"
        ] 
    """
    RDF_INCENDIOS += ENTRY

    aux += 1


# 5. Escribir el archivo final
OUTPUT_FILENAME = 'incendios_final.ttl'
with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
    f.write(RDF_INCENDIOS)
    
print(f"Archivo '{OUTPUT_FILENAME}' generado con éxito.")
import pandas as pd
import requests
import time

# --- FUNCIÓN DE BÚSQUEDA ROBUSTA ---
def get_wikidata_uri(municipio_raw):
    """
    1. Busca en Wikidata usando el nombre tal cual (tolera mayúsculas/falta de acentos).
    2. Filtra los resultados para asegurar que es el de Galicia/España.
    """
    url = "https://www.wikidata.org/w/api.php"
    
    # Limpiamos un poco el nombre por si acaso
    search_term = municipio_raw.strip()
    
    params = {
        'action': 'wbsearchentities',
        'format': 'json',
        'language': 'es',     # Queremos resultados priorizando español
        'search': search_term, 
        'limit': 5            # Pedimos 5 candidatos para filtrar el correcto
    }
    
    try:
        response = requests.get(url, params=params, headers={'User-Agent': 'MiScriptDeDatos/1.0'})
        data = response.json()
        
        results = data.get('search', [])
        
        if not results:
            return None

        # --- FILTRO INTELIGENTE ---
        # Buscamos en la descripción palabras clave que confirmen que es el lugar correcto.
        # Esto distingue "Santiago de Compostela" (Galicia) de "Santiago" (Chile).
        keywords_galicia = ['galicia', 'españa', 'spain', 'coruña', 'lugo', 'ourense', 'pontevedra', 'municipio', 'concello']
        
        for result in results:
            description = result.get('description', '').lower()
            label = result.get('label', '').lower()
            
            # Chequeamos si alguna palabra clave está en la descripción
            if any(key in description for key in keywords_galicia):
                return result['concepturi']
                
        # Si ninguno de los 5 primeros tiene descripción clara, 
        # pero el nombre coincide mucho, devolvemos el primero (arriesgado pero útil)
        # return results[0]['concepturi'] 
        
        return None

    except Exception as e:
        print(f"Error conectando con Wikidata para {municipio_raw}: {e}")
        return None

# -------------------------------------------

# 1. Cargar datos
df = pd.read_csv('..data/municipios_incendios_maps.csv', sep=';')

# 2. Limpieza
df['municipio'] = df['municipio'].astype(str).str.strip()
df = df.drop_duplicates(subset=['municipio'], keep='first')
df = df.reset_index(drop=True)

# 3. Prefijos
rdf_content = """@prefix :      <http://127.0.0.1:3333/> .
@prefix ex:     <http://example/> .
@prefix schema: <https://schema.org/> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix owl:    <http://www.w3.org/2002/07/owl#> .

"""

print(f"Procesando {len(df)} municipios...")

# 4. Iterar
for index, row in df.iterrows():
    municipio = row['municipio']
    lat = row['lat']
    lng = row['lng']
    url = str(row['url_maps']).strip()
    
    # --- LLAMADA A LA API ---
    wikidata_uri = get_wikidata_uri(municipio)
    
    # Pausa de seguridad
    time.sleep(0.2)
    
    # Construcción de la línea sameAs
    same_as_line = f'    owl:sameAs <{wikidata_uri}> ;' if wikidata_uri else ''
    
    entry = f"""<http://example/place/{index}>
    rdf:type schema:Place ;
    schema:name "{municipio}" ;
{same_as_line}
    schema:geo [
        rdf:type schema:GeoCoordinates ;
        schema:latitude {lat} ;
        schema:longitude {lng}
    ] ;
    schema:hasMap "{url}" .

"""
    rdf_content += entry
    
    # Log de progreso para que veas qué está encontrando
    if wikidata_uri:
        print(f"[OK] {municipio} -> {wikidata_uri}")
    else:
        print(f"[!!] NO ENCONTRADO: {municipio}")

# 5. Guardar
output_filename = 'municipios_schema_enriched.ttl'
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(rdf_content)

print(f"¡Listo! Archivo generado: {output_filename}")
import pandas as pd

# Read the CSV file
df = pd.read_csv('data/municipios_incendios_maps.csv', sep=';')

# --- PARTE NUEVA: LIMPIEZA DE DUPLICADOS ---

# 1. Aseguramos que no haya espacios extra antes de comparar
df['municipio'] = df['municipio'].astype(str).str.strip()

# 2. Eliminamos duplicados basándonos en la columna 'municipio'
# keep='first' significa que se queda con el primero que encuentra y borra el resto
df = df.drop_duplicates(subset=['municipio'], keep='first')

# 3. Reseteamos el índice para que los URIs sean consecutivos (0, 1, 2...)
# Si no haces esto, los IDs saltarían (ej: place/0, place/5, place/12...)
df = df.reset_index(drop=True)

# -------------------------------------------

# Define the prefix part of the RDF
rdf_content = """@prefix :       <http://127.0.0.1:3333/> .
@prefix ex:     <http://example/> .
@prefix schema: <https://schema.org/> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

"""

# Iterate through all rows to generate the RDF entries
for index, row in df.iterrows():
    municipio = row['municipio'] # Ya hicimos el strip arriba
    lat = row['lat']
    lng = row['lng']
    url = str(row['url_maps']).strip()
    
    # Create a unique subject URI. 
    entry = f"""<http://example/place/{index}>
    rdf:type schema:Place ;
    schema:name "{municipio}" ;
    schema:geo [
        rdf:type schema:GeoCoordinates ;
        schema:latitude {lat} ;
        schema:longitude {lng}
    ] ;
    schema:hasMap "{url}" .

"""
    rdf_content += entry

# Save the content to a file
output_filename = 'municipios_schema.ttl'
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(rdf_content)

print(f"File '{output_filename}' generated with {len(df)} unique entries.")
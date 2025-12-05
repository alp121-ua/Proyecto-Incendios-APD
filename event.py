import pandas as pd

df_incendios = pd.read_csv('data/fires_all_transformado.csv')

municipios_dict = {}

with open("municipios_schema_enriched.ttl", "r", encoding="utf-8") as f:
    lines = f.readlines()


current_id = None
for line in lines:
    line = line.strip()

    # Detectar ID de municipio
    if line.startswith("<http://example/place/"):
        current_id = line.split("/")[-1].replace(">", "")

    # Detectar nombre
    if "schema:name" in line and current_id is not None:
        name = line.split('"')[1].strip().upper()
        municipios_dict[name] = current_id
        current_id = None
    
# Inicialización de la cadena RDF
RDF_INCENDIOS = """@prefix :       <http://127.0.0.1:3333/>
@prefix schema: <https://schema.org/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix fire: <http://example/fire/> .
@prefix place: <http://example/place/> .

"""
AUX = 0
for _, row in df_incendios.iterrows():
    EVENT_ID = AUX

    if row['intencionado']:
        INTENCION = 'Intencionado'
    else:
        INTENCION = 'Causas naturales'

    municipio = row['municipio']

    if municipio in municipios_dict:
        muni_id = municipios_dict[municipio]
        location_triple = f"schema:location <http://example/place/{muni_id}> ;"
    else:
        # Si no existe, se deja como literal (para evitar errores)
        location_triple = f'schema:location "{row["municipio"]}" ;'

    
    ENTRY = f"""<http://example/event/{row['id']}>
    fire:{EVENT_ID}
        a schema:Event ;
        schema:about "Incendio" ;
        {location_triple}
        schema:identifier "{row['id']}" ;
        schema:startDate "{row['fecha']}";
        schema:description "Intencion: {INTENCION} Superficie quemada: {row['superficie_bin']} Estacion: {row['estacion']}";
        schema:geo [
            a schema:GeoCoordinates ;
            schema:latitude {row['lat']};
            schema:longitude {row['lng']}
        ] 

    """
    RDF_INCENDIOS += ENTRY

    AUX += 1

OUTPUT_FILENAME = 'schema_event.ttl'
with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
    f.write(RDF_INCENDIOS)
    
print(f"Archivo '{OUTPUT_FILENAME}' generado con éxito.")
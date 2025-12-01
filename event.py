import pandas as pd

df_incendios = pd.read_csv('data/fires_all_transformado.csv')
    
# Inicialización de la cadena RDF
RDF_INCENDIOS = """@prefix schema: <https://schema.org/> .
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
    
    ENTRY = f"""
    fire:{EVENT_ID}
        a schema:Event ;
        schema:about "Incendio" ;
        schema:location "{row['municipio']}";
        schema:identifier "{row['id']}" ;
        schema:startDate "{row['fecha']}";
        schema:description "Intencion: {INTENCION} \n           Superficie quemada: {row['superficie_bin']}\n           Estacion: {row['estacion']}";
        schema:geo [
            a schema:GeoCoordinates ;
            schema:latitude "{row['lat']}";
            schema:longitude "{row['lng']}"
        ] 
    """
    RDF_INCENDIOS += ENTRY

    AUX += 1

OUTPUT_FILENAME = 'schema_event.ttl'
with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
    f.write(RDF_INCENDIOS)
    
print(f"Archivo '{OUTPUT_FILENAME}' generado con éxito.")
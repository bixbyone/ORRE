# Importar bibliotecas
from shapely.geometry import mapping, shape  
import json
import fiona

# Caminho do arquivo JSON original
json_file = "https://raw.githubusercontent.com/bixbyone/ORRE/main/src/DataRecords.json" 

# Ler os dados do JSON
with open(json_file) as f:
  data = json.load(f)

# Gerar o conteúdo GML com as features
gml = "<gml:FeatureCollection xmlns:gml='http://www.opengis.net/gml'>"

for feature in data:

  # Extrair a geometria
  geom = shape(feature['geometry'])  

  # Convert geometry to GML 
  gml_feature = f"""
  <gml:featureMember>
    <gml:Feature>
      <gml:geometryProperty>
        <gml:Polygon>{mapping(geom)}</gml:Polygon>  
      </gml:geometryProperty>
    </gml:Feature>
  </gml:featureMember>
  """

  # Adicionar ao GML
  gml += gml_feature

# Finalizar a FeatureCollection
gml += "</gml:FeatureCollection>"

# Salvar o arquivo GML
with open('data.gml', 'w') as f:
  f.write(gml)

print("Normalização concluída com sucesso!")
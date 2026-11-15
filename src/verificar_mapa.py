
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
arquivo = BASE_DIR / "data" / "geo" / "estados_br.geojson"

with open(arquivo, encoding="utf-8") as f:
    dados = json.load(f)

print("Tipo:", dados.get("type"))
print("Quantidade de geometrias:", len(dados["features"]))

for feature in dados["features"][:5]:
    print(
        "Código:",
        feature["properties"].get("codarea"),
        "| Geometria:",
        feature["geometry"]["type"]
    )

print(
    "\nPrimeiras coordenadas:",
    str(dados["features"][0]["geometry"]["coordinates"])[:300]
)

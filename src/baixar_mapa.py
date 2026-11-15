
import json
import gzip
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

pasta_geo = BASE_DIR / "data" / "geo"
pasta_geo.mkdir(parents=True, exist_ok=True)

arquivo_saida = pasta_geo / "estados_br.geojson"

url = (
    "https://servicodados.ibge.gov.br/api/v3/"
    "malhas/paises/BR?intrarregiao=UF"
    "&formato=application/vnd.geo+json"
    "&qualidade=minima"
)

print("Baixando malha geográfica do IBGE...")

with urllib.request.urlopen(url, timeout=60) as resposta:
    conteudo = resposta.read()

# Verificar se o conteúdo está comprimido em GZIP
if conteudo.startswith(b"\x1f\x8b"):
    conteudo = gzip.decompress(conteudo)

# Converter os bytes em JSON
dados = json.loads(conteudo.decode("utf-8"))

if dados.get("type") != "FeatureCollection":
    raise ValueError("Resposta inesperada da API do IBGE.")

with open(arquivo_saida, "w", encoding="utf-8") as arquivo:
    json.dump(dados, arquivo, ensure_ascii=False)

print("Download concluído!")
print("Quantidade de estados:", len(dados["features"]))
print("Arquivo salvo em:", arquivo_saida)

print("\nPropriedades do primeiro estado:")
print(dados["features"][0]["properties"])

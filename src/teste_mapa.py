
import json
from pathlib import Path
import plotly.graph_objects as go

BASE_DIR = Path(__file__).resolve().parent.parent

arquivo_geo = BASE_DIR / "data" / "geo" / "estados_br.geojson"

with open(arquivo_geo, encoding="utf-8") as f:
    geojson = json.load(f)

# Selecionar São Paulo
sp = next(
    feature
    for feature in geojson["features"]
    if str(feature["properties"]["codarea"]) == "35"
)

coordenadas = sp["geometry"]["coordinates"][0]

longitudes = [p[0] for p in coordenadas]
latitudes = [p[1] for p in coordenadas]

print("Pontos:", len(coordenadas))
print("Longitude:", min(longitudes), max(longitudes))
print("Latitude:", min(latitudes), max(latitudes))

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=longitudes,
        y=latitudes,
        mode="lines",
        fill="toself",
        fillcolor="lightblue",
        line=dict(color="black", width=1),
        name="São Paulo"
    )
)

fig.update_layout(
    title="Teste cartesiano - São Paulo",
    xaxis_title="Longitude",
    yaxis_title="Latitude",
    height=600
)

fig.update_yaxes(
    scaleanchor="x",
    scaleratio=1
)

fig.show()

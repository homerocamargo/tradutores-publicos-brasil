
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

entrada = BASE_DIR / "data" / "processed" / "tradutores_tratados.csv"
saida = BASE_DIR / "data" / "processed" / "conflitos_identificacao.csv"

df = pd.read_csv(
    entrada,
    sep=";",
    encoding="utf-8-sig",
    dtype=str
)

# Normalizar nomes para comparação
df["Nome_normalizado"] = (
    df["Nome completo"]
    .fillna("")
    .str.strip()
    .str.upper()
)

# Identificar matrículas associadas a nomes diferentes
conflitos = (
    df.groupby(
        ["Junta_normalizada", "Matricula_normalizada"]
    )["Nome_normalizado"]
    .nunique()
    .reset_index(name="Nomes_distintos")
)

conflitos = conflitos[
    conflitos["Nomes_distintos"] > 1
]

# Recuperar registros envolvidos nos conflitos
detalhes = df.merge(
    conflitos,
    on=["Junta_normalizada", "Matricula_normalizada"],
    how="inner"
)

# Selecionar colunas para auditoria
colunas = [
    "Nome completo",
    "Matrícula",
    "Junta comercial",
    "Idioma_padronizado",
    "UF",
    "Município",
    "Nomes_distintos"
]

detalhes = detalhes[colunas].sort_values(
    ["Junta comercial", "Matrícula", "Nome completo"]
)

detalhes.to_csv(
    saida,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print("--- AUDITORIA DE IDENTIFICAÇÃO ---")
print("Grupos com nomes diferentes:", len(conflitos))
print("Registros envolvidos:", len(detalhes))
print("Relatório salvo em:", saida)

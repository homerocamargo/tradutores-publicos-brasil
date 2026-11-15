
import pandas as pd
from pathlib import Path

# Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
entrada = BASE_DIR / "data" / "raw" / "tradutores.xlsx"
saida = BASE_DIR / "data" / "processed" / "tradutores_tratados.csv"

saida.parent.mkdir(parents=True, exist_ok=True)

# EXTRAÇÃO
df = pd.read_excel(entrada, sheet_name="Tradutor", dtype=str)

total_original = len(df)

# TRANSFORMAÇÃO

# Padronizar nomes das colunas
df.columns = df.columns.str.strip()

# Remover duplicatas exatas antes das transformações
df = df.drop_duplicates().copy()

# Preservar idioma original
df["Idioma_original"] = df["Idiomas"]

# Padronizar idiomas
df["Idioma_padronizado"] = (
    df["Idiomas"]
    .astype("string")
    .str.strip()
    .str.upper()
    .replace({
        "INGLES": "INGLÊS",
        "FRANCES": "FRANCÊS"
    })
)

# Normalizar campos de identificação
df["Junta_normalizada"] = (
    df["Junta comercial"]
    .astype("string")
    .str.strip()
    .str.upper()
)

df["Matricula_normalizada"] = (
    df["Matrícula"]
    .astype("string")
    .str.strip()
)

# Criar identificador provisório
df["ID_cadastro"] = (
    df["Junta_normalizada"]
    + "_"
    + df["Matricula_normalizada"]
)


# PADRONIZAÇÃO GEOGRÁFICA

# Preservar valores originais
df["UF_original"] = df["UF"]
df["Municipio_original"] = df["Município"]

# Normalizar UFs
df["UF"] = (
    df["UF"]
    .astype("string")
    .str.strip()
    .str.upper()
)

# Normalizar municípios
df["Municipio_padronizado"] = (
    df["Município"]
    .astype("string")
    .str.strip()
    .str.upper()
    .str.replace(r"\s+", " ", regex=True)
)

print("\n--- PADRONIZAÇÃO GEOGRÁFICA ---")
print("UFs distintas:", df["UF"].nunique())
print("Municípios distintos:",
      df["Municipio_padronizado"].nunique())


# CARGA
df.to_csv(
    saida,
    index=False,
    encoding="utf-8-sig",
    sep=";"
)

print("--- RESULTADO DO ETL ---")
print("Registros originais:", total_original)
print("Registros tratados:", len(df))
print("Duplicatas exatas removidas:", total_original - len(df))
print("Idiomas padronizados:", df["Idioma_padronizado"].nunique())
print("Arquivo gerado:", saida)

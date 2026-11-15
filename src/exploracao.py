
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
arquivo = BASE_DIR / "data" / "raw" / "tradutores.xlsx"

df = pd.read_excel(arquivo, sheet_name="Tradutor")

# Remover colunas inteiramente vazias
df = df.dropna(axis=1, how="all")

# Padronizar nomes das colunas
df.columns = df.columns.str.strip()

print("Dimensões da base:", df.shape)
print("\nColunas:")
print(df.columns.tolist())

print("\nPrimeiros registros:")
print(df.head())

print("\nValores ausentes:")
print(df.isna().sum().sort_values(ascending=False))

print("\nRegistros por idioma:")
print(df["Idiomas"].value_counts())


# ETAPA 2 - Padronização dos idiomas

# Preservar os valores originais
df["Idioma_original"] = df["Idiomas"]

# Padronizar maiúsculas e espaços
df["Idioma_padronizado"] = (
    df["Idiomas"]
    .astype("string")
    .str.strip()
    .str.upper()
)

# Corrigir variações sem acento
correcoes = {
    "INGLES": "INGLÊS",
    "FRANCES": "FRANCÊS"
}

df["Idioma_padronizado"] = (
    df["Idioma_padronizado"].replace(correcoes)
)

print("\nQuantidade de categorias antes:")
print(df["Idioma_original"].nunique())

print("\nQuantidade de categorias depois:")
print(df["Idioma_padronizado"].nunique())

print("\nContagem por idioma padronizado:")
print(df["Idioma_padronizado"].value_counts())


# ETAPA 3 - Análise de cadastros e duplicidades

# Criar identificador provisório do cadastro
df["ID_cadastro"] = (
    df["Junta comercial"].astype("string").str.strip().str.upper()
    + "_"
    + df["Matrícula"].astype("string").str.strip()
)

total_registros = len(df)
total_cadastros = df["ID_cadastro"].nunique()

print("\n--- ANÁLISE DE CADASTROS ---")
print("Total de registros:", total_registros)
print("Cadastros distintos:", total_cadastros)
print("Registros adicionais por cadastro:",
      total_registros - total_cadastros)

# Identificar cadastros com múltiplos registros
repetidos = df[
    df.duplicated(subset=["ID_cadastro"], keep=False)
].copy()

print("\nCadastros com múltiplos registros:",
      repetidos["ID_cadastro"].nunique())

# Exibir exemplos para investigação
print("\nExemplos de cadastros repetidos:")
print(
    repetidos[
        ["Nome completo", "Matrícula",
         "Junta comercial", "Idioma_padronizado"]
    ]
    .sort_values(["Junta comercial", "Matrícula"])
    .head(20)
    .to_string(index=False)
)

# Verificar se um cadastro aparece com nomes diferentes
nomes_por_cadastro = (
    df.groupby("ID_cadastro")["Nome completo"]
    .nunique()
)

print("\nCadastros associados a mais de um nome:",
      (nomes_por_cadastro > 1).sum())


# ETAPA 4 - Diagnóstico de duplicidades

# Padronizar nomes para comparação
df["Nome_normalizado"] = (
    df["Nome completo"]
    .astype("string")
    .str.strip()
    .str.upper()
)

# 1. Registros repetidos na combinação
# cadastro + nome + idioma
colunas_comparacao = [
    "ID_cadastro",
    "Nome_normalizado",
    "Idioma_padronizado"
]

duplicados = df.duplicated(
    subset=colunas_comparacao,
    keep="first"
)

print("\n--- DIAGNÓSTICO DE DUPLICIDADES ---")

print("Linhas adicionais com mesma chave, nome e idioma:",
      duplicados.sum())

# 2. Cadastros com múltiplos idiomas
idiomas_por_cadastro = (
    df.groupby("ID_cadastro")["Idioma_padronizado"]
    .nunique()
)

print("Cadastros com mais de um idioma:",
      (idiomas_por_cadastro > 1).sum())

# 3. Investigar conflitos de nomes
conflitos = df[
    df["ID_cadastro"].isin(
        nomes_por_cadastro[nomes_por_cadastro > 1].index
    )
].copy()

print("\n--- POSSÍVEIS CONFLITOS DE IDENTIFICAÇÃO ---")

print(
    conflitos[
        ["ID_cadastro", "Nome completo",
         "Idioma_padronizado", "Situação"]
    ]
    .sort_values(["ID_cadastro", "Nome completo"])
    .to_string(index=False)
)


# ETAPA 5 - Verificação de duplicações exatas

# Comparar somente as 12 colunas originais
colunas_originais = [
    "Nome completo",
    "Matrícula",
    "Data da Matrícula",
    "Situação",
    "Endereço",
    "E-mail Principal",
    "Telefone Principal",
    "Município",
    "UF",
    "CEP",
    "Idiomas",
    "Junta comercial"
]

duplicatas_exatas = df.duplicated(
    subset=colunas_originais,
    keep="first"
)

print("\n--- DUPLICATAS EXATAS ---")
print("Linhas completamente duplicadas:",
      duplicatas_exatas.sum())

# Comparar registros com mesma chave, nome e idioma
# para identificar diferenças em outros campos
candidatos = df[
    df.duplicated(
        subset=[
            "ID_cadastro",
            "Nome_normalizado",
            "Idioma_padronizado"
        ],
        keep=False
    )
]

print("\nLinhas envolvidas em possíveis duplicações:",
      len(candidatos))

print("\nDistribuição por Junta Comercial:")
print(
    candidatos["Junta comercial"]
    .value_counts()
)


# ETAPA 6 - Qualidade dos dados geográficos

print("\n--- ANÁLISE GEOGRÁFICA ---")

print("Quantidade de UFs distintas:",
      df["UF"].nunique())

print("\nValores de UF:")
print(df["UF"].value_counts().to_string())

# Normalizar municípios para comparação
df["Municipio_normalizado"] = (
    df["Município"]
    .astype("string")
    .str.strip()
    .str.upper()
)

print("\nMunicípios distintos antes:",
      df["Município"].nunique())

print("Municípios distintos após normalização:",
      df["Municipio_normalizado"].nunique())

# Identificar variações de grafia dentro da mesma UF
variacoes = (
    df.groupby(["UF", "Municipio_normalizado"])["Município"]
    .nunique()
)

print("\nGrupos UF/município com variações de grafia:",
      (variacoes > 1).sum())

print("\nExemplos de variações:")
print(
    variacoes[variacoes > 1]
    .head(15)
    .to_string()
)

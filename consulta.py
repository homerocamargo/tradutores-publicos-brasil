import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
import unicodedata

BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_DADOS = BASE_DIR / "data" / "processed" / "tradutores_publicos.csv"
ARQUIVO_GEO = BASE_DIR / "data" / "geo" / "estados_br.geojson"

@st.cache_data
def carregar_dados():
    return pd.read_csv(
        ARQUIVO_DADOS,
        sep=";",
        encoding="utf-8-sig",
        dtype=str,
    )

def normalizar_busca(texto):
    texto = str(texto).casefold()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(
        caractere for caractere in texto
        if not unicodedata.combining(caractere)
    )

def area_assinada(anel):
    """Área orientada de um anel de coordenadas [longitude, latitude]."""
    return sum(
        p1[0] * p2[1] - p2[0] * p1[1]
        for p1, p2 in zip(anel, anel[1:])
    )

@st.cache_data
def carregar_geojson_corrigido():
    with open(ARQUIVO_GEO, "r", encoding="utf-8") as arquivo:
        geojson = json.load(arquivo)

    # Algumas malhas em GeoJSON seguem a orientação RFC 7946,
    # mas o renderizador geográfico do Plotly/D3 exige orientação
    # oposta: anel externo horário, anéis de buracos anti-horários.
    # Ajustamos a cópia carregada sem modificar o arquivo do IBGE.
    for feature in geojson["features"]:
        geometria = feature["geometry"]
        tipo = geometria["type"]

        if tipo == "Polygon":
            poligonos = [geometria["coordinates"]]
        elif tipo == "MultiPolygon":
            poligonos = geometria["coordinates"]
        else:
            continue

        for poligono in poligonos:
            for indice, anel in enumerate(poligono):
                area = area_assinada(anel)
                externo_anti_horario = indice == 0 and area > 0
                buraco_horario = indice > 0 and area < 0
                if externo_anti_horario or buraco_horario:
                    anel.reverse()

    return geojson

df = carregar_dados()
df_original = df.copy()

st.title("Tradutores Públicos Brasil")

st.caption(
    "Projeto independente de consulta a dados públicos do "
    "Departamento Nacional de Registro Empresarial e Integração (DREI)."
)

st.info(
    "Base oficial de referência: setembro de 2026. "
    "Atualização pelo DREI: sob demanda. "
    "Os dados podem não refletir alterações cadastrais recentes. "
    "Para confirmar a habilitação e a situação atual de um profissional, "
    "consulte a Junta Comercial responsável.",
    icon="ℹ️"
)

st.link_button(
    "Consultar repositório oficial de dados (DREI)",
    "https://www.gov.br/memp/pt-br/acesso-a-informacao/dados-abertos/repositorio-de-dados-abertos",
)

st.link_button(
    "Baixar planilha oficial — Setembro 2026",
    "https://www.gov.br/memp/pt-br/acesso-a-informacao/dados-abertos/dados-tradutores-e-leiloeiro/tabela-padrao-tradutor-e-leiloeiro-publica.xlsx/@@download/file",
)


# FILTROS INTERATIVOS NA ÁREA PRINCIPAL

st.subheader("Encontrar um tradutor")
st.caption("Pesquise pelo nome ou filtre por idioma e localização.")

busca = st.text_input(
    "Nome do profissional",
    placeholder="Digite o nome do tradutor...",
)

col_idioma, col_uf, col_municipio = st.columns(3)

with col_idioma:
    idiomas = sorted(df["Idioma_padronizado"].dropna().unique())
    idioma = st.selectbox("Idioma", ["Todos"] + idiomas)

if idioma != "Todos":
    df = df[df["Idioma_padronizado"] == idioma]

with col_uf:
    estados = sorted(df["UF"].dropna().unique())
    uf = st.selectbox("Estado (UF)", ["Todos"] + estados)

if uf != "Todos":
    df = df[df["UF"] == uf]

with col_municipio:
    municipios = sorted(df["Municipio_padronizado"].dropna().unique())
    municipio = st.selectbox("Município", ["Todos"] + municipios)

if municipio != "Todos":
    df = df[df["Municipio_padronizado"] == municipio]


# TABELA DE CONSULTA
st.divider()
st.subheader("Resultados da pesquisa")

df_consulta = df.copy()

if busca:
    termos = normalizar_busca(busca.strip()).split()

    nomes_normalizados = (
        df_consulta["Nome completo"]
        .fillna("")
        .map(normalizar_busca)
    )

    mascara = pd.Series(True, index=df_consulta.index)

    for termo in termos:
        mascara &= nomes_normalizados.str.contains(termo, regex=False)

    df_consulta = df_consulta[mascara]

# AGRUPAR IDIOMAS POR PROFISSIONAL

# Criar chave provisória com nome, junta e matrícula
df_consulta["Chave_profissional"] = (
    df_consulta["Nome completo"].fillna("").str.strip().str.upper()
    + "|"
    + df_consulta["Junta_normalizada"].fillna("")
    + "|"
    + df_consulta["Matricula_normalizada"].fillna("")
)

# Agrupar registros e reunir os idiomas
df_consulta = (
    df_consulta.groupby("Chave_profissional", as_index=False)
    .agg({
        "Nome completo": "first",
        "Matrícula": "first",
        "Idioma_padronizado": lambda x: ", ".join(
            sorted(x.dropna().unique())
        ),
        "Município": "first",
        "UF": "first",
        "Junta comercial": "first",
        "Situação": "first",
    })
)

# Selecionar colunas para exibição

colunas_exibicao = [
    "Chave_profissional",
    "Nome completo",
    "Matrícula",
    "Idioma_padronizado",
    "Município",
    "UF",
    "Junta comercial",
    "Situação",
]


# GUARDAR OS DADOS DE IDENTIFICAÇÃO PARA CONSULTA INDIVIDUAL

df_detalhes = df_original.copy()

df_detalhes["Chave_profissional"] = (
    df_detalhes["Nome completo"].fillna("").str.strip().str.upper()
    + "|"
    + df_detalhes["Junta_normalizada"].fillna("")
    + "|"
    + df_detalhes["Matricula_normalizada"].fillna("")
)


df_consulta = df_consulta[colunas_exibicao].sort_values("Nome completo")
st.write(f"**{len(df_consulta)} registros encontrados**")

evento_tabela = st.dataframe(
    df_consulta.drop(columns=["Chave_profissional"]),
    width="stretch",
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    column_config={
        "Nome completo": "Tradutor",
        "Matrícula": "Matrícula",
        "Idioma_padronizado": "Idiomas",
        "Município": "Município",
        "UF": "Estado",
        "Junta comercial": "Junta Comercial",
        "Situação": "Situação",
    },
)

st.caption("Clique em um profissional na tabela para visualizar sua ficha.")


# DOWNLOAD DOS RESULTADOS FILTRADOS

df_exportacao = df_consulta.drop(
    columns=["Chave_profissional"]
).rename(columns={
    "Nome completo": "Tradutor",
    "Matrícula": "Matrícula",
    "Idioma_padronizado": "Idiomas",
    "Município": "Município",
    "UF": "Estado",
    "Junta comercial": "Junta Comercial",
    "Situação": "Situação",
})

csv_exportacao = df_exportacao.to_csv(
    index=False,
    sep=";"
).encode("utf-8-sig")

with st.expander("Exportar resultados"):
    st.download_button(
        label="Baixar CSV",
        data=csv_exportacao,
        file_name="tradutores_publicos_consulta.csv",
        mime="text/csv",
        disabled=df_exportacao.empty,
    )

# FICHA INDIVIDUAL DO TRADUTOR

linhas_selecionadas = evento_tabela.selection.rows

if linhas_selecionadas:
    indice = linhas_selecionadas[0]
    selecionado = df_consulta.iloc[indice]

    registros = df_detalhes[
        df_detalhes["Chave_profissional"]
        == selecionado["Chave_profissional"]
    ]

    st.divider()
    st.subheader("Ficha do profissional")
    st.markdown(f"### {selecionado['Nome completo']}")

    col1, col2 = st.columns(2)
    idiomas_profissional = ", ".join(
        sorted(registros["Idioma_padronizado"].dropna().unique())
    )

    col1.write(f"**Idiomas:** {idiomas_profissional}")
    col1.write(f"**Estado:** {selecionado['UF']}")
    col1.write(f"**Município:** {selecionado['Município']}")

    col2.write(f"**Junta Comercial:** {selecionado['Junta comercial']}")
    col2.write(f"**Situação:** {selecionado['Situação']}")

    matriculas = sorted(
        registros["Matrícula"].dropna().unique()
    )

    st.write(
        "**Matrícula(s):** "
        + (", ".join(matriculas) if matriculas else "Não informado")
    )

    st.caption(
        "Informações provenientes da base pública do DREI. "
        "Consulte a Junta Comercial para confirmar a situação atual."
    )

# INDICADORES
col1, col2, col3 = st.columns(3)
col1.metric("Registros", len(df))
col2.metric("Juntas Comerciais", df["Junta_normalizada"].nunique())
col3.metric("Idiomas", df["Idioma_padronizado"].nunique())

st.divider()

# GRÁFICO POR IDIOMA
contagem = df["Idioma_padronizado"].value_counts().head(15).reset_index()
contagem.columns = ["Idioma", "Registros"]

fig = px.bar(
    contagem,
    x="Registros",
    y="Idioma",
    orientation="h",
    title="Registros por idioma",
)
fig.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig, width="stretch")
st.caption(
    "As contagens representam registros por idioma, "
    "não necessariamente profissionais distintos."
)

# GRÁFICO POR MUNICÍPIO
st.subheader("Distribuição por município")
contagem_municipios = (
    df["Municipio_padronizado"].value_counts().head(15).reset_index()
)
contagem_municipios.columns = ["Município", "Registros"]
fig_municipios = px.bar(
    contagem_municipios,
    x="Registros",
    y="Município",
    orientation="h",
    title="Municípios com mais registros",
)
fig_municipios.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_municipios, width="stretch")

# MAPA INTERATIVO DO BRASIL (APENAS UM MAPA)
st.divider()
st.subheader("Mapa de tradutores públicos por estado")
geojson = carregar_geojson_corrigido()

codigos_ibge = {
    "RO": "11", "AC": "12", "AM": "13", "RR": "14",
    "PA": "15", "AP": "16", "TO": "17", "MA": "21",
    "PI": "22", "CE": "23", "RN": "24", "PB": "25",
    "PE": "26", "AL": "27", "SE": "28", "BA": "29",
    "MG": "31", "ES": "32", "RJ": "33", "SP": "35",
    "PR": "41", "SC": "42", "RS": "43", "MS": "50",
    "MT": "51", "GO": "52", "DF": "53",
}
uf_por_codigo = {codigo: sigla for sigla, codigo in codigos_ibge.items()}

# Mantemos os 27 contornos no mapa, inclusive estados sem registros
# nos filtros atuais. Zero aqui é o resultado do filtro, não uma
# afirmação sobre a inexistência de profissionais no estado.
dados_mapa = pd.DataFrame({
    "codarea": [
        str(feature["properties"]["codarea"])
        for feature in geojson["features"]
    ]
})
dados_mapa["UF"] = dados_mapa["codarea"].map(uf_por_codigo)
contagem_uf = df.groupby("UF").size().reset_index(name="Registros")
dados_mapa = dados_mapa.merge(contagem_uf, on="UF", how="left")
dados_mapa["Registros"] = dados_mapa["Registros"].fillna(0).astype(int)

fig_mapa = px.choropleth(
    dados_mapa,
    geojson=geojson,
    locations="codarea",
    featureidkey="properties.codarea",
    color="Registros",
    hover_name="UF",
    hover_data={"Registros": True, "codarea": False},
    color_continuous_scale="YlOrRd",
    title="Distribuição de registros por estado",
)
fig_mapa.update_traces(
    marker_line_color="#ffffff",
    marker_line_width=1,
)
fig_mapa.update_geos(
    projection_type="mercator",
    lonaxis_range=[-75, -30],
    lataxis_range=[-35, 7],
    visible=False,
    showframe=False,
    showcoastlines=False,
    showcountries=False,
)
fig_mapa.update_layout(
    margin=dict(l=0, r=0, t=50, b=0),
    height=650,
)
st.plotly_chart(fig_mapa, width="stretch")
st.caption(
    "Fonte: dados públicos do DREI. Limites geográficos: IBGE. "
    "As contagens representam registros, não necessariamente pessoas distintas. "
    "Zero significa nenhum registro correspondente aos filtros na base consultada."
)

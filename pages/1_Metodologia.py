
import streamlit as st

st.set_page_config(
    page_title="Metodologia | Tradutores Públicos Brasil",
    page_icon="📋",
    layout="wide",
)

st.title("Metodologia e Fonte dos Dados")

st.markdown("""
Esta página apresenta a origem dos dados, os procedimentos de
tratamento e as limitações conhecidas do projeto
**Tradutores Públicos Brasil**.

O portal é uma iniciativa independente e não representa
um sistema oficial do Governo Federal.
""")

st.divider()

st.header("1. Fonte dos dados")


st.markdown("""
Os dados utilizados neste projeto foram obtidos a partir
de uma planilha pública disponibilizada pelo
**Departamento Nacional de Registro Empresarial e Integração (DREI)**,
órgão vinculado ao Ministério do Empreendedorismo, da Microempresa
e da Empresa de Pequeno Porte.

**Informações sobre a base utilizada:**

- **Referência da planilha:** setembro de 2026.
- **Periodicidade de atualização pelo DREI:** sob demanda.
- **Formato original:** Excel (.xlsx).
- **Órgão responsável:** DREI.

A base contém informações cadastrais de tradutores públicos
e intérpretes comerciais matriculados nas Juntas Comerciais.

**Fontes oficiais:**

- [Repositório de Dados Abertos — Governo Federal](https://www.gov.br/memp/pt-br/acesso-a-informacao/dados-abertos/repositorio-de-dados-abertos)
- [Baixar planilha original — Setembro de 2026](https://www.gov.br/memp/pt-br/acesso-a-informacao/dados-abertos/dados-tradutores-e-leiloeiro/tabela-padrao-tradutor-e-leiloeiro-publica.xlsx/@@download/file)

**Observação:** setembro de 2026 corresponde à referência
da planilha publicada, não necessariamente à data da última
atualização individual de cada cadastro.
""")

st.info(
    "A base de referência é de setembro de 2026 e possui "
    "atualização sob demanda. A situação cadastral dos "
    "profissionais pode ter mudado desde a publicação. "
    "Para informações atualizadas, consulte a Junta "
    "Comercial responsável.",
    icon="ℹ️"
)

st.header("2. Tratamento dos dados")

st.markdown("""
O processamento foi realizado em Python, utilizando Pandas.

As principais etapas foram:

- Remoção de registros exatamente duplicados.
- Padronização dos nomes dos idiomas.
- Normalização das siglas das unidades federativas.
- Padronização de nomes de municípios.
- Criação de campos auxiliares para identificação e análise.

Os registros originais não foram alterados diretamente.
O processamento gera uma base derivada para consulta.
""")

st.header("3. Quantidade de registros")

col1, col2, col3 = st.columns(3)

col1.metric("Registros originais", "2.306")
col2.metric("Duplicatas exatas removidas", "10")
col3.metric("Registros após tratamento", "2.296")

st.info(
    "Um registro não corresponde necessariamente a um "
    "profissional distinto. Um tradutor pode possuir "
    "habilitação em mais de um idioma."
)

st.header("4. Identificação dos profissionais")

st.markdown("""
Para apresentar os idiomas de um mesmo profissional,
a tabela de consulta utiliza um agrupamento provisório
baseado em:

- Nome do profissional.
- Junta Comercial.
- Matrícula.

Esse agrupamento facilita a consulta, mas não constitui
uma identificação única oficialmente validada.
""")

st.header("5. Auditoria de qualidade")

st.markdown("""
Foi realizada uma auditoria para identificar matrículas
associadas a nomes diferentes dentro da mesma Junta Comercial.

**Resultados encontrados:**

- 7 grupos com possíveis conflitos de identificação.
- 24 registros envolvidos nesses grupos.

Entre os casos identificados estão matrículas não informadas,
nomes diferentes associados à mesma matrícula e possíveis
variações de nomes.

Esses casos não foram corrigidos automaticamente, pois
exigem verificação adicional nas fontes oficiais.
""")

st.header("6. Interpretação dos indicadores")

st.markdown("""
Os gráficos e o mapa apresentam quantidades de registros
da base processada, considerando os filtros selecionados.

**Importante:**

- As contagens não representam necessariamente pessoas distintas.
- A ausência de registros em uma localidade não comprova
  a inexistência de tradutores naquela região.
- Os dados refletem a base utilizada no projeto e podem
  não representar a situação cadastral atual.
- O agrupamento de idiomas na tabela é provisório.
""")

st.header("7. Dados geográficos")

st.markdown("""
Os limites estaduais utilizados no mapa foram obtidos
da API de malhas territoriais do
**Instituto Brasileiro de Geografia e Estatística (IBGE)**.

[Fonte: API de Malhas do IBGE](https://servicodados.ibge.gov.br/api/docs/malhas)
""")

st.divider()

st.caption(
    "Tradutores Públicos Brasil — Projeto independente "
    "de organização e visualização de dados públicos."
)


# Tradutores Públicos Brasil

Portal independente de consulta e visualização de dados públicos sobre tradutores públicos e intérpretes comerciais matriculados nas Juntas Comerciais brasileiras.

O projeto utiliza Python, Pandas, Streamlit e Plotly para facilitar o acesso às informações disponibilizadas pelo Departamento Nacional de Registro Empresarial e Integração (DREI).

## Funcionalidades

- Pesquisa de profissionais por nome, sem diferenciação de acentos ou maiúsculas.
- Filtros por idioma, estado e município.
- Consulta de matrícula, Junta Comercial e situação cadastral.
- Ficha individual com os idiomas cadastrados.
- Exportação dos resultados filtrados em CSV.
- Gráficos de distribuição por idioma e município.
- Mapa interativo do Brasil com limites geográficos do IBGE.
- Página de metodologia e limitações dos dados.

## Fonte dos dados

**Órgão responsável:** Departamento Nacional de Registro Empresarial e Integração (DREI).

**Referência da planilha:** setembro de 2026.

**Periodicidade de atualização:** sob demanda.

[Repositório oficial de dados abertos](https://www.gov.br/memp/pt-br/acesso-a-informacao/dados-abertos/repositorio-de-dados-abertos)

A base original possui 2.306 registros. Após a remoção de 10 duplicatas exatas, foram mantidos 2.296 registros.

Um registro não corresponde necessariamente a um profissional distinto, pois uma pessoa pode possuir habilitação em vários idiomas.

## Tratamento e privacidade

Os dados foram tratados utilizando Python e Pandas.

A versão pública utilizada pelo aplicativo não inclui endereços, telefones, e-mails ou CEPs dos profissionais.

O agrupamento de registros por nome, Junta Comercial e matrícula é provisório e não representa uma identificação única oficialmente validada.

## Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o aplicativo:

```bash
streamlit run app.py
```

## Limitações

A situação cadastral dos profissionais pode ter mudado desde a publicação da planilha.

Para confirmar a habilitação e a situação atual de um tradutor, consulte a Junta Comercial responsável.

## Aviso

Este é um projeto independente, sem vínculo institucional com o DREI ou com o Governo Federal.

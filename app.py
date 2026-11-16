
import streamlit as st

st.set_page_config(
    page_title="Tradutores Públicos Brasil",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

pagina_consulta = st.Page(
    "consulta.py",
    title="Consulta de Tradutores",
    default=True,
)

pagina_metodologia = st.Page(
    "pages/1_Metodologia.py",
    title="Metodologia",
)

st.navigation([pagina_consulta, pagina_metodologia]).run()

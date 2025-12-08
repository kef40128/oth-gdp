
# %%
import streamlit as st


# %%
st.set_page_config(page_title="La Dolce Pizza", layout="wide", page_icon=":pizza:")


#%% 
st.write("# 🍕 La Dolce Pizza")

st.write(f"""
         Willkommen im Verwaltungs- und Analysesystem Ihrer Pizzeria. Über das Menü auf der linken Seite können Sie...
         * Ihre Stammdaten (Kunden und Pizzen) verwalten,
         * Bestellungen erfassen und
         * Ihre Verkaufshistorie analysieren.
         """)
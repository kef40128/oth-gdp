
# %%
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotnine as p9


# %%
st.set_page_config(page_title="La Dolce Pizza", layout="wide", page_icon=":pizza:")


# %%
conn = sqlite3.connect('oth-gp-pizza.db')
# conn = sqlite3.connect('../pizzen.db')


# %%
st.header("Datenanalyse")

query = '''
        SELECT bestellungen.id AS Bestellung_ID, bestellungen.bestellzeitpunkt AS Datum, kunden.name AS Kunde, pizzen.name AS Pizza, pizzen.preis AS Preis
        FROM bestellungen 
        JOIN pizzen ON bestellungen.pizza_id = pizzen.id
        JOIN kunden ON bestellungen.kunde_id = kunden.id
    '''

bestellungen = pd.read_sql_query(query, conn)

conn.close()


# %%
st.write("### Arbeit mit Tabellen")

st.write("##### Übersicht: Bestellungen")
st.dataframe(bestellungen)


col1, col2 = st.columns(2)

with col1:
    st.write("##### Die ersten 5 Einträge")
    st.write(bestellungen.head(5))

with col2:
    st.write("##### Die letzten 5 Einträge")
    st.write(bestellungen.tail(5))


st.write("##### Summary Statistics")
st.write(bestellungen.describe())

st.write("##### Bestimmte Spalten")
st.write(bestellungen[["Datum", "Kunde", "Pizza", "Preis"]])

st.write("##### Bestimmte Zeilen")
st.write(bestellungen[bestellungen['Kunde'] == 'Meier'])

st.write("##### Neue Spalte")
bestellungen['Nettopreis'] = bestellungen['Preis'] * 1.19
st.write(bestellungen)


col1, col2 = st.columns(2)

with col1:
    st.write("##### Aggregation")
    st.write(bestellungen.groupby('Kunde')['Preis'].sum().reset_index())

with col2:
    st.write("##### Sortierung")
    st.write(
    bestellungen \
        .groupby('Kunde')['Preis'] \
        .sum() \
        .reset_index() \
        .sort_values(by='Preis', ascending=False)
    )


# %%
st.divider()
st.write("### Arbeit mit Grafiken")

temp = bestellungen \
        .groupby('Kunde')['Preis'] \
        .sum() \
        .reset_index() \
        .sort_values(by='Preis', ascending=False)


tab1, tab2, tab3 = st.tabs(["Streamlit", "Plotly", "GGplot"])

with tab1:
    st.write("#### Streamlit")
    st.bar_chart(temp, x='Kunde', y='Preis')
with tab2:
    st.write("#### Plotly")
    fig = px.bar(temp, x='Kunde', y='Preis')
    st.plotly_chart(fig)
with tab3:
    st.write("#### GGplot")

    plot = (
        p9.ggplot(temp, p9.aes(x='Kunde', y='Preis'))
        + p9.geom_bar(stat = "identity", fill='blue')
        + p9.ggtitle("Unsere wichtigsten Kunden")
        + p9.theme_bw()
        + p9.theme(axis_text_x=p9.element_text(angle=90, hjust=1))
    )
    st.pyplot(plot.draw())

    temp = bestellungen \
        .groupby(['Kunde', 'Datum'])['Preis'] \
        .sum() \
        .reset_index() \
        .sort_values(by='Preis', ascending=False)
    plot = (
        p9.ggplot(temp, p9.aes(x='Datum', y='Preis'))
        + p9.geom_bar(stat = "identity", fill='blue')
        + p9.ggtitle("Unsere wichtigsten Kunden")
        + p9.theme_bw()
        + p9.theme(axis_text_x=p9.element_text(angle=90, hjust=1))
        + p9.facet_wrap('~Kunde')
    )
    st.pyplot(plot.draw())

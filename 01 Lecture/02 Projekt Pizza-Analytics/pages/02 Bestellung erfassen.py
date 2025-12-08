
# %%
import streamlit as st
import sqlite3
import datetime


# %%
st.set_page_config(page_title="La Dolce Pizza", layout="wide", page_icon=":pizza:")


# %%
conn = sqlite3.connect('oth-gp-pizza.db')
cursor = conn.cursor()


# %%
def bestellung_hinzufuegen():
    # Pizzen aus der Datenbank laden
    cursor.execute("SELECT id, name, preis FROM pizzen")
    pizzen = cursor.fetchall()
    pizza_namen = [f"{row[1]} ({row[2]:.2f} €)" for row in pizzen]
    pizza_ids = [row[0] for row in pizzen]

    # Kunden aus der Datenbank laden
    cursor.execute("SELECT id, name FROM kunden")
    kunden = cursor.fetchall()
    kunden_namen = [row[1] for row in kunden]
    kunden_ids = [row[0] for row in kunden]

    # Auswahl der Pizza und des Kunden
    auswahl_pizza = st.selectbox("Pizza auswählen:", pizza_namen)
    auswahl_kunde = st.selectbox("Kunde auswählen:", kunden_namen)
    menge = st.number_input("Menge:", min_value=1, step=1)


    if st.button("Bestellung hinzufügen"):
        today = datetime.date.today()
        pizza_id = pizza_ids[pizza_namen.index(auswahl_pizza)]
        kunden_id = kunden_ids[kunden_namen.index(auswahl_kunde)]
        cursor.execute("INSERT INTO bestellungen (bestellzeitpunkt, pizza_id, kunde_id, menge) VALUES (?, ?, ?, ?)", (today, pizza_id, kunden_id, menge))
        conn.commit()
        st.success("Bestellung hinzugefügt!")


# %%
st.header("Bestellungen")

bestellung_hinzufuegen()

conn.close()

# %%
import streamlit as st


# %%
st.set_page_config(page_title="La Dolce Pizza", layout="wide", page_icon=":pizza:")


# %%
st.header("Stammdaten")
st.write("""
         In diesem Bereich der Software werden die Stammdaten (Kunden und Pizzen) gepflegt. Wir machen dies in 3 Ausbaustufen (Level).
         """)


#%%
with st.expander("Level 1: Daten anzeigen"):
    l1_pizzen = {
        "Margherita": ["Tomatensauce", "Mozzarella", "Basilikum"],
        "Salami": ["Tomatensauce", "Mozzarella", "Salami"],
        "Funghi": ["Tomatensauce", "Mozzarella", "Champignons"]
    }

    l1_kunden = [
        "Anna Berger",
        "Markus Schmidt",
        "Lisa Müller"
    ]

    st.write('#### Unser Pizza-Sortiment:')

    for pizza in l1_pizzen:
        st.write(f"* {pizza}")

    if st.button('Zeige Kunden'):
        st.write('#### Unsere Kunden:')

        for kunde in l1_kunden:
            st.write(f"* {kunde}")


# %%
with st.expander("Level 2: CRUD - Daten anlegen, ändern und löschen"):
    if 'pizzen' not in st.session_state:
        st.session_state.pizzen = {
            "Margherita": ["Tomatensauce", "Mozzarella", "Basilikum"],
            "Salami": ["Tomatensauce", "Mozzarella", "Salami"],
            "Funghi": ["Tomatensauce", "Mozzarella", "Champignons"]
        }

    # Pizza hinzufügen
    def pizza_hinzufuegen():
        l2_name = st.text_input("Name der neuen Pizza:")
        l2_zutaten = st.text_area("Zutaten (durch Komma getrennt):")
        if st.button("Hinzufügen"):
            if l2_name and l2_zutaten:
                st.session_state.pizzen[l2_name] = l2_zutaten.split(",")
                st.success(f"Pizza '{l2_name}' hinzugefügt!")
            else:
                st.warning("Bitte Name und Zutaten angeben.")

    # Pizza löschen
    def pizza_loeschen():
        l2_name = st.selectbox("Pizza zum Löschen auswählen:", list(st.session_state.pizzen.keys()))
        if st.button("Löschen"):
            del st.session_state.pizzen[l2_name]
            st.success(f"Pizza '{l2_name}' gelöscht!")

    # Pizza ändern
    def pizza_aendern():
        l2_name = st.selectbox("Pizza zum Ändern auswählen:", list(st.session_state.pizzen.keys()))
        l2_neue_zutaten = st.text_area("Neue Zutaten (durch Komma getrennt):", value=", ".join(st.session_state.pizzen[l2_name]))
        if st.button("Ändern"):
            st.session_state.pizzen[l2_name] = l2_neue_zutaten.split(",")
            st.success(f"Pizza '{l2_name}' geändert!")

    # Anzeige der Pizzen
    st.write("#### Unser Pizza-Sortiment:")
    for l2_name, l2_zutaten in st.session_state.pizzen.items():
        st.write(f"- {l2_name}: {', '.join(l2_zutaten)}")

    # Auswahl der Aktion
    l2_aktion = st.selectbox("Aktion auswählen:", ["Pizza hinzufügen", "Pizza löschen", "Pizza ändern"])

    # Ausführung der ausgewählten Aktion
    if l2_aktion == "Pizza hinzufügen":
        pizza_hinzufuegen()
    elif l2_aktion == "Pizza löschen":
        pizza_loeschen()
    elif l2_aktion == "Pizza ändern":
        pizza_aendern()


# %%
with st.expander("Level 3: Arbeit mit Datenbanken"):
    import sqlite3

    conn = sqlite3.connect('oth-gp-pizza.db')
    cursor = conn.cursor()

    # Pizza hinzufügen
    def pizza_hinzufuegen():
        l3_name = st.text_input("Name der Pizza:")
        l3_zutaten = st.text_area("Zutaten (Komma getrennt):")
        l3_preis = st.number_input("Preis:")
        if st.button("Hinzufügen!"):
            if l3_name and l3_zutaten and l3_preis:
                try:
                    cursor.execute("INSERT INTO pizzen (name, zutaten, preis) VALUES (?, ?, ?)", (l3_name, l3_zutaten, l3_preis))
                    conn.commit()
                    st.success(f"Pizza '{l3_name}' hinzugefügt!")
                except sqlite3.IntegrityError:
                    st.error(f"Pizza mit dem Namen '{l3_name}' existiert bereits!")
            else:
                st.warning("Bitte Name und Zutaten angeben.")

    # Pizza löschen
    def pizza_loeschen():
        cursor.execute("SELECT name FROM pizzen")
        l3_pizza_namen = [row[0] for row in cursor.fetchall()]
        if l3_pizza_namen:
            l3_name = st.selectbox("Pizza zum Löschen wählen:", l3_pizza_namen)
            if st.button("Löschen!"):
                cursor.execute("DELETE FROM pizzen WHERE name = ?", (l3_name,))
                conn.commit()
                st.success(f"Pizza '{l3_name}' gelöscht!")
        else:
            st.warning("Keine Pizzen zum Löschen vorhanden.")

    # Pizza ändern
    def pizza_aendern():
        cursor.execute("SELECT name FROM pizzen")
        l3_pizza_namen = [row[0] for row in cursor.fetchall()]
        if l3_pizza_namen:
            l3_name = st.selectbox("Pizza zum Ändern auswählen:", l3_pizza_namen)
            cursor.execute("SELECT zutaten FROM pizzen WHERE name = ?", (l3_name,))
            l3_aktuelle_zutaten = cursor.fetchone()[0]
            cursor.execute("SELECT preis FROM pizzen WHERE name = ?", (l3_name,))
            l3_aktueller_preis = cursor.fetchone()[0]
            l3_neue_zutaten = st.text_area("Neue Zutaten (durch Komma getrennt):", value=l3_aktuelle_zutaten)
            l3_neuer_preis = st.number_input("Neuer Preis:", value=l3_aktueller_preis)
            if st.button("Ändern!"):
                cursor.execute("UPDATE pizzen SET zutaten = ? WHERE name = ?", (l3_neue_zutaten, l3_name))
                cursor.execute("UPDATE pizzen SET preis = ? WHERE name = ?", (l3_neuer_preis, l3_name))
                conn.commit()
                st.success(f"Pizza '{l3_name}' geändert!")
        else:
            st.warning("Keine Pizzen zum Ändern vorhanden.")

    # Anzeige der Pizzen
    st.write("#### Unser Pizza-Sortiment:")
    cursor.execute("SELECT name, zutaten, preis FROM pizzen")
    for row in cursor.fetchall():
        st.write(f"- {row[0]}: {row[1]}")

    # Auswahl der Aktion
    l3_aktion = st.selectbox("Aktion wählen:", ["Pizza hinzufügen", "Pizza löschen", "Pizza ändern"])

    # Ausführung der ausgewählten Aktion
    if l3_aktion == "Pizza hinzufügen":
        pizza_hinzufuegen()
    elif l3_aktion == "Pizza löschen":
        pizza_loeschen()
    elif l3_aktion == "Pizza ändern":
        pizza_aendern()

    # Datenbankverbindung schließen
    conn.close()


# %%


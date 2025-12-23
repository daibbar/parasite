import streamlit as st
import pandas as pd
from datetime import date
import datetime
from src.database import run_query, get_data

st.set_page_config(page_title="Gestion des Clubs", page_icon="♟️")
st.title("♟️ Gestion Spécifique des Clubs")

st.subheader("Créer un nouveau Club")

with st.form("form_add_club"):
    club_name, date_creation = st.columns(2);
    with club_name:
        st.text_input("Nom du club")
    with date_creation:
        st.date_input(
        "Date de Creation",
        value=datetime.date.today(),
        min_value=datetime.date(2007,1,1),
        max_value=datetime.date.today(),
        format="DD/MM/YYYY"
    )
    category = st.selectbox("Category du Club", "entertaiment")
    description = st.text_area("Description du Club")
    submitted = st.form_submit_button("Enregistrer le Club")

    if submitted and club_name and date_creation and category:
        try:
            query = "INSERT INTO clubs (nom, category, date_creation, club_description) VALUES (?,?,?,?)"
            run_query(query, (club_name, category, date_creation, description))
            st.success(f"le {club_name} a ete ajoute avec succee! ")
        except Exception as e:
            st.error(f"Erreur lors de l'ajout: {e}")




st.divider("----")
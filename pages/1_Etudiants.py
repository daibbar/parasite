import streamlit as st
import pandas as pd
from src.database import run_query, get_data

st.set_page_config(page_title="Étudiants", page_icon="🎓")
st.title("Étudiants")

st.subheader("Statistiques")

col5, col6, col7 = st.columns(3)
etudiants_query = "SELECT COUNT(id_etudiant) FROM etudiants;" 
etudiant_frame = get_data(etudiants_query)
etudiants_total = etudiant_frame.iloc[0,0]
col5.metric(label="le nombre totale des etudiants",value=etudiants_total)

active_etudiants_query = "SELECT COUNT(DISTINCT id_etudiant) FROM clubs_membres;" 
active_etudiant_frame = get_data(active_etudiants_query)
active_etudiants_total = active_etudiant_frame.iloc[0,0]
col6.metric(label="les etudiants actifs dans un club",value=active_etudiants_total)

st.markdown("---")


st.markdown("### Manger les étudiants")
col8, col9 = st.columns(2)

col8.markdown("##### Ajouter un etudiant")
with col8.form("form_add_etudiant"):
    col1, col2 = st.columns(2)
    nom = col2.text_input("Nom")
    prenom = col1.text_input("Prénom")
    col3, col4 = st.columns(2)
    cne = col3.text_input("CNE")
    filiere = col4.selectbox("Filière", ["IID", "GI", "MGSI", "IRIC", "GE", "GPEE"])
    email = st.text_input("Email")
    submitted = st.form_submit_button("Enregistrer")
    
    if submitted:
        if nom and prenom and email and cne:
            try:
                filiereId_query = "SELECT id_filliere FROM fillieres WHERE nom = ?;"
                filiere_id_frame = get_data(filiereId_query, (filiere,))
                filiere_id = int(filiere_id_frame.iloc[0,0])
                query = "INSERT INTO etudiants (nom, prenom, cne, email, id_filliere) VALUES (?, ?, ?, ?, ?);"
                run_query(query, (nom, prenom, cne, email, filiere_id))
                st.success(f"Étudiant {nom} {prenom} ajouté avec succès !")
            except Exception as e:
                st.error(f"Erreur lors de l'ajout : {e}")
        else:
            st.warning("Veuillez remplir tous les champs obligatoires.")

col9.markdown("##### Supprimer un etudiant")
with col9.form("form_delete_etudiant"):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    cne = st.text_input("CNE")
    submitted = st.form_submit_button("Supprimer")
    
    if submitted:
        if nom and prenom and cne:
            try:
                etudiants_frame = get_data("SELECT * FROM etudiants;")
                for etudiant in etudiants_frame.itertuples():
                    if etudiant.cne == cne and etudiant.prenom == prenom and etudiant.nom == nom:
                        query = "DELETE FROM etudiants WHERE cne = ?;"
                        run_query(query, (cne,))
                        break
                    elif not(etudiant.cne == cne and etudiant.prenom == prenom and etudiant.nom == nom):
                        st.error("il y a une erreur dans les informations!")

            except Exception as e:
                st.error(f"Erreur lors de l'ajout : {e}")
        else:
            st.warning("Veuillez remplir tous les champs obligatoires.")

st.markdown("---")

st.subheader("List des etudiants")
st.dataframe(get_data("SELECT * FROM etudiants"), use_container_width=True)

st.markdown("---")


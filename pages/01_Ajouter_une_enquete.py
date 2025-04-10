import streamlit as st
import os
from datetime import date
from database import ajouter_enquete

# Configuration
st.set_page_config(page_title="Ajouter une enquête", layout="wide")
st.title("➕ Ajouter une nouvelle enquête")

# Création du dossier uploads si besoin
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Formulaire d'ajout
with st.form("form_enquete"):
    col1, col2 = st.columns(2)

    with col1:
        num_enquete = st.text_input("Numéro d'enquête (ex : EV003)")
        responsable = st.text_input("Responsable")
        lieu = st.text_input("Lieu de l’enquête")

    with col2:
        date_limite = st.date_input("Date limite", min_value=date.today())
        statut = st.selectbox("Statut", ["Planifiée", "En cours", "Terminée", "Clôturée"])
        type_incident = st.selectbox("Type d’incident", ["Sécurité", "Technique", "Autre"])

    fichier = st.file_uploader("Pièce jointe (PDF, image, etc.)", type=["pdf", "png", "jpg", "jpeg"])

    submitted = st.form_submit_button("Ajouter")

if submitted:
    chemin_fichier = ""
    if fichier:
        chemin_fichier = os.path.join("uploads", fichier.name)
        with open(chemin_fichier, "wb") as f:
            f.write(fichier.read())

    ajouter_enquete(
        num_enquete=num_enquete,
        responsable=responsable,
        date_limite=str(date_limite),
        statut=statut,
        lieu=lieu,
        type_incident=type_incident,
        fichier=chemin_fichier
    )

    st.success("✅ Enquête ajoutée avec succès !")
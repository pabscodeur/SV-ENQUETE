
import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta
from database import init_db, ajouter_enquete, recuperer_enquetes
from calendar_gantt import afficher_calendrier_gantt
from edit_delete import afficher_modification_et_suppression
from filtre import appliquer_filtres

# ======================== INITIALISATION ========================
init_db()

st.set_page_config(page_title="Gestion des Enquêtes", layout="wide")
st.title("🔍 Outil de gestion des enquêtes de sécurité")
st.subheader("Version 0.7 — Filtres avancés et recherche globale")

# Création dossier uploads
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ======================== FORMULAIRE D'AJOUT ========================
st.write("## ➕ Ajouter une enquête")

with st.form("form_enquete"):
    col1, col2 = st.columns(2)
    with col1:
        num_enquete = st.text_input("Numéro d'enquête (ex : EV003)")
        responsable = st.text_input("Responsable")
        lieu = st.text_input("Lieu")
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

    ajouter_enquete(num_enquete, responsable, str(date_limite), statut, lieu, type_incident, chemin_fichier)
    st.success("✅ Enquête enregistrée avec succès !")

# ======================== RÉCUPÉRATION DES ENQUÊTES ========================
enquetes = recuperer_enquetes()
st.write("## 📋 Enquêtes enregistrées")

if enquetes:
    df = pd.DataFrame(enquetes, columns=[
        "ID", "Enquête", "Responsable", "Date limite", "Statut",
        "Lieu", "Type incident", "Fichier"
    ])
    df["Date limite"] = pd.to_datetime(df["Date limite"], errors="coerce")

    # Calcul de l’état du délai
    def calcul_etat_delai(d):
        if pd.isnull(d):
            return "—"
        if d.date() < date.today():
            return "🔴 Retard"
        elif d.date() <= date.today() + timedelta(days=3):
            return "🟡 À rendre bientôt"
        else:
            return "🟢 OK"

    df["État délai"] = df["Date limite"].apply(calcul_etat_delai)

    # ======================== FILTRES (nouveau module) ========================
    df_filtered = appliquer_filtres(df)

    if df_filtered.empty:
        st.warning("Aucun résultat après application des filtres.")
    else:
        st.dataframe(df_filtered.drop(columns=["ID"]), use_container_width=True)
        st.write("### ✏️ Modifier ou Supprimer une enquête")
        afficher_modification_et_suppression(df_filtered)

else:
    st.info("Aucune enquête enregistrée.")

# ======================== CALENDRIER GANTT ========================
st.write("## 📅 Calendrier des enquêtes")
if enquetes:
    df_cal = pd.DataFrame(enquetes, columns=[
        "ID", "Enquête", "Responsable", "Date limite", "Statut",
        "Lieu", "Type incident", "Fichier"
    ])
    if not df_cal.empty:
        afficher_calendrier_gantt(df_cal)

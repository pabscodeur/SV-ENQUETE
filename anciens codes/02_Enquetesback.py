import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta
from database import recuperer_enquetes
from edit_delete import afficher_modification_et_suppression

st.set_page_config(page_title="Détail Enquête", layout="wide", initial_sidebar_state="auto")

# Cacher la page du sommaire
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] a[href$="04_Detail_enquete"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(page_title="Enquêtes", layout="wide")
st.title("📋 Liste des enquêtes enregistrées")

# --- Récupération
enquetes = recuperer_enquetes()
if not enquetes:
    st.info("Aucune enquête enregistrée.")
    st.stop()

# --- Conversion en DataFrame
df = pd.DataFrame(enquetes, columns=[
    "ID", "Enquête", "Responsable", "Date limite", "Statut",
    "Lieu", "Type incident", "Fichier"
])
df["Date limite"] = pd.to_datetime(df["Date limite"], errors="coerce")

# --- Calcul de l'état du délai
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

# --- 🔍 Filtres dynamiques
st.write("### 🔎 Filtres")
col1, col2, col3 = st.columns(3)
with col1:
    statut_filter = st.multiselect("Statut", df["Statut"].unique())
with col2:
    responsable_filter = st.multiselect("Responsable", df["Responsable"].unique())
with col3:
    delai_filter = st.multiselect("État du délai", df["État délai"].unique())

search = st.text_input("🔍 Recherche (mot-clé : enquête, responsable, lieu)").lower()

if statut_filter:
    df = df[df["Statut"].isin(statut_filter)]
if responsable_filter:
    df = df[df["Responsable"].isin(responsable_filter)]
if delai_filter:
    df = df[df["État délai"].isin(delai_filter)]
if search:
    df = df[
        df["Enquête"].str.lower().str.contains(search) |
        df["Responsable"].str.lower().str.contains(search) |
        df["Lieu"].str.lower().str.contains(search)
    ]

if df.empty:
    st.warning("Aucun résultat.")
    st.stop()

# --- Colonne cliquable "Pièce jointe" pour accéder à la page détail
def bouton_detail(row):
    label = "📄 Info"
    if row["Fichier"] and os.path.exists(row["Fichier"]):
        label += f" ({os.path.basename(row['Fichier'])})"
    bouton = st.button(label, key=f"btn_{row['ID']}")
    if bouton:
        st.session_state["selected_enquete"] = row.to_dict()
        st.switch_page("pages/04_Detail_enquete.py")
    return ""

df["Pièce jointe"] = df.apply(bouton_detail, axis=1)

# --- Tableau affiché
df_affichage = df[[
    "Enquête", "Responsable", "Statut", "Lieu", "Type incident",
    "Date limite", "État délai", "Pièce jointe"
]]
st.dataframe(df_affichage, use_container_width=True, hide_index=True)

# --- Section édition / suppression
st.write("### ✏️ Modifier ou Supprimer une enquête")
afficher_modification_et_suppression(df)

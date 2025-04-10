import streamlit as st
import pandas as pd
import os
from datetime import date, timedelta
from database import recuperer_enquetes
from edit_delete import afficher_modification_et_suppression

st.set_page_config(page_title="Enquêtes", layout="wide")
st.title("📋 Liste des enquêtes enregistrées")

# --- Récupération
enquetes = recuperer_enquetes()
if not enquetes:
    st.info("Aucune enquête enregistrée.")
    st.stop()

# --- Création du DataFrame
df = pd.DataFrame(enquetes, columns=[
    "ID", "Enquête", "Responsable", "Date limite", "Statut",
    "Lieu", "Type incident", "Fichier"
])
df["Date limite"] = pd.to_datetime(df["Date limite"], errors="coerce")

# --- Nettoyage des valeurs manquantes
df = df.fillna("—")
df.replace("", "—", inplace=True)

# --- Calcul de l'état du délai
def calcul_etat_delai(d):
    if d == "—" or pd.isnull(d):
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

# --- 🎨 CSS mode sombre
st.markdown("""
<style>
.table-header {
    font-weight: bold;
    background-color: #2b2b2b;
    color: #f5f5f5;
    padding: 0.6rem;
    border-bottom: 1px solid #444;
    border-top: 1px solid #444;
    text-align: center;
    font-size: 0.95rem;
}
.table-cell {
    background-color: #1e1e1e;
    color: #e0e0e0;
    padding: 0.5rem;
    border-bottom: 1px solid #333;
    text-align: center;
    font-size: 0.9rem;
    font-family: "Segoe UI", sans-serif;
}
</style>
""", unsafe_allow_html=True)

st.write("### 📊 Résultat")

# En-têtes du tableau
cols = st.columns([1.5, 1.5, 1.2, 1.5, 1.5, 1.5, 1.2, 0.8])
headers = [
    "🧾 Enquête", "👤 Responsable", "📌 Statut", "📍 Lieu",
    "⚠️ Type d'incident", "📅 Date limite", "⏳ Délai", "🔍"
]
for col, title in zip(cols, headers):
    col.markdown(f"<div class='table-header'>{title}</div>", unsafe_allow_html=True)

# Lignes avec données + bouton
for _, row in df.iterrows():
    c1, c2, c3, c4, c5, c6, c7, c8 = st.columns([1.5, 1.5, 1.2, 1.5, 1.5, 1.5, 1.2, 0.8])
    with c1:
        st.markdown(f"<div class='table-cell'>{row['Enquête']}</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='table-cell'>{row['Responsable']}</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='table-cell'>{row['Statut']}</div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='table-cell'>{row['Lieu']}</div>", unsafe_allow_html=True)
    with c5:
        st.markdown(f"<div class='table-cell'>{row['Type incident']}</div>", unsafe_allow_html=True)
    with c6:
        date_affiche = str(row["Date limite"].date()) if row["Date limite"] != "—" else "—"
        st.markdown(f"<div class='table-cell'>{date_affiche}</div>", unsafe_allow_html=True)
    with c7:
        st.markdown(f"<div class='table-cell'>{row['État délai']}</div>", unsafe_allow_html=True)
    with c8:
        if st.button("🔍", key=f"btn_detail_{row['ID']}"):
            st.session_state["selected_enquete"] = row.to_dict()
            st.switch_page("pages/04_Detail_enquete.py")

# --- Section édition / suppression
st.write("### ✏️ Modifier ou Supprimer une enquête")
afficher_modification_et_suppression(df)

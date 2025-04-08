
import streamlit as st
import pandas as pd

def appliquer_filtres(df):
    st.write("### 🔎 Filtres (tableau HTML)")

    # Recherche globale
    search = st.text_input("Rechercher dans toutes les colonnes")

    # Filtres spécifiques
    col1, col2, col3 = st.columns(3)
    with col1:
        statut_filter = st.multiselect("Statut", df["Statut"].unique())
    with col2:
        responsable_filter = st.multiselect("Responsable", df["Responsable"].unique())
    with col3:
        etat_filter = st.multiselect("État du délai", df["État délai"].unique())

    # Application des filtres
    filtered_df = df.copy()

    if search:
        search_lower = search.lower()
        filtered_df = filtered_df[
            filtered_df.apply(lambda row: row.astype(str).str.lower().str.contains(search_lower).any(), axis=1)
        ]

    if statut_filter:
        filtered_df = filtered_df[filtered_df["Statut"].isin(statut_filter)]
    if responsable_filter:
        filtered_df = filtered_df[filtered_df["Responsable"].isin(responsable_filter)]
    if etat_filter:
        filtered_df = filtered_df[filtered_df["État délai"].isin(etat_filter)]

    return filtered_df

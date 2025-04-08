import plotly.express as px
import pandas as pd
import streamlit as st

def afficher_calendrier_gantt(df):
    # On copie le DataFrame pour ne pas le modifier directement
    df_gantt = df.copy()

    # Convertir en datetime si ce n’est pas déjà fait
    df_gantt["Date limite"] = pd.to_datetime(df_gantt["Date limite"], errors="coerce")

    # Créer une colonne "Début" = 3 jours avant la date limite
    df_gantt["Début"] = df_gantt["Date limite"] - pd.to_timedelta(3, unit="d")

    # Créer un champ texte pour affichage dans la barre
    df_gantt["Tâche"] = df_gantt["Enquête"] + " — " + df_gantt["Responsable"]

    fig = px.timeline(
        df_gantt,
        x_start="Début",
        x_end="Date limite",
        y="Tâche",
        color="Statut",
        title="📅 Calendrier Gantt des enquêtes",
        labels={"Tâche": "Enquête"},
    )

    # Inverser l’ordre des tâches pour affichage du haut vers le bas
    fig.update_yaxes(autorange="reversed")

    # Affichage dans Streamlit
    st.plotly_chart(fig, use_container_width=True)
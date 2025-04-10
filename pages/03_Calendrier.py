import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
from database import recuperer_enquetes

st.set_page_config(page_title="Calendrier", layout="wide")

st.title("📅 Calendrier des enquêtes")

enquetes = recuperer_enquetes()

if not enquetes:
    st.info("Aucune enquête enregistrée.")
    st.stop()

# Colonnes attendues dans la base de données
colonnes = [
    "id", "num_enquete", "responsable", "date_limite", "statut",
    "lieu", "type_incident", "fichier"
]

df = pd.DataFrame(enquetes, columns=colonnes)

# Construction des événements pour le calendrier
events = []

for _, row in df.iterrows():
    if row["date_limite"] != "" and row["date_limite"] is not None:
        events.append({
            "title": row["num_enquete"],
            "start": str(row["date_limite"]),
            "end": str(row["date_limite"]),
            "color": "#1976D2",
            "id": row["id"]
        })

calendar_options = {
    "initialView": "dayGridMonth",
    "locale": "fr",
    "height": 750,
    "editable": False,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek"
    }
}

selected = calendar(events=events, options=calendar_options)

if selected:
    if "id" in selected:
        st.session_state["selected_enquete_id"] = selected["id"]
        st.switch_page("pages/04_Detail_enquete.py")
    else:
        st.warning("⚠️ Merci de cliquer sur une enquête pour accéder à son détail.")


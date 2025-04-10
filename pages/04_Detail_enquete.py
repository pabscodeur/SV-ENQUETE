import streamlit as st
import os

st.set_page_config(page_title="Détail Enquête", layout="wide", initial_sidebar_state="auto")

# Masquer la page dans le sommaire Streamlit via son nom exact affiché
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] a:has(span:contains("Enquête détaillée")) {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📝 Détail de l'enquête sélectionnée")

if "selected_enquete" not in st.session_state:
    st.warning("Aucune enquête sélectionnée.")
    st.stop()

enquete = st.session_state["selected_enquete"]

st.markdown("### Informations générales")
st.write(f"**Numéro d'enquête :** {enquete['Enquête']}")
st.write(f"**Responsable :** {enquete['Responsable']}")
st.write(f"**Lieu :** {enquete['Lieu']}")
st.write(f"**Type d’incident :** {enquete['Type incident']}")
st.write(f"**Statut :** {enquete['Statut']}")
st.write(f"**Date limite :** {enquete['Date limite']}")
st.write(f"**État du délai :** {enquete['État délai']}")

st.markdown("---")
st.markdown("### 📎 Pièce jointe")

if "Fichier" in enquete and enquete["Fichier"] and os.path.exists(enquete["Fichier"]):
    with open(enquete["Fichier"], "rb") as file:
        file_bytes = file.read()
        filename = os.path.basename(enquete["Fichier"])
        st.download_button(
            label=f"📥 Télécharger {filename}",
            data=file_bytes,
            file_name=filename
        )
else:
    st.info("Aucune pièce jointe disponible.")

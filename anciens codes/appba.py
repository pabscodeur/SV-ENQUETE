import streamlit as st
import base64

# ========== CONFIG ==========
st.set_page_config(
    page_title="SV ENQUÊTES",
    page_icon="🛠️",
    layout="wide"
)

# ========== FOND D'ÉCRAN ==========
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

set_background("images/fond_accueil.png")

# ========== STYLE LISIBILITÉ AMÉLIORÉE ==========
st.markdown("""
<style>
.glass-container {
    background: rgba(30, 30, 30, 0.55);  /* plus sombre */
    border-radius: 20px;
    padding: 45px 55px;
    margin-top: 60px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: white;
    box-shadow: 0 8px 40px rgba(0, 0, 0, 0.4);
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
    font-size: 18px;
    line-height: 1.6;
}
.glass-container h1, .glass-container h2, .glass-container p, .glass-container li {
    color: #f5f5f5;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

# ========== CONTENU ==========
st.markdown("""
<div class="glass-container">

<h1>🛠️ Plateforme SV ENQUÊTES</h1>
<p>Bienvenue sur l'outil interne de gestion des enquêtes de sécurité des vols.</p>

<hr>

<h2>📌 Fonctionnalités :</h2>
<ul>
  <li>🔵 Suivi des enquêtes avec échéances</li>
  <li>🟣 Filtres dynamiques par responsable, statut, délai</li>
  <li>🧷 Pièces jointes téléchargeables</li>
  <li>🛠️ Modification & suppression rapides</li>
  <li>📅 Calendrier Gantt pour visualisation globale</li>
</ul>

<hr>

<p>👉 <strong>Utilisez le menu de gauche</strong> pour naviguer entre les différentes pages.</p>

</div>
""", unsafe_allow_html=True)

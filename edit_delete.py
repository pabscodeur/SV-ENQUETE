import streamlit as st
import os
from database import modifier_enquete, supprimer_enquete

def afficher_modification_et_suppression(df):
    # 🔁 Gestion du rechargement manuel avec session_state
    if st.session_state.get("rerun", False):
        st.session_state["rerun"] = False
        st.rerun()

    for _, row in df.iterrows():
        with st.expander(f"✏️ Modifier ou supprimer : {row['Enquête']}"):
            with st.form(f"form_{row['ID']}"):
                col1, col2 = st.columns(2)

                with col1:
                    new_num = st.text_input("Numéro d'enquête", value=row["Enquête"])
                    new_resp = st.text_input("Responsable", value=row["Responsable"])
                    new_lieu = st.text_input("Lieu", value=row["Lieu"])

                with col2:
                    new_date = st.date_input("Date limite", value=row["Date limite"])
                    new_statut = st.selectbox(
                        "Statut", 
                        ["Planifiée", "En cours", "Terminée", "Clôturée"], 
                        index=["Planifiée", "En cours", "Terminée", "Clôturée"].index(row["Statut"])
                    )
                    new_type = st.selectbox(
                        "Type d’incident", 
                        ["Sécurité", "Technique", "Autre"], 
                        index=["Sécurité", "Technique", "Autre"].index(row["Type incident"])
                    )

                new_file = st.file_uploader("Modifier le fichier joint", type=["pdf", "png", "jpg", "jpeg"])

                submit_modif = st.form_submit_button("💾 Enregistrer les modifications")
                supprimer = st.form_submit_button("🗑️ Supprimer cette enquête")

                if submit_modif:
                    chemin_fichier = row["Fichier"]
                    if new_file:
                        chemin_fichier = os.path.join("uploads", new_file.name)
                        with open(chemin_fichier, "wb") as f:
                            f.write(new_file.read())

                    modifier_enquete(
                        id=row["ID"],
                        num_enquete=new_num,
                        responsable=new_resp,
                        date_limite=str(new_date),
                        statut=new_statut,
                        lieu=new_lieu,
                        type_incident=new_type,
                        fichier=chemin_fichier
                    )
                    st.success("✅ Enquête modifiée avec succès !")
                    st.session_state["rerun"] = True

                if supprimer:
                    supprimer_enquete(row["ID"])
                    st.warning("🗑️ Enquête supprimée.")
                    st.session_state["rerun"] = True

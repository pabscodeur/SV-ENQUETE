import streamlit as st
import pandas as pd
from database import modifier_enquete, supprimer_enquete

def afficher_modification_et_suppression(df):
    st.write("## ✏️ Modifier ou Supprimer une enquête")

    for index, row in df.iterrows():
        with st.expander(f"Modifier/Supprimer : {row['Enquête']}"):
            col1, col2 = st.columns([4, 1])
            with col1:
                with st.form(f"modif_form_{row['ID']}"):
                    new_num = st.text_input("Numéro d'enquête", value=row["Enquête"])
                    new_resp = st.text_input("Responsable", value=row["Responsable"])
                    new_date = st.date_input("Date limite", value=row["Date limite"].date())
                    new_statut = st.selectbox("Statut", ["Planifiée", "En cours", "Terminée", "Clôturée"], index=["Planifiée", "En cours", "Terminée", "Clôturée"].index(row["Statut"]))
                    new_lieu = st.text_input("Lieu", value=row["Lieu"])
                    new_type = st.selectbox("Type d’incident", ["Sécurité", "Technique", "Autre"], index=["Sécurité", "Technique", "Autre"].index(row["Type incident"]))
                    submitted = st.form_submit_button("Enregistrer les modifications")
                    if submitted:
                        modifier_enquete(row["ID"], new_num, new_resp, str(new_date), new_statut, new_lieu, new_type, row["Fichier"])
                        st.success("✅ Enquête modifiée")
                        st.rerun()

            with col2:
                if st.button("Supprimer", key=f"del_{row['ID']}"):
                    supprimer_enquete(row["ID"])
                    st.warning("❌ Enquête supprimée")
                    st.rerun()

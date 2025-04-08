
import pandas as pd
import os

def afficher_table_html(df):
    def lien_cliquable(file_path):
        if file_path and os.path.exists(file_path):
            filename = os.path.basename(file_path)
            return f'<a href="{file_path}" target="_blank">{filename}</a>'
        else:
            return "—"

    def color_etat_delai(val):
        if val == "🔴 Retard":
            return f'<span style="background-color:#f8d7da;color:#721c24;padding:3px 6px;border-radius:4px;">{val}</span>'
        elif val == "🟡 À rendre bientôt":
            return f'<span style="background-color:#fff3cd;color:#856404;padding:3px 6px;border-radius:4px;">{val}</span>'
        elif val == "🟢 OK":
            return f'<span style="background-color:#d4edda;color:#155724;padding:3px 6px;border-radius:4px;">{val}</span>'
        return val

    df["Pièce jointe"] = df["Fichier"].apply(lien_cliquable)
    df["État délai"] = df["État délai"].apply(color_etat_delai)
    df_affiche = df.drop(columns=["ID", "Fichier"])
    return df_affiche.to_html(index=False, escape=False)

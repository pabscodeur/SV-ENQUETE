# 🛠️ SV ENQUÊTES — Plateforme de gestion des enquêtes de sécurité

Cette application a été conçue pour faciliter la gestion des enquêtes de sécurité au sein d'un service professionnel : suivi des échéances, filtres dynamiques, calendrier interactif et pièce jointe cliquable.

---

## 🚀 Fonctionnalités

- **Ajout d'enquêtes** avec statut, date limite, type d'incident, lieu et fichier joint.
- **Tableau intelligent** avec :
  - Recherche par mot-clé 🔍
  - Filtres dynamiques par responsable, délai et statut
  - Affichage des pièces jointes via lien cliquable
  - Détails étendus
- **Modification / Suppression** rapide via un panneau dédié
- **Vue calendrier Gantt** pour suivre les échéances

---

## 🧭 Navigation

Le menu latéral permet de naviguer entre les pages :

1. **➕ Ajouter une enquête** : formulaire d'ajout
2. **📋 Enquêtes** : consultation avec filtres & actions
3. **📅 Calendrier** : visualisation temporelle

---

## 📁 Organisation des fichiers

```
gestion_enquetes/
│
├── app.py                    # Hub principal (ne contient que la config générale)
├── database.py               # Gestion de la base SQLite
├── table.py                  # Filtres et transformation de données
├── edit_delete.py            # Fonctions de modification/suppression
├── detail.py                 # Affichage des détails cliquables
├── calendar_gantt.py         # Vue calendrier avec Plotly
├── uploads/                  # Contient les fichiers joints
└── pages/
    ├── 01_Ajouter_une_enquête.py
    ├── 02_Enquêtes.py
    └── 03_Calendrier.py
```

---

## ✅ Lancer l'application

Dans le terminal PowerShell :
```bash
streamlit run app.py
```

---

## 🌐 Déploiement en ligne

Utilisez [Streamlit Community Cloud](https://streamlit.io/cloud) :
- Connectez votre dépôt GitHub
- Sélectionnez `app.py` comme point d'entrée
- Autorisez les accès si nécessaire

---

## 🤝 Contributeurs

Développement réalisé pour une utilisation au sein du service SV-GR (Sécurité des Vols — Gestion des Risques).

---

🛡️ **Développé avec Streamlit.**
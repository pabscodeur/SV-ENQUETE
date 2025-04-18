import sqlite3

# Connexion et création si besoin
def init_db():
    conn = sqlite3.connect("enquetes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enquetes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_enquete TEXT,
            responsable TEXT,
            date_limite TEXT,
            statut TEXT,
            lieu TEXT,
            type_incident TEXT,
            fichier TEXT
        )
    """)
    conn.commit()
    conn.close()


def ajouter_enquete(num_enquete, responsable, date_limite, statut, lieu, type_incident, fichier):
    conn = sqlite3.connect("enquetes.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO enquetes (num_enquete, responsable, date_limite, statut, lieu, type_incident, fichier)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (num_enquete, responsable, date_limite, statut, lieu, type_incident, fichier))
    conn.commit()
    conn.close()


def recuperer_enquetes():
    conn = sqlite3.connect("enquetes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM enquetes")
    lignes = cursor.fetchall()
    conn.close()
    return lignes




def modifier_enquete(id, num_enquete, responsable, date_limite, statut, lieu, type_incident, fichier):
    conn = sqlite3.connect("enquetes.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE enquetes
        SET num_enquete=?, responsable=?, date_limite=?, statut=?, lieu=?, type_incident=?, fichier=?
        WHERE id=?
    """, (num_enquete, responsable, date_limite, statut, lieu, type_incident, fichier, id))
    conn.commit()
    conn.close()


def supprimer_enquete(id):
    conn = sqlite3.connect("enquetes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enquetes WHERE id=?", (id,))
    conn.commit()
    conn.close()


import sqlite3

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect('utilisateurs.db')
cursor = conn.cursor()

# Création de la table utilisateurs
cursor.execute('''
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    identifiant TEXT NOT NULL,
    mot_de_passe TEXT NOT NULL,
    role TEXT NOT NULL
)
''')

# Insertion de quelques utilisateurs pour le test
utilisateurs = [
    ('admin', 'admin_pass', 'admin'),
    ('user1', 'user1_pass', 'user'),
    ('user2', 'user2_pass', 'user')
]

cursor.executemany('''
INSERT INTO utilisateurs (identifiant, mot_de_passe, role)
VALUES (?, ?, ?)
''', utilisateurs)

# Validation des modifications et fermeture de la connexion
conn.commit()
conn.close()

print("Base de données créée avec succès.")

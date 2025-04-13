import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Fenêtre d'identification")
        self.root.geometry("500x500")

        self.compteur_essais = 0
        self.conn = sqlite3.connect("utilisateurs.db")

        self.authenticated = False
        self.create_table()

        self.create_widgets()

    def create_widgets(self):
        # Appliquer un thème moderne avec ttk
        self.root.style = ttk.Style()
        self.root.style.theme_use("clam")  # Choisir un thème moderne

        # Personnalisation des couleurs et des polices
        self.root.config(bg="#2e2e2e")  # Fond de la fenêtre en gris foncé
        self.root.option_add("*Font", "Helvetica 12")

        # Création des labels et champs de texte
        self.label_identifiant = ttk.Label(
            self.root, text="Identifiant :", background="#2e2e2e", foreground="white"
        )
        self.label_identifiant.pack(pady=20)
        self.entry_identifiant = ttk.Entry(self.root, font=("Helvetica", 12))
        self.entry_identifiant.pack(pady=10)

        self.label_mot_de_passe = ttk.Label(
            self.root, text="Mot de passe :", background="#2e2e2e", foreground="white"
        )
        self.label_mot_de_passe.pack(pady=20)
        self.entry_mot_de_passe = ttk.Entry(self.root, font=("Helvetica", 12), show="*")
        self.entry_mot_de_passe.pack(pady=10)

        # Option pour afficher ou masquer le mot de passe
        self.var_afficher_mdp = tk.BooleanVar()
        self.checkbox_afficher_mdp = ttk.Checkbutton(
            self.root,
            text="Afficher le mot de passe",
            variable=self.var_afficher_mdp,
            command=self.afficher_mdp,
            style="TCheckbutton",
        )
        self.checkbox_afficher_mdp.pack(pady=10)

        # Personnalisation de la case à cocher
        self.root.style.configure(
            "TCheckbutton", background="#2e2e2e", foreground="white"
        )

        # Création du bouton de connexion
        self.bouton_connexion = ttk.Button(
            self.root,
            text="Se connecter",
            command=self.verifier_identifiants,
            style="TButton",
        )
        self.bouton_connexion.pack(pady=40)

        # Personnaliser le bouton "Se connecter"
        self.root.style.configure(
            "TButton",
            background="#0078d4",
            foreground="white",
            font=("Helvetica", 12),
            padding=6,
        )

        # Ajouter un effet de survol pour le bouton
        self.bouton_connexion.bind("<Enter>", self.on_enter)
        self.bouton_connexion.bind("<Leave>", self.on_leave)

    def afficher_mdp(self):
        if self.var_afficher_mdp.get():
            self.entry_mot_de_passe.config(show="")  # Afficher le mot de passe
        else:
            self.entry_mot_de_passe.config(show="*")  # Masquer le mot de passe

    def verifier_identifiants(self):
        identifiant = self.entry_identifiant.get()
        mot_de_passe = self.entry_mot_de_passe.get()

        # Rechercher l'utilisateur dans la base de données
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, mot_de_passe, role FROM utilisateurs WHERE identifiant=?",
            (identifiant,),
        )
        result = cursor.fetchone()

        if result is None:
            messagebox.showerror("Erreur", "Identifiant inconnu.")
        else:
            utilisateur_id = result[0]
            stored_mdp = result[1]
            role = result[2]

            # Vérifier si le mot de passe correspond
            if mot_de_passe == stored_mdp:
                if role == "admin":
                    messagebox.showinfo(
                        "Succès", "Connexion réussie en tant qu'admin !"
                    )
                    self.authenticated = True
                    self.root.quit()
                    # self.show_dashboard()  # Afficher les boutons
                else:
                    messagebox.showerror(
                        "Accès refusé", "Vous n'êtes pas habilité pour ce poste."
                    )
            else:
                # Incrémenter le compteur d'essais
                self.compteur_essais += 1
                if self.compteur_essais >= 4:
                    messagebox.showerror(
                        "Erreur", "Vous avez dépassé le nombre d'essais autorisés."
                    )
                    self.root.destroy()
                else:
                    messagebox.showerror(
                        "Erreur",
                        f"Mot de passe incorrect. Tentative n°{self.compteur_essais}",
                    )

    def on_enter(self, e):
        self.root.style.configure("TButton", background="#005a9e")

    def on_leave(self, e):
        self.root.style.configure("TButton", background="#0078d4")

    def show_dashboard(self):
        # Fermer la fenêtre de connexion
        self.root.withdraw()

        # Créer une nouvelle fenêtre pour le tableau de bord
        dashboard = tk.Toplevel(self.root)
        dashboard.title("Tableau de bord")
        dashboard.geometry("800x200")  # Agrandir la fenêtre si nécessaire
        dashboard.config(bg="#2e2e2e")

        # Placer les boutons sur une même ligne avec grid
        bouton_routine = ttk.Button(
            dashboard,
            text="Routine de reconnaissance",
            command=self.routine_reconnaissance,
            style="TButton",
        )
        bouton_routine.grid(row=0, column=0, padx=10, pady=20, sticky="ew", ipadx=10)

        bouton_autopilotage = ttk.Button(
            dashboard,
            text="Autopilotage zone ciblée",
            command=self.autopilotage_zone,
            style="TButton",
        )
        bouton_autopilotage.grid(
            row=0, column=1, padx=10, pady=20, sticky="ew", ipadx=10
        )

        bouton_mode_manuel = ttk.Button(
            dashboard, text="Mode manuel", command=self.mode_manuel, style="TButton"
        )
        bouton_mode_manuel.grid(
            row=0, column=2, padx=10, pady=20, sticky="ew", ipadx=10
        )

        bouton_parametres = ttk.Button(
            dashboard,
            text="Paramètres de mission",
            command=self.parametres_mission,
            style="TButton",
        )
        bouton_parametres.grid(row=0, column=3, padx=10, pady=20, sticky="ew", ipadx=10)

        # Personnalisation des boutons
        dashboard.style = ttk.Style()
        dashboard.style.configure(
            "TButton",
            background="#0078d4",
            foreground="white",
            font=("Helvetica", 12),
            padding=6,
        )

        # Rendre les colonnes égales en largeur
        dashboard.grid_columnconfigure(0, weight=1)
        dashboard.grid_columnconfigure(1, weight=1)
        dashboard.grid_columnconfigure(2, weight=1)
        dashboard.grid_columnconfigure(3, weight=1)

    def routine_reconnaissance(self):
        messagebox.showinfo("Routine", "Routine de reconnaissance activée.")

    def autopilotage_zone(self):
        messagebox.showinfo("Autopilotage", "Autopilotage zone ciblée activé.")

    def mode_manuel(self):
        messagebox.showinfo("Mode manuel", "Mode manuel activé.")

    def parametres_mission(self):
        messagebox.showinfo("Paramètres de mission", "Paramètres de mission affichés.")

    def create_table(self):
        cursor = self.conn.cursor()

        # Créer la table utilisateurs si elle n'existe pas déjà
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            identifiant TEXT NOT NULL UNIQUE,
            mot_de_passe TEXT NOT NULL,
            role TEXT NOT NULL
        )
        """)

        # Ajouter un utilisateur 'admin' si ce n'est pas déjà fait
        cursor.execute(
            "INSERT OR IGNORE INTO utilisateurs (identifiant, mot_de_passe, role) VALUES ('admin', 'admin123', 'admin')"
        )


if __name__ == "__main__":
    fenetre = tk.Tk()
    app = Application(fenetre)
    fenetre.mainloop()

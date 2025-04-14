import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
from PIL import Image, ImageTk
import os
import sqlite3


class IdentificationWindow:
    def __init__(self, master, conn):
        self.master = master
        self.master.title("Identification")
        self.master.configure(bg="#2e2e2e")
        self.master.attributes("-fullscreen", True)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_rowconfigure(3, weight=1)
        self.master.grid_rowconfigure(4, weight=1)
        self.master.grid_rowconfigure(5, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.title_label = ttk.Label(
            master,
            text="Faucon Bleu",
            font=("Helvetica", 24, "bold"),
            background="#2e2e2e",
            foreground="white",
        )
        self.title_label.grid(row=0, column=0, sticky="n", pady=20)

        label_font = ("Helvetica", 16)

        self.label = ttk.Label(
            master,
            text="Username:",
            background="#2e2e2e",
            foreground="white",
            font=label_font,
        )
        self.label.grid(row=1, column=0, sticky="nsew", padx=10, pady=2)

        self.username = ttk.Entry(master, font=label_font)
        self.username.grid(row=2, column=0, sticky="ew", padx=10, pady=2)

        self.password_label = ttk.Label(
            master,
            text="Password:",
            background="#2e2e2e",
            foreground="white",
            font=label_font,
        )
        self.password_label.grid(row=3, column=0, sticky="nsew", padx=10, pady=2)

        self.password = ttk.Entry(master, show="*", font=label_font)
        self.password.grid(row=4, column=0, sticky="ew", padx=10, pady=2)

        self.login_button = tk.Button(
            master,
            text="Connect",
            bg="#0078d7",
            fg="white",
            font=("Helvetica", 12),
            command=self.login,
        )
        self.login_button.grid(row=5, column=0, sticky="nsew", padx=20, pady=20)

        self.conn = conn
        self.compteur_essais = 0

    def login(self):
        try:
            self.verifier_identifiants()
        except IdentifiantInconnuError:
            messagebox.showerror("Erreur", "Identifiant inconnu.")
        except MotDePasseIncorrectError as e:
            messagebox.showerror("Erreur", str(e))
        except TentativesDepasseesError:
            messagebox.showerror(
                "Erreur", "Vous avez dépassé le nombre d'essais autorisés."
            )
            self.master.destroy()
        except AccesRefuseError:
            messagebox.showerror(
                "Accès refusé", "Vous n'êtes pas habilité pour ce poste."
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur inattendue s'est produite: {e}")

    def verifier_identifiants(self):
        identifiant = self.username.get()
        mot_de_passe = self.password.get()

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, mot_de_passe, role FROM utilisateurs WHERE identifiant=?",
            (identifiant,),
        )
        result = cursor.fetchone()

        if result is None:
            raise IdentifiantInconnuError()

        utilisateur_id, stored_mdp, role = result

        if mot_de_passe != stored_mdp:
            self.compteur_essais += 1
            if self.compteur_essais >= 4:
                raise TentativesDepasseesError()
            else:
                raise MotDePasseIncorrectError(
                    f"Mot de passe incorrect. Tentative n°{self.compteur_essais}"
                )

        if role != "admin":
            raise AccesRefuseError()

        messagebox.showinfo("Succès", "Connexion réussie en tant qu'admin !")
        self.master.destroy()
        self.open_main_menu()

    def open_main_menu(self):
        main_window = tk.Tk()
        MainMenu(main_window)
        main_window.mainloop()


# Exceptions personnalisées
class IdentifiantInconnuError(Exception):
    pass


class MotDePasseIncorrectError(Exception):
    def __init__(self, message):
        super().__init__(message)


class TentativesDepasseesError(Exception):
    pass


class AccesRefuseError(Exception):
    pass


class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Menu")
        self.master.configure(bg="#2e2e2e")

        self.master.attributes("-fullscreen", True)

        for i in range(7):
            self.master.grid_rowconfigure(i, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        self.title_label = ttk.Label(
            master,
            text="Faucon Bleu",
            font=("Helvetica", 24, "bold"),
            background="#2e2e2e",
            foreground="white",
        )
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="n", pady=20)

        self.mission_button1 = tk.Button(
            master,
            text="Manual",
            bg="#0078d7",
            fg="white",
            font=("Helvetica", 14),
            command=self.select_mission1,
        )
        self.mission_button1.grid(
            row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=20
        )

        self.mission_button2 = tk.Button(
            master,
            text="Autonomous",
            bg="#0078d7",
            fg="white",
            font=("Helvetica", 14),
            command=self.select_mission2,
        )
        self.mission_button2.grid(
            row=2, column=0, columnspan=2, sticky="nsew", padx=20, pady=20
        )

        self.settings_button = tk.Button(
            master,
            text="Parameters",
            bg="#0078d7",
            fg="white",
            font=("Helvetica", 14),
            command=self.open_settings,
        )
        self.settings_button.grid(
            row=4, column=0, columnspan=2, sticky="nsew", padx=20, pady=20
        )

        self.add_logos()

    def add_logos(self):
        # Charger et redimensionner les images
        logo_paths = ["assets/logo-seatech.png", "assets/Logo-DGA.png"]
        logos = []

        # Redimensionner les images pour qu'elles s'affichent correctement
        sizes = [(300, 85), (100, 60)]  # Ajustez les tailles selon vos besoins
        for path, size in zip(logo_paths, sizes):
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            logos.append(ImageTk.PhotoImage(img))

        # Placer les images dans la grille
        logo_frame = tk.Frame(self.master, bg="#2e2e2e")
        logo_frame.grid(row=5, column=0, sticky="sw", padx=10, pady=10)

        for logo in logos:
            label = tk.Label(logo_frame, image=logo, bg="#2e2e2e")
            label.image = logo  # Conserver une référence
            label.pack(side="left", padx=5)

    def select_mission1(self):
        self.master.destroy()
        self.start_mission1_program()

    def start_mission1_program(self):
        # Get the directory of the current script (IHM.py)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(base_dir, "main.py")

        if not os.path.isfile(script_path):
            messagebox.showerror("Erreur", f"Le fichier {script_path} est introuvable.")
            return

        # Set the working directory to the directory of main.py
        subprocess.Popen(
            [
                os.path.join(base_dir, "..", ".venv", "Scripts", "python.exe"),
                script_path,
            ],
            cwd=base_dir,  # Ensure the working directory is correct
        )

    def select_mission2(self):
        self.master.destroy()
        self.start_pygame_program()

    def open_settings(self):
        self.master.destroy()
        self.open_parameter_menu()

    def open_parameter_menu(self):
        parameter_window = tk.Tk()
        ParameterMenu(parameter_window)
        parameter_window.mainloop()

    def start_pygame_program(self):
        script_path = os.path.join(
            os.getcwd(), "SimulateurDroneFauconBleu", "carte_2D.py"
        )

        if not os.path.isfile(script_path):
            messagebox.showerror("Erreur", f"Le fichier {script_path} est introuvable.")
            return

        script_dir = os.path.dirname(script_path)

        subprocess.Popen(
            [os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe"), script_path],
            cwd=script_dir,  # Set the working directory to the directory of Carte_2D.py
        )


class ParameterMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Parameters")
        self.master.configure(bg="#2e2e2e")

        self.master.attributes("-fullscreen", True)

        self.settings_label = ttk.Label(
            master,
            text="Parameters",
            font=("Helvetica", 16),
            background="#2e2e2e",
            foreground="white",
        )
        self.settings_label.pack(pady=20)

        self.enemy_presence = tk.BooleanVar(value=False)
        self.selected_weather = tk.StringVar(value="Sunny")
        self.selected_time = tk.StringVar(value="12")
        self.selected_mission_type = tk.StringVar(value="Offshore")

        self.enemy_check = ttk.Checkbutton(
            master, text="Enemy ", variable=self.enemy_presence
        )
        self.enemy_check.pack(pady=10, anchor="w", padx=20)

        self.weather_label = ttk.Label(
            master, text="Weather:", background="#2e2e2e", foreground="white"
        )
        self.weather_label.pack(pady=10, anchor="w", padx=20)
        self.weather_combobox = ttk.Combobox(master, textvariable=self.selected_weather)
        self.weather_combobox["values"] = ("Sunny", "Rainy", "Windy")
        self.weather_combobox.pack(pady=10, anchor="w", padx=20)
        self.weather_combobox.current(0)

        self.time_label = ttk.Label(
            master, text="Hour:", background="#2e2e2e", foreground="white"
        )
        self.time_label.pack(pady=10, anchor="w", padx=20)
        self.time_spinbox = ttk.Spinbox(
            master, from_=0, to=23, textvariable=self.selected_time, wrap=True
        )
        self.time_spinbox.pack(pady=10, anchor="w", padx=20)

        self.mission_type_label = ttk.Label(
            master, text="Type of mission:", background="#2e2e2e", foreground="white"
        )
        self.mission_type_label.pack(pady=10, anchor="w", padx=20)
        self.mission_type_combobox = ttk.Combobox(
            master, textvariable=self.selected_mission_type
        )
        self.mission_type_combobox["values"] = ("Offshore", "Onshore")
        self.mission_type_combobox.pack(pady=10, anchor="w", padx=20)
        self.mission_type_combobox.current(0)

        self.back_button = tk.Button(
            master,
            text="Back",
            bg="#0078d7",
            fg="white",
            font=("Helvetica", 14),
            command=self.go_back,
        )
        self.back_button.pack(pady=20, fill=tk.X, padx=20)

    def go_back(self):
        enemy_presence = self.enemy_presence.get()
        selected_weather = self.selected_weather.get()
        selected_time = self.selected_time.get()
        selected_mission_type = self.selected_mission_type.get()

        print(f"Ennemis présents: {enemy_presence}")
        print(f"Météo sélectionnée: {selected_weather}")
        print(f"Heure sélectionnée: {selected_time}")
        print(f"Type de mission sélectionné: {selected_mission_type}")

        self.master.destroy()
        main_window = tk.Tk()
        MainMenu(main_window)
        main_window.mainloop()


if __name__ == "__main__":
    conn = sqlite3.connect("utilisateurs.db")
    root = tk.Tk()
    app = IdentificationWindow(root, conn)
    root.mainloop()
    conn.close()

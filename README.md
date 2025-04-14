# Installation du projet

## Prérequis

Avant de démarrer le projet, il est recommandé de créer un environnement virtuel pour éviter les conflits de dépendances avec d'autres projets. Voici les étapes à suivre pour installer les dépendances nécessaires à l'exécution du projet.

## Étapes d'installation

1. **Créer un environnement virtuel**

   Ouvrez votre terminal et naviguez jusqu'au répertoire du projet. Ensuite, exécutez la commande suivante pour créer un environnement virtuel :

   - Sur **Linux/macOS** :
     ```bash
     python3 -m venv venv
     ```
   - Sur **Windows** :
     ```bash
     python -m venv venv
     ```

2. **Activer l'environnement virtuel**

   - Sur **Linux/macOS** :
     ```bash
     source venv/bin/activate
     ```
   - Sur **Windows** :
     ```bash
     .\venv\Scripts\activate
     ```

3. **Installer les dépendances**

   Une fois l'environnement virtuel activé, installez les packages nécessaires en utilisant le fichier `requirements.txt` :

   ```bash
   pip install -r requirements.txt


# Le Faucon Bleu
Simulateur d'un drone visant à augmenter la vision hors de l'eau d'un sous-marin en Python et OpenGL

Contrôles: ZQSD shift espace + souris

![minecraft](/screenshot/0.jpg)

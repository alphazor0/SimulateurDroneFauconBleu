import pygame
import sys
import subprocess

# Initialisation de Pygame
pygame.init()

# Constantes
MAP_WIDTH, MAP_HEIGHT = 400, 300  # Taille de la carte 2D

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialiser la sous-fenêtre pour la carte 2D
map_screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
pygame.display.set_caption("2D Map")

# Charger l'image de fond pour la carte 2D
map_background_image = pygame.image.load('assets/map.png')
map_background_image = pygame.transform.scale(map_background_image, (MAP_WIDTH, MAP_HEIGHT))

# Fonction pour dessiner la carte 2D
def draw_2d_map(screen, drone_position_2d):
    # Dessiner l'image de fond de la carte
    screen.blit(map_background_image, (0, 0))
    # Dessiner le drone sur la carte 2D
    pygame.draw.circle(screen, (0, 0, 255), drone_position_2d, 5)

# Fonction pour convertir les coordonnées 2D en 3D
def convert_2d_to_3d(position_2d):
    # Exemple de conversion simple (à adapter selon votre logique)
    x_3d = position_2d[0] * 2
    y_3d = position_2d[1] * 2
    return x_3d, y_3d

# Position initiale du drone en 2D
drone_position_2d = [100, 150]

# Lancer le script 3D
subprocess.Popen(["python", "SimulateurDroneFauconBleu-main/main.pymain.py"])

# Boucle principale pour la carte 2D
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Convertir les coordonnées 2D en 3D
    drone_position_3d = convert_2d_to_3d(drone_position_2d)

    # Mettre à jour la position de la caméra dans le script 3D
    # Vous devrez implémenter une méthode pour envoyer drone_position_3d à votre script 3D

    # Dessiner la carte 2D
    draw_2d_map(map_screen, drone_position_2d)
    pygame.display.flip()
    clock.tick(30)

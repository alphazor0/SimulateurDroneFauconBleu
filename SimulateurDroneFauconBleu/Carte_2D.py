import pygame
import sys
import random
import heapq

# Initialisation de pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Charger l'image de fond
background_image = pygame.image.load(r'../assets/map.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

class Drone_2D:
    def __init__(self, start_position, path):
        self.position = list(start_position)  # Utiliser une liste pour la position
        self.path = path
        self.index = 0
        self.speed = 20
        self.battery_level = 100  # Initial battery level

    def move(self):
        if self.index < len(self.path):
            target = self.path[self.index]
            dx = target[0] - self.position[0]
            dy = target[1] - self.position[1]
            distance = (dx**2 + dy**2)**0.5

            if distance < self.speed:
                self.position = list(target)  # Mettre à jour la position avec une liste
                self.index += 1
            else:
                self.position[0] += dx / distance * self.speed
                self.position[1] += dy / distance * self.speed

            # Decrease battery level based on movement
            self.battery_level -= 0.1  # Adjust the decrement value as needed

class Objet_2D:
    def __init__(self, position, obj_type):
        self.position = position
        self.obj_type = obj_type

    def draw(self, screen):
        if self.obj_type == "submarine":
            color = GREEN
        elif self.obj_type == "building":
            color = YELLOW
        elif self.obj_type == "boat":
            color = RED
        pygame.draw.circle(screen, color, self.position, 10)

class Map_2D:
    def __init__(self, size, drone, objects):
        self.size = size
        self.drone = drone
        self.objects = objects
        # Initialiser la fenêtre en plein écran
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        pygame.display.set_caption("Drone Map")
        self.fog_of_war = pygame.Surface(size, pygame.SRCALPHA)
        self.fog_of_war.fill((0, 0, 0, 255))
        self.explored = pygame.Surface(size, pygame.SRCALPHA)
        self.explored.fill((0, 0, 0, 255))

    def update_fog_of_war(self, radius=50):
        # Mettre à jour la zone explorée
        pygame.draw.circle(self.explored, (0, 0, 0, 0), self.drone.position, radius)
        # Combiner le brouillard de guerre avec les zones explorées
        self.fog_of_war = self.explored.copy()

    def draw_battery_bar(self):
        # Dessiner la barre de batterie
        bar_width = 100
        bar_height = 20
        bar_x = 10
        bar_y = 10
        border_color = BLACK
        fill_color = GREEN
        border_width = 2

        # Dessiner le contour de la barre
        pygame.draw.rect(self.screen, border_color, (bar_x, bar_y, bar_width, bar_height), border_width)

        # Dessiner la partie remplie de la barre
        fill_width = int((self.drone.battery_level / 100) * (bar_width - 2 * border_width))
        pygame.draw.rect(self.screen, fill_color, (bar_x + border_width, bar_y + border_width, fill_width, bar_height - 2 * border_width))

    def draw(self):
        self.screen.blit(background_image, (0, 0))  # Dessiner l'image de fond
        pygame.draw.circle(self.screen, BLUE, self.drone.position, 5)

        # Dessiner les objets
        for obj in self.objects:
            obj.draw(self.screen)

        self.screen.blit(self.fog_of_war, (0, 0))

        # Dessiner la barre de batterie
        self.draw_battery_bar()

        pygame.display.flip()

def select_waypoints():
    waypoints = []
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche pour ajouter un point
                    waypoints.append(event.pos)
                elif event.button == 3:  # Clic droit pour terminer la sélection
                    selecting = False

        screen.blit(background_image, (0, 0))  # Dessiner l'image de fond
        for point in waypoints:
            pygame.draw.circle(screen, RED, point, 5)
        pygame.display.flip()
    return waypoints

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(graph, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not len(frontier) == 0:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    return came_from, cost_so_far

class SimpleGraph:
    def __init__(self):
        self.edges = {}

    def neighbors(self, node):
        return self.edges[node]

    def cost(self, from_node, to_node):
        return 1  # Coût uniforme pour cet exemple

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

# Fonction pour calculer la distance entre deux points
def distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

# Fonction de fitness : calcule la longueur totale du chemin
def fitness(path, waypoints):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distance(waypoints[path[i]], waypoints[path[i + 1]])
    return total_distance

# Algorithme génétique pour optimiser l'ordre des points de contrôle
def genetic_algorithm(waypoints, population_size=50, generations=100, mutation_rate=0.01):
    # Initialiser une population de solutions aléatoires
    population = [random.sample(range(len(waypoints)), len(waypoints)) for _ in range(population_size)]

    for generation in range(generations):
        # Évaluer chaque solution
        fitness_scores = [(fitness(individual, waypoints), individual) for individual in population]
        # Trier les solutions par score de fitness
        fitness_scores.sort(key=lambda x: x[0])

        # Sélectionner les meilleures solutions
        best_solutions = [individual for _, individual in fitness_scores[:population_size // 2]]

        # Créer une nouvelle génération
        new_generation = []
        while len(new_generation) < population_size:
            # Sélectionner deux parents
            parent1, parent2 = random.choices(best_solutions, k=2)
            # Croisement : combiner les deux parents
            crossover_point = random.randint(0, len(parent1) - 1)
            child = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]

            # Mutation : modifier légèrement le enfant
            if random.random() < mutation_rate:
                i, j = random.sample(range(len(child)), 2)
                child[i], child[j] = child[j], child[i]

            new_generation.append(child)

        population = new_generation

    # Retourner la meilleure solution trouvée
    best_solution = min(population, key=lambda x: fitness(x, waypoints))
    return best_solution

# Exemple d'utilisation
start_position = (0, HEIGHT)  # Position en bas à gauche
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Drone Map")

# Sélection des points de contrôle
waypoints = select_waypoints()

# Optimiser l'ordre des points de contrôle avec l'algorithme génétique
optimized_order = genetic_algorithm(waypoints)

# Créer un graphe à partir des points de contrôle
graph = SimpleGraph()
for waypoint in waypoints:
    graph.edges[waypoint] = [w for w in waypoints if w != waypoint]

# Trouver le chemin optimisé avec A* en utilisant l'ordre optimisé
full_path = []
for i in range(len(optimized_order) - 1):
    start = waypoints[optimized_order[i]]
    goal = waypoints[optimized_order[i + 1]]
    came_from, cost_so_far = a_star_search(graph, start, goal)
    path_segment = reconstruct_path(came_from, start, goal)
    full_path.extend(path_segment)

# Création des objets
submarine = Objet_2D(start_position, "submarine")
buildings = [Objet_2D((random.randint(0, WIDTH), random.randint(0, HEIGHT)), "building") for _ in range(5)]
boats = [Objet_2D((random.randint(0, WIDTH), random.randint(0, HEIGHT)), "boat") for _ in range(3)]
objects = [submarine] + buildings + boats

drone = Drone_2D(start_position, full_path)
Map = Map_2D((WIDTH, HEIGHT), drone, objects)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if drone.battery_level > 0:
        drone.move()
    else:
        # Afficher un message lorsque la batterie est épuisée
        font = pygame.font.Font(None, 36)
        battery_text = font.render("Battery Depleted! Drone Stopped.", True, RED)
        Map.screen.blit(battery_text, (WIDTH // 2 - battery_text.get_width() // 2, HEIGHT // 2 - battery_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # Attendre 2 secondes avant de quitter
        pygame.quit()
        sys.exit()

    Map.update_fog_of_war()
    Map.draw()
    clock.tick(30)

from .noise import noise2, noise3
from random import random
from .settings import *


@njit
def get_height(x, z):
    # island mask
    island = 1 / (pow(0.0025 * math.hypot(x - CENTER_XZ, z - CENTER_XZ), 20) + 0.0001)
    island = min(island, 1)

    # amplitude
    a1 = CENTER_Y
    a2, a4, a8 = a1 * 0.5, a1 * 0.25, a1 * 0.125

    # frequency
    f1 = 0.005
    f2, f4, f8 = f1 * 2, f1 * 4, f1 * 8

    if noise2(0.1 * x, 0.1 * z) < 0:
        a1 /= 1.07

    height = 0
    height += noise2(x * f1, z * f1) * a1 + a1
    height += noise2(x * f2, z * f2) * a2 - a2
    height += noise2(x * f4, z * f4) * a4 + a4
    height += noise2(x * f8, z * f8) * a8 - a8

    height = max(height, noise2(x * f8, z * f8) + 2)
    height *= island

    return int(height)


@njit
def get_index(x, y, z):
    return x + CHUNK_SIZE * z + CHUNK_AREA * y


@njit
def set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height):
    voxel_id = 0

    if wy < world_height - 1:
        if (
            noise3(wx * 0.09, wy * 0.09, wz * 0.09) > 0
            and noise2(wx * 0.1, wz * 0.1) * 3 + 3 < wy < world_height - 10
        ):
            voxel_id = 0  # L'espace vide (caverne)
        else:
            voxel_id = STONE  # Le matériau par défaut pour le terrain (pierre)
    else:
        rng = int(7 * random())
        ry = wy - rng
        if SNOW_LVL <= ry < world_height:
            voxel_id = SNOW
        elif STONE_LVL <= ry < SNOW_LVL:
            voxel_id = STONE
        elif DIRT_LVL <= ry < STONE_LVL:
            voxel_id = DIRT
        elif GRASS_LVL <= ry < DIRT_LVL:
            voxel_id = GRASS
        else:
            voxel_id = SAND

    # Assigner l'ID du voxel
    voxels[get_index(x, y, z)] = voxel_id

    # Placer un arbre si les conditions sont remplies
    if wy < DIRT_LVL:
        place_tree(voxels, x, y, z, voxel_id)

    # Condition pour le placement des bâtiments : zones aléatoires espacées et hors de l'eau
    if wy <= DIRT_LVL and random() < 0.05:  # Placer un bâtiment avec 5% de probabilité
        # Vérifier que le terrain n'est pas sous l'eau
        if (
            world_height > WATER_LINE
        ):  # Si la hauteur du terrain est au-dessus du niveau de l'eau
            # Vérifier l'espacement des bâtiments
            if x % 20 == 0 and z % 20 == 0:  # Espacement tous les 20 blocs
                place_building(voxels, x, y, z, STONE)  # Placer un bâtiment en pierre
    return None


@njit
def place_tree(voxels, x, y, z, voxel_id):
    rnd = random()
    if voxel_id != GRASS or rnd > TREE_PROBABILITY:
        return None
    if y + TREE_HEIGHT >= CHUNK_SIZE:
        return None
    if x - TREE_H_WIDTH < 0 or x + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    if z - TREE_H_WIDTH < 0 or z + TREE_H_WIDTH >= CHUNK_SIZE:
        return None

    # dirt under the tree
    voxels[get_index(x, y, z)] = DIRT

    # leaves
    m = 0
    for n, iy in enumerate(range(TREE_H_HEIGHT, TREE_HEIGHT - 1)):
        k = iy % 2
        rng = int(random() * 2)
        for ix in range(-TREE_H_WIDTH + m, TREE_H_WIDTH - m * rng):
            for iz in range(-TREE_H_WIDTH + m * rng, TREE_H_WIDTH - m):
                if (ix + iz) % 4:
                    voxels[get_index(x + ix + k, y + iy, z + iz + k)] = LEAVES
        m += 1 if n > 0 else 3 if n > 1 else 0

    # tree trunk
    for iy in range(1, TREE_HEIGHT - 2):
        voxels[get_index(x, y + iy, z)] = WOOD

    # top
    voxels[get_index(x, y + TREE_HEIGHT - 2, z)] = LEAVES


@njit
def place_building(voxels, x, y, z, building_id):
    """
    Place un bâtiment dans le monde aux coordonnées (x, y, z).
    :param voxels: La liste des voxels du monde.
    :param x, y, z: Les coordonnées de la base du bâtiment.
    :param building_id: L'ID du matériau utilisé pour construire le bâtiment (p. ex. pierre, béton).
    """
    # Dimensions du bâtiment
    building_width = 9  # Largeur du bâtiment
    building_height = 7  # Hauteur du bâtiment
    building_depth = 9  # Profondeur du bâtiment

    # Vérifier si le bâtiment tient dans les limites du chunk
    if (
        x + building_width > CHUNK_SIZE
        or y + building_height > CHUNK_SIZE
        or z + building_depth > CHUNK_SIZE
    ):
        return None  # Ne pas placer le bâtiment s'il dépasse les bords du chunk

    # Construction des murs (utilisation du matériau 'building_id' pour les murs)
    for ix in range(building_width):
        for iy in range(building_height):
            for iz in range(building_depth):
                # Construire les murs (sur les bords du bâtiment)
                if (
                    ix == 0
                    or ix == building_width - 1
                    or iz == 0
                    or iz == building_depth - 1
                ):
                    voxels[get_index(x + ix, y + iy, z + iz)] = (
                        building_id  # Murs en pierre (STONE)
                    )

    # Création du toit (utilisation de 'building_id' pour le toit)
    for ix in range(building_width):
        for iz in range(building_depth):
            voxels[get_index(x + ix, y + building_height, z + iz)] = (
                building_id  # Toit en pierre
            )

    # **Ne pas ajouter de blocs de terre au-dessus du bâtiment**
    # Placer le sol sous le bâtiment, mais **ne pas** modifier les positions au-dessus du bâtiment
    for ix in range(building_width):
        for iz in range(building_depth):
            # Placer du sol sous le bâtiment seulement, en évitant de toucher au-dessus
            if (
                y - 1 >= 0
            ):  # Assurez-vous que la position du sol est dans les limites du chunk
                voxels[get_index(x + ix, y - 1, z + iz)] = DIRT  # Sol sous le bâtiment

    # Ajouter une porte (utiliser un matériau comme 'WOOD' pour la porte)
    door_width = 1
    door_height = 2
    for ix in range(door_width):
        for iy in range(door_height):
            voxels[
                get_index(x + building_width // 2 - door_width // 2 + ix, y + iy, z)
            ] = WOOD  # Porte en bois

    return True

import unittest
import numpy as np
import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from SimulateurDroneFauconBleu.terrain_gen import get_height, get_index, set_voxel_id
from SimulateurDroneFauconBleu.settings import (
    CHUNK_SIZE,
    CHUNK_AREA,
    CENTER_XZ,
    CENTER_Y,
)


class TestTerrainGen(unittest.TestCase):
    def test_get_height(self):
        x, z = 0, 0
        height = get_height(x, z)
        self.assertIsInstance(height, int, "La hauteur doit être un entier.")
        self.assertGreaterEqual(height, 0, "La hauteur doit être positive ou nulle.")

    def test_get_index(self):
        x, y, z = 1, 2, 3
        index = get_index(x, y, z)
        expected_index = x + CHUNK_SIZE * z + CHUNK_AREA * y
        self.assertEqual(index, expected_index, "L'index calculé est incorrect.")

    def test_set_voxel_id(self):
        voxels = np.zeros(CHUNK_SIZE * CHUNK_SIZE * CHUNK_SIZE, dtype=np.int32)
        x, y, z = 5, 5, 5
        wx, wy, wz = 5, 5, 5
        world_height = 10

        set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height)
        voxel_id = voxels[get_index(x, y, z)]
        self.assertIn(voxel_id, [0, 1, 2, 3, 4, 5], "L'ID du voxel est incorrect.")


if __name__ == "__main__":
    unittest.main()

import unittest
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "SimulateurDroneFauconBleu")
    )
)

from Carte_2D import *  # ou importe ce dont tu as besoin


class TestDrone2D(unittest.TestCase):
    def test_initial_position(self):
        drone = Drone_2D((0, 0), [])
        self.assertEqual(drone.position, [0, 0])


if __name__ == "__main__":
    unittest.main()

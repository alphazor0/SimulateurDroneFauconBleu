import unittest
from SimulateurDroneFauconBleu.Drone_2D import Drone_2D


class TestDrone2D(unittest.TestCase):
    def test_initial_position(self):
        drone = Drone_2D((0, 0), [])
        self.assertEqual(drone.position, [0, 0])


if __name__ == "__main__":
    unittest.main()

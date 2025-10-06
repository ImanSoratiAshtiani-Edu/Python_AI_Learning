import unittest
from exercises.core_ex02 import core_ex02

class TestCoreEx02(unittest.TestCase):
    def test_mean_of_column_B(self):
        result = core_ex02()
        expected = (4 + 5 + 6) / 3  # yani 5.0
        self.assertEqual(result, expected)
        self.assertIsInstance(result, float)

if __name__ == "__main__":
    unittest.main()
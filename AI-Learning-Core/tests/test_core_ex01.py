
import unittest
from exercises.core_ex01 import core_ex01

class TestCoreEx01(unittest.TestCase):
    def test_core_ex01_output(self):
        lista, summ = core_ex01()
        self.assertEqual(len(lista), 10)
        self.assertTrue(all(100 <= x < 200 for x in lista))
        self.assertEqual(summ, sum(lista))

if __name__ == "__main__":
    unittest.main()

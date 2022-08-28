from importlib.util import set_loader
import cfrac   
import unittest   

class Test_TestIncrementDecrement(unittest.TestCase):
    def test_is_square(self):
        self.assertEqual(cfrac.is_square(9), True)
        self.assertEqual(cfrac.is_square(13), False)
        self.assertEqual(cfrac.is_square(19), False)
        self.assertEqual(cfrac.is_square(36), True)
    
    def test_factor(self):
        self.assertEqual(cfrac.factor(128), {2: 7})
        self.assertEqual(cfrac.factor(188), {2: 2, 47: 1})
        self.assertEqual(cfrac.factor(432), {2: 4, 3: 3})
        self.assertEqual(cfrac.factor(432124124), {2: 2, 108031031: 1})
        self.assertEqual(cfrac.factor(31911990362625565390), {2: 1, 5: 1, 11: 1, 29: 1, 97: 1, 499: 1, 1297: 1, 11483: 1, 13877: 1})

    def test_issquarefree(self):
        self.assertEqual(cfrac.is_square_free(9), False)
        self.assertEqual(cfrac.is_square_free(123), True)
        self.assertEqual(cfrac.is_square_free(244), False)
        self.assertEqual(cfrac.is_square_free(30), True)

    def test_next_multiplier(self):
        self.assertEqual(cfrac.next_multiplier(1081, 3), 5)
        self.assertEqual(cfrac.next_multiplier(21299881, 3), 5)
        self.assertEqual(cfrac.next_multiplier(21299881, 1), 3)

    def test_is_prime(self):
        self.assertEqual(cfrac.is_prime(21299881), False)


if __name__ == '__main__':
    unittest.main()

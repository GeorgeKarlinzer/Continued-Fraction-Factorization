from importlib.util import set_loader
import temp    # The code to test
import unittest   # The test framework

class Test_TestIncrementDecrement(unittest.TestCase):
    def test_is_square(self):
        self.assertEqual(temp.issquare(9), True)
        self.assertEqual(temp.issquare(13), False)
        self.assertEqual(temp.issquare(19), False)
        self.assertEqual(temp.issquare(36), True)
    
    def test_factor(self):
        self.assertEqual(temp.factor(128), {2: 7})
        self.assertEqual(temp.factor(188), {2: 2, 47: 1})
        self.assertEqual(temp.factor(432), {2: 4, 3: 3})
        self.assertEqual(temp.factor(432124124), {2: 2, 108031031: 1})
        self.assertEqual(temp.factor(31911990362625565390), {2: 1, 5: 1, 11: 1, 29: 1, 499: 1, 1297: 1, 11483: 1, 13877: 1})

    def test_issquarefree(self):
        self.assertEqual(temp.issquarefree(9), False)
        self.assertEqual(temp.issquarefree(123), True)
        self.assertEqual(temp.issquarefree(244), False)
        self.assertEqual(temp.issquarefree(30), True)

    def test_next_multiplier(self):
        self.assertEqual(temp.next_multiplier(1081, 3), 5)
        self.assertEqual(temp.next_multiplier(21299881, 3), 5)
        self.assertEqual(temp.next_multiplier(21299881, 1), 3)

    def test_is_prime(self):
        self.assertEqual(temp.is_prime(21299881), False)


if __name__ == '__main__':
    unittest.main()
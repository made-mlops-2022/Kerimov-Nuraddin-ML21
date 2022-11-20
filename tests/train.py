import unittest
import os
from ml_example.train import train


class TestTrain(unittest.TestCase):
    def test_train(self):
        train()
        self.assertTrue(os.path.exists('./models/model.pkl'))


if __name__ == "__main__":
    unittest.main()

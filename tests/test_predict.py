import unittest
import os
from ml_example.predict import predict
from ml_example.data.make_dataset import generete_fake_data

class TestTrain(unittest.TestCase):
    def test_train(self):
        generete_fake_data('./tests/data/raw/fake_data.csv',1000)
        predict('./tests/data/raw/fake_data.csv',
                './models/model.pkl', './tests/res.csv')
        self.assertTrue(os.path.exists('./tests/res.csv'))


if __name__ == "__main__":
    unittest.main()

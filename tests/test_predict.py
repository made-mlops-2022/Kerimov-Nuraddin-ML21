import unittest
import os
from ml_example.predict import predict


class TestTrain(unittest.TestCase):
    def test_train(self):
        predict('./tests/data/raw/fake_data.csv','./models/model.pkl','./tests/res.csv')
        self.assertTrue(os.path.exists('./tests/res.csv'))

if __name__ == "__main__":
    unittest.main()
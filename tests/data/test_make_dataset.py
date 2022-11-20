import pandas as pd
import numpy as np
import os
import unittest
from ml_example.enities.download_params import DownloadParams
from ml_example.enities.split_params import SplittingParams
from ml_example.data.make_dataset import download_data, read_data,split_train_val_data,save_predicted_results,generete_fake_data

class TestData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cfg = DownloadParams()
        cfg.path='./tests/data/raw'
        cfg.csv='heart_cleveland_upload.csv'
        cfg.file_id='1q2ehxJdWkP-ak84wIc6GWRhCC3bgSTC4'
        cfg.zip_path='data.zip'
        cfg.url='https://docs.google.com/uc?export=download'
        download_data(cfg)  
    def test_download_data(self)->None:      
        self.assertTrue(os.path.exists('./tests/data/raw/heart_cleveland_upload.csv'))
        self.assertTrue(os.path.exists('./tests/data/raw/data.zip'))
        data = pd.read_csv('./tests/data/raw/heart_cleveland_upload.csv')
        self.assertTrue(len(data) != 0)


    def test_read_data(self):
        data = read_data('./tests/data/raw/heart_cleveland_upload.csv')
        self.assertTrue(len(data)!=0)

    def test_split_train_val_data(self):
        data = read_data('./tests/data/raw/heart_cleveland_upload.csv')

        cfg = SplittingParams()
        cfg.val_size= 0.2
        cfg.random_state= 42

        tr,val = split_train_val_data(data,cfg)

        trc = tr.shape[0]
        valc = val.shape[0]
        self.assertTrue(valc/(trc+valc) < cfg.val_size+0.1)
        


    def test_save_predicted_results(self)->None:
        

        data = read_data('./tests/data/raw/heart_cleveland_upload.csv')

        labels = data['condition']
        data = data.drop(columns=['condition'])

        save_predicted_results(data,labels,'./tests/data/raw/predicted.csv')

        self.assertTrue(os.path.exists('./tests/data/raw/predicted.csv'))
        data_original = read_data('./tests/data/raw/heart_cleveland_upload.csv')

        data_saved = read_data('./tests/data/raw/predicted.csv')
        data_original = data_original.rename(columns = {'condition':'predicted'})
        print(data_original)
        print(data_saved)
        self.assertTrue(data_original.equals(data_saved))

    def test_generete_fake_data(self)->None:
        generete_fake_data('./tests./data/raw/fake_data.csv',1000)
        self.assertTrue(os.path.exists('./tests./data/raw/fake_data.csv'))

        data = read_data('./tests./data/raw/fake_data.csv')

        self.assertTrue(data.shape[0] ==1000)

        


if __name__ == "__main__":
    unittest.main()
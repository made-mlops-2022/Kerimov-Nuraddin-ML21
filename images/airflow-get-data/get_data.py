import os
import numpy as np
import pandas as pd
import argparse

def generete_fake_data(samples) -> pd.DataFrame:
    data = pd.DataFrame()
    data['age'] = np.random.normal(loc=58, scale=30, size=samples).astype(int)
    data['sex'] = np.random.randint(0, 1, size=samples)
    data['cp'] = np.random.randint(0, 3, size=samples)
    data['trestbps'] = np.random.normal(
        loc=130, scale=20, size=samples).astype(int)
    data['chol'] = np.random.normal(
        loc=250, scale=100, size=samples).astype(int)
    data['fbs'] = np.random.randint(0, 1, size=samples)
    data['restecg'] = np.random.randint(0, 2, size=samples)
    data['thalach'] = np.random.normal(
        loc=160, scale=60, size=samples).astype(int)
    data['exang'] = np.random.randint(0, 1, size=samples)
    data['oldpeak'] = np.abs(np.random.normal(
        loc=0, scale=3, size=samples).astype(int))
    data['slope'] = np.random.randint(0, 2, size=samples)
    data['ca'] = np.random.randint(0, 3, size=samples)
    data['thal'] = np.random.randint(0, 2, size=samples)
    data['condition'] = np.random.randint(0, 2, size=samples)
    return data

def get_data(dir,data_file,target_file) -> None:
    data = generete_fake_data(100)

    os.makedirs(dir, exist_ok=True)

    data.drop(columns=['condition']).to_csv(os.path.join(dir,data_file))
    data['condition'].to_csv(os.path.join(dir,target_file))
    


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('dir')
    p.add_argument('data_file')
    p.add_argument('target_file')
    args = p.parse_args()
    get_data(args.dir,args.data_file,args.target_file)
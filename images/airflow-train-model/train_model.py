import os
import numpy as np
import pandas as pd
import argparse
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
import pickle
def train(data_dir,data_file,model_dir,model_file):

    data = pd.read_csv(os.path.join(data_dir,data_file),dtype=int).astype(int)
    target = data['condition']
    features = data.drop(columns=['Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0','condition'])
    model = CatBoostClassifier(
            iterations=100,
            random_seed=42,
            learning_rate=0.005,
            custom_loss=['AUC','Accuracy','Recall'],
        ) 
    model.fit(
            features, target,
            cat_features=["sex" ,"cp" ,"fbs" ,"restecg" ,"exang" ,"slope" ,"thal"],
            verbose=False
        )
    os.makedirs(model_dir, exist_ok=True)
    with open(os.path.join(model_dir,model_file),'wb') as f:
        pickle.dump(model,f)
 


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('data_dir')
    p.add_argument('data_file')
    p.add_argument('model_dir')
    p.add_argument('model_file')
    args = p.parse_args()
    train(args.data_dir,args.data_file,args.model_dir,args.model_file)
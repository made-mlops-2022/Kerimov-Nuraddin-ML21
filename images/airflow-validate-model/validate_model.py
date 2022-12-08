import os
import pandas as pd
import argparse
from sklearn.metrics import precision_recall_fscore_support
import pickle


def validate(data_dir, data_file, model_dir, model_file):

    data = pd.read_csv(os.path.join(data_dir, data_file),dtype=int).astype(int)
    with open(os.path.join(model_dir, model_file), 'rb') as f:
        model = pickle.load(f)
    predicts = model.predict(data.drop(columns = ['condition','Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0']))
    target = data['condition']

    pr, rec, f1, _ = precision_recall_fscore_support(
        target, predicts, average='binary')

    with open(os.path.join(model_dir, model_file+' metriks'), 'w') as f:
        f.write(f"precision {pr}, \n")
        f.write(f"recall, {rec}, \n")
        f.write(f"f1, {f1}, \n")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('data_dir')
    p.add_argument('data_file')
    p.add_argument('model_dir')
    p.add_argument('model_file')
    args = p.parse_args()
    validate(args.data_dir, args.data_file, args.model_dir, args.model_file)

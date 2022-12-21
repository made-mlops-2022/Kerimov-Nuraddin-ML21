import os
import numpy as np
import pandas as pd
import argparse
import pickle

def work(data_file,predict_dir,model_file):

    data = pd.read_csv(data_file,index_col=False)

    with open(model_file, 'rb') as f:
        model = pickle.load(f)
    predicts = model.predict(data.drop(columns=['Unnamed: 0']))

    ans = pd.DataFrame(predicts)

    ans.to_csv(predict_dir,index=False)
 


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('data_file')
    p.add_argument('predict_dir')
    p.add_argument('model_file')
    args = p.parse_args()
    print(args.data_file,args.predict_dir,args.model_file)
    work(args.data_file,args.predict_dir,args.model_file)
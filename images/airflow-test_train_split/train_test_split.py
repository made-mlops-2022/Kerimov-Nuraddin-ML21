import os
import numpy as np
import pandas as pd
import argparse
from sklearn.model_selection import train_test_split

def data_split(process_dir,process_file,train_file,val_file) -> None:
    data = pd.read_csv(os.path.join(process_dir,process_file), index_col=False)
    train,val = train_test_split(data,test_size=0.1,random_state=42)

    train.to_csv(os.path.join(process_dir,train_file))
    val.to_csv(os.path.join(process_dir,val_file))
 


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('process_dir')
    p.add_argument('process_file')
    p.add_argument('train_file')
    p.add_argument('val_file')
    args = p.parse_args()
    data_split(args.process_dir,args.process_file,args.train_file,args.val_file)
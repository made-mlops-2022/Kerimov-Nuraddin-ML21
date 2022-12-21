import os
import numpy as np
import pandas as pd
import argparse


def process(dir, data_file, answer_file, process_dir, process_file) -> None:
    data = pd.read_csv(os.path.join(dir, data_file), index_col=False)
    data['condition'] = pd.read_csv(os.path.join(dir, answer_file), index_col=False)['condition']
    os.makedirs(process_dir, exist_ok=True)
    data.dropna(inplace=True)
    data.drop_duplicates(inplace=True)

    data.to_csv(os.path.join(process_dir, process_file))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('dir')
    p.add_argument('data_file')
    p.add_argument('answer_file')
    p.add_argument('process_dir')
    p.add_argument('process_data_file')
    args = p.parse_args()
    process(args.dir, args.data_file, args.answer_file,
            args.process_dir, args.process_data_file)

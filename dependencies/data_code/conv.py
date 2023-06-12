# This is only a trail and error file
# Do not work

import os
import pandas as pd
import glob

from prepare_dataset_for_modeling import prepare_dataset_for_modeling

PATH = '../../data/processed/'

path = os.path.abspath(PATH)
csv_files = glob.glob(os.path.join(path, '*.csv'))
print(f'PATH: {path}')
print(f'CSV_FILES: {csv_files}')

lst = []

def convert_csv(csv_files):
    for file_path in csv_files:
        print(f"Processing dataset: {os.path.basename(file_path)}")
        directory = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        cc = prepare_dataset_for_modeling(file_name, pred_type='c', data_directory=directory)
        print(cc)

cc = convert_csv(csv_files)
print(cc)




def convert_csv2(files):
    for f in files:
        dataset_name = os.path.basename(f)  # Extract the dataset name from the file path
        data_directory = os.path.dirname(f) 

        print(f'Processing dataset: {dataset_name}')
        print(f'directory: {data_directory}')

        file_path = os.path.join(data_directory, dataset_name)  # Construct the file path correctly

        x, y = prepare_dataset_for_modeling(dataset_name, pred_type='c', data_directory=data_directory)
        df = pd.DataFrame({'data': x, 'label': y})
        lst.append(df)
    return lst



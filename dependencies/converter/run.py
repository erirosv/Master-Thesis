import pandas as pd
import os
import io
import requests
import ssl
from sklearn import preprocessing
from sklearn.utils import shuffle
import glob
from converter import prepare_dataset_for_modeling

# dir paths
CONVERTED_DATA = '../../data/data_converted'
PROCESSED_DATA = '../../data/processed'

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
#SAVE_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, '/data')
SAVE_DIRECTORY = '../../data/test'
print(f'SAVE DIRECTORY : {SAVE_DIRECTORY}')

PATH = '../../data/processed/'
SAVE_PATH = '../../data/test/'

path = os.path.abspath(PATH)
csv_files = glob.glob(os.path.join(path, '*.csv'))
print(f'PATH: {path}')
print(f'CSV_FILES: {csv_files}')

def convert_csv(files):
    for f in files:
        dataset_name = os.path.basename(f)  # Extract the dataset name from the file path
        data_directory = os.path.dirname(f) 

        print(f'Processing dataset: {dataset_name}')
        print(f'directory: {data_directory}')

        x, y = prepare_dataset_for_modeling(dataset_name, pred_type='c', data_directory=data_directory) 
        print('--- CONVERTION COMPLETE ---')
        print(f'TYPE X : {x.shape}\n\n\n')
        print(f'TYPE Y : {y.shape}\n\n\n')

        print('--- CREATE DATAFRAME ---')
        #df = pd.DataFrame({'data': x.astype(float), 'label': y.astype(int)})
        for i in range(len(y)):
            for j in range(len(x)):
                df = pd.DataFrame({'data': x[j], 'label': y[i]})
            print(f'Y_VALUE : {y[i]}')
        print('--- COMPLETE --- ')

        print(df.head())
        # Create the save directory if it doesn't exist
        os.makedirs(SAVE_DIRECTORY, exist_ok=True)

        # Save DataFrame to CSV file
        save_file_path = os.path.join(SAVE_DIRECTORY, os.path.splitext(dataset_name)[0] + '.csv')
        df.to_csv(save_file_path, index=False)
        print(f"Saved converted DataFrame to: {save_file_path}")

convert_csv(csv_files)
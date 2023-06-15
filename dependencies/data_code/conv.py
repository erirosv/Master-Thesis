import os
import pandas as pd
import numpy as np
import glob

#from prepare_dataset_for_modeling import prepare_dataset_for_modeling
from prepare_dataset_for_modeling_github import prepare_dataset_for_modeling

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
SAVE_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, '../../data/data_converted_csv')

PATH = '../../data/processed/'
SAVE_PATH = '../../data/data_converted_csv/'

path = os.path.abspath(PATH)
csv_files = glob.glob(os.path.join(path, '*.csv'))
print(f'PATH: {path}')
print(f'CSV_FILES: {csv_files}')

def pre_data(data):
    print(f'Number of files: {len(data)}')

    for d in data:
        dataset_name = os.path.basename(d)  
        data_directory = os.path.dirname(d)

        print(f'Processing dataset: {dataset_name}')
        print(f'directory: {data_directory}')
      
        x, y = prepare_dataset_for_modeling(dataset_name, pred_type='c', data_directory=data_directory)

        df = pd.DataFrame({'data': x.astype(float), 'label': y.astype(int)})
        # Create the save directory if it doesn't exist
        os.makedirs(SAVE_DIRECTORY, exist_ok=True)

        # Save DataFrame to CSV file
        save_file_path = os.path.join(SAVE_DIRECTORY, os.path.splitext(dataset_name)[0] + '.csv')
        df.to_csv(save_file_path, index=False)
        print(f"Saved converted DataFrame to: {save_file_path}")

pre_data(csv_files)
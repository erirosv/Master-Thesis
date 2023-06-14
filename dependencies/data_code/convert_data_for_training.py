import os
import pandas as pd
import numpy as np
import glob

from prepare_dataset_for_modeling import prepare_dataset_for_modeling

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
SAVE_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, '../../data/data_converted_csv')

PATH = '../../data/processed/'
SAVE_PATH = '../../data/data_converted_csv/'

path = os.path.abspath(PATH)
csv_files = glob.glob(os.path.join(path, '*.csv'))
print(f'PATH: {path}')
print(f'CSV_FILES: {csv_files}')

lst = []

def convert_csv(files):
    for f in files:
        dataset_name = os.path.basename(f)  # Extract the dataset name from the file path
        data_directory = os.path.dirname(f) 

        print(f'Processing dataset: {dataset_name}')
        print(f'directory: {data_directory}')

        file_path = os.path.join(data_directory, dataset_name)  # Concatenate directory and dataset name correctly
        file_path2 = data_directory
        print(f'FILE_PATH: {file_path}')

        x, y = prepare_dataset_for_modeling(dataset_name, pred_type='c', data_directory=file_path2)

        ## Check if x and y have the same length
        # if len(x) != len(y):
        #     print(f'Adjusting lengths for dataset: {dataset_name}')

        #     # Calculate the mean of x and y
        #     mean_x = np.mean(x)
        #     mean_y = np.mean(y)

        #     max_length = max(len(x), len(y))
        #     x = np.pad(x, (0, max_length - len(x)), mode='constant', constant_values=mean_x)
        #     y = np.pad(y, (0, max_length - len(y)), mode='constant', constant_values=mean_y)

        max_length = max(len(x), len(y))

        # Pad the shorter array with NaN values
        if len(x) < max_length:
            x = np.pad(x.astype(float), (0, max_length - len(x)), mode='constant', constant_values=np.nan)
        if len(y) < max_length:
            y = np.pad(y.astype(float), (0, max_length - len(y)), mode='constant', constant_values=np.nan)



        df = pd.DataFrame({'data': x.astype(float), 'label': y.astype(float)})

        # Create the save directory if it doesn't exist
        os.makedirs(SAVE_DIRECTORY, exist_ok=True)

        # Save DataFrame to CSV file
        save_file_path = os.path.join(SAVE_DIRECTORY, os.path.splitext(dataset_name)[0] + '.csv')
        df.to_csv(save_file_path, index=False)
        print(f"Saved converted DataFrame to: {save_file_path}")

        lst.append(df)
    return lst



cc = convert_csv(csv_files)
print(cc)

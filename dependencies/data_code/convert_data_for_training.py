import os
import pandas as pd
import glob

from prepare_dataset_for_modeling import prepare_dataset_for_modeling

PATH = '../../data/processed'

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
        print(f'FILE_PATH: {file_path}')

        x, y = prepare_dataset_for_modeling(dataset_name, pred_type='c', data_directory=file_path)
        df = pd.DataFrame({'data': x, 'label': y})
        lst.append(df)
    return lst

cc = convert_csv(csv_files)
print(cc)


'''
for f in csv_files:
      
    # read the csv file
    df = pd.read_csv(f)
      
    # print the location and filename
    print('Location:', f)
    print('File Name:', f.split("\\")[-1])
      
    # print the content
    print(f'Content: {df}')
    #display(df)
    print()
'''
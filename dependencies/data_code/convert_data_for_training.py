import os
import pandas as pd
import glob

from prepare_dataset_for_modeling import prepare_dataset_for_modeling

PATH = '../../data/processed'

#path = os.getcwd(PATH)
path = os.path.abspath(PATH)
csv_files = glob.glob(os.path.join(path, '*.csv'))

# TODO:
# - grab the first csv file 
# - Run it through: prepare_dataset_for_modeling
# - stor the converted datafile and run through all the datasets

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
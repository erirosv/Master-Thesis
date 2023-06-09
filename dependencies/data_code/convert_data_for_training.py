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

def convert_csv(files):
    lst = []
    for f in files:
        print(f)
        x, y = prepare_dataset_for_modeling(f, pred_type='c')
        df = pd.DataFrame({'data':x, 'label':y})
        print(df)
        lst.append(df)
    return lst

#print(csv_files)
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
# -*- coding: utf-8 -*-
import pandas as pd
import os
import io
import requests
import ssl
from sklearn import preprocessing
from sklearn.utils import shuffle
import glob
import subprocess

def main():
    # dir paths
    SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    PATH = '../data/processed/'

    path = os.path.abspath(PATH)
    csv_files = glob.glob(os.path.join(path, '*.csv'))
    print(f'PATH: {path}')
    print(f'CSV_FILES: {csv_files}')

    for f in csv_files:
        dataset_name = os.path.basename(f)  # Extract the dataset name from the file path
        data_directory = os.path.dirname(f) 

        print('--- SEEDING DATASET ---')
        print(f'Processing dataset: {dataset_name}')
        print(f'directory: {data_directory}')
        script_path = os.path.join(SCRIPT_DIRECTORY, 'fsr_comp_FR_paper_master.py')
        python_executable = '/opt/homebrew/opt/python@3.10'  # Replace with the actual path to the 'python' executable
        subprocess.call(['python3', python_executable, script_path, dataset_name])
        print('--- SEEDING COMPLETE ---\n')


if __name__ == '__main__':
    main()

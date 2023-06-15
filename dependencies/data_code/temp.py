import pandas as pd
import os
import glob
import io
import requests
import ssl
from sklearn import preprocessing
from sklearn.utils import shuffle

# dir paths
CONVERTED_DATA = '../../data/data_converted'
PROCESSED_DATA = '../../data/processed'

# Converted datastest
path_converted = os.path.abspath(CONVERTED_DATA)
csv_files_converted = glob.glob(os.path.join(path_converted, '*.csv'))
print(path_converted)
print(csv_files_converted)

# processed data sets
path_processed = os.path.abspath(PROCESSED_DATA)
csv_files_processed = glob.glob(os.path.join(path_processed, '*.csv'))
print(path_processed)
print(csv_files_processed)

#df_conv = pd.read_csv(csv_files_converted[0])
#df_conv.head()

#df_pros = pd.read_csv(csv_files_processed[4])
#df_pros.head()

def prepare_dataset_for_modeling(dataset_name,
                                 pred_type,
                                 data_directory=None,
                                 na_values='?',
                                 n_samples_max=None,
                                 random_state=999,
                                 drop_const_columns=True,
                                 scale_data=True):


    if pred_type not in ['c', 'r']:
        raise ValueError("Prediction type needs to be either 'c' for classification or 'r' for regression.")

    if data_directory:
        # read in from local directory
        df = pd.read_csv(data_directory + dataset_name, na_values=na_values, header=0)
        print(f'DATA: {df.head()}')
    else:
        # read in the data file from GitHub into a Pandas data frame
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
                getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = ssl._create_unverified_context
        github_location = 'https://raw.githubusercontent.com/vaksakalli/datasets/master/'
        dataset_url = github_location + dataset_name.lower()
        df = pd.read_csv(io.StringIO(requests.get(dataset_url).content.decode('utf-8')), na_values=na_values, header=0)

    # drop missing values before (any) sampling
    df = df.dropna()

    n_observations = df.shape[0]  # no. of observations in the dataset
    n_samples = n_observations  # initialization - no. of observations after (any) sampling
    if n_samples_max and (n_samples_max < n_observations):
        # do not sample more rows than what is in the dataset
        n_samples = n_samples_max
    df = shuffle(df, n_samples=n_samples, random_state=random_state)

    if drop_const_columns:
        df = df.loc[:, df.nunique() > 1]
    df = df.drop_duplicates(ignore_index=True)

    y = df.iloc[:, -1].values
    x = df.iloc[:, :-1]

    categorical_cols = x.columns[x.dtypes == object].tolist()

    print(f'\nnumber of nominal categorical descriptive features detected: {len(categorical_cols)}\n')

    for col in categorical_cols:
        n = len(x[col].unique())
        if n == 2:
            x[col] = pd.get_dummies(x[col], drop_first=True)
    x = pd.get_dummies(x).values

    if scale_data:
        x = preprocessing.MinMaxScaler().fit_transform(x)
        if pred_type == 'r':
            y = preprocessing.MinMaxScaler().fit_transform(y.reshape(-1, 1)).flatten()

    if pred_type == 'c':
        y = preprocessing.LabelEncoder().fit_transform(y)

    return x, y



x, y = prepare_dataset_for_modeling(csv_files_processed[4], pred_type='c')
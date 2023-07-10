'''
This code performs feature selection for a given list of wrappers & methods
and writes detailed & summary results to csv files
'''

import os
import sys
import random
import numpy as np
import pandas as pd
import sklearn.metrics as metrics
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from scipy import stats
from itertools import combinations

from sklearn.naive_bayes import MultinomialNB

import fsr_methods as fsrm
from prepare_dataset_for_modeling_github import prepare_dataset_for_modeling

import warnings

warnings.filterwarnings("ignore")

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
###
num_features_list = [5, 10, 15, 20, 25]  # list of num_features to loop over. Default: [5, 10, 15]
###
params = dict()
# choose a run mode for spFtSel: regular or short
params['pred_type'] = 'c'  # used during data prep
###
params['algo_comp_cv_reps'] = 5  # we want 5 reps for the **full** runs
params['cv_folds'] = 5
params['n_jobs'] = 1
###
params['pvalue_cutoff'] = 0.05
###
params['data_directory'] = '../data/processed/'
params['seed'] = 1
params['run_details'] = 'gene_fsr_'  # put any run details here as a prefix
params['results_directory'] = params['run_details'] + 'results' + '/'
params['scoring_metric'] = 'accuracy'
params['cv_control'] = RepeatedStratifiedKFold(n_splits=params['cv_folds'],
                                               n_repeats=params['algo_comp_cv_reps'],
                                               random_state=params['seed'])
#########
wrappers = dict()
wrappers['DT'] = DecisionTreeClassifier()
wrappers['KNN'] = KNeighborsClassifier(n_neighbors=1)
wrappers['NB'] = GaussianNB()
wrappers['SVM'] = LinearSVC()
###
# store sel_features_* functions for each FS method, including full set of features
fs_methods = dict()
###
# fs_methods['Full'] = fsrm.sel_features_full
fs_methods['InfoGain'] = fsrm.sel_features_mutual_inf
fs_methods['FScore'] = fsrm.sel_features_fscore
fs_methods['MRMR'] = fsrm.sel_features_mrmr
fs_methods['SFS'] = fsrm.sel_features_sfs

fs_methods['GA'] = fsrm.sel_features_ga
fs_methods['SPFSR'] = fsrm.sel_features_spfsr
#fs_methods['BSPSA'] = fsrm.sel_features_bspsa
###
fs_methods['RFI'] = fsrm.sel_features_rf_imp
# fs_methods['ChiSq'] = fsrm.sel_features_chi2
# fs_methods['CMIM'] = fsrm.sel_features_cmim
fs_methods['ReliefF'] = fsrm.sel_features_relieff
fs_methods['PCA'] = fsrm.sel_features_pca

fs_methods['CFS'] = fsrm.sel_features_correlation_best
#####
# select which dataset to run - you can specify the dataset name in the command line as well
# dataset = 'sonar.csv'
#dataset = 'west.csv'
dataset = sys.argv[1]

if not os.path.exists(params['results_directory']):
    os.mkdir(params['results_directory'])


def main():
    print("Results directory = ", params['results_directory'])

    # make sure the results are repeatable by setting these two seeds at the beginning
    np.random.seed(params['seed'])
    random.seed(params['seed'])

    # we use these column names for the resulting csv files
    results_columns_basic = ['dataset', '_wrapper', 'num_features_algo']
    results_columns = results_columns_basic + ['fs_method', 'cv_error_mean', 'cv_error_std']

    # define an empty DataFrame to hold summary results for each dataset
    results_dataset = pd.DataFrame(columns=results_columns)

    # the _cv df below stores results at the fold level for the t-test for each dataset
    results_dataset_cv = pd.DataFrame()

    # this df stores the outcomes of the paired t-tests
    results_dataset_ttest = pd.DataFrame(columns=results_columns_basic +
                                                 ['fs_method1', 'fs_method2',
                                                  'fs_method1_cv', 'fs_method2_cv', 'p_value', 'winner'])

    # get the x & y for this dataset
    x, y = prepare_dataset_for_modeling(dataset,
                                        pred_type=params['pred_type'],
                                        data_directory=params['data_directory'])

    dataset_name = os.path.splitext(dataset)[0]  # remove the file extension
    print("dataset = " + dataset_name + ", shape = ", x.shape)

    # loop over wrappers
    for wrapper_name, wrapper in wrappers.items():

        print("wrapper_name = " + wrapper_name)

        # define here so that we only have the current _wrapper's cv results in this df
        results_dataset_cv_wrapper = pd.DataFrame(columns=results_columns_basic +
                                                          ['cv_' + fs_method for fs_method in fs_methods.keys()],
                                                  index=list(range(params['cv_folds'] * params['algo_comp_cv_reps'])))

        # loop over number of features
        for num_features_algo in num_features_list:

            print("num_features_algo = ", num_features_algo)

            # loop over fs methods
            for fs_method_name, fs_method in fs_methods.items():

                print("fs_method_name = " + fs_method_name)

                results_row_basic = [dataset_name,
                                     wrapper_name,
                                     int(num_features_algo)]

                # now set the basic cv info, notice how we replicate results_row_basic using list *
                results_dataset_cv_wrapper[results_columns_basic] = np.array(
                    results_row_basic * params['algo_comp_cv_reps'] * params['cv_folds']).reshape(-1, len(
                    results_row_basic))

                cv_results = np.zeros(0)  # holds the cv results at the rep/ fold level
                # perform the repeated cross validation,
                # first loop over repetitions, then folds
                for rep_no in range(1, 1 + params['algo_comp_cv_reps']):
                    # get the fold
                    sk_fold = StratifiedKFold(n_splits=params['cv_folds'],
                                              shuffle=True,
                                              random_state=params['seed'] + rep_no)

                    # loop over the folds for this cv repetition
                    fold_no = 0
                    for train_index, test_index in sk_fold.split(x, y):
                        fold_no += 1
                        x_train, x_test = x[train_index], x[test_index]
                        y_train, y_test = y[train_index], y[test_index]

                        # get the indices of the best features for each fs method
                        if fs_method_name == 'PCA':
                            # unlike other fs method functions that return indices of selected features,
                            # the function corresponding to PCA returns just a PCA object
                            ret_fs = fs_methods[fs_method_name](num_features=num_features_algo)
                            pca_fit = ret_fs['pca'].fit(x_train)
                            x_train_fs = pca_fit.transform(x_train)
                            # transform test data into PCA using the same transformation as in training
                            x_test_fs = pca_fit.transform(x_test)
                        else:
                            ret_fs = fs_methods[fs_method_name](x=x_train,
                                                                y=y_train,
                                                                wrapper=wrapper,
                                                                num_features=num_features_algo,
                                                                params=params)

                        # get the indices of the best features for each fs method
                        # if fs_method_name == 'PCA':
                        #     # unlike other fs method functions that return indices of selected features,
                        #     # the function corresponding to PCA returns just a PCA object
                        #     ret_fs = fs_methods[fs_method_name](num_features=num_features_algo)
                        #     pca_fit = ret_fs['pca'].fit(x_train)
                        #     x_train_fs = pca_fit.transform(x_train)
                        #     # transform test data into PCA using the same transformation as in training
                        #     x_test_fs = pca_fit.transform(x_test)
                        # else:
                        #     if fs_method_name == 'GA':
                        #         ret_fs = fs_methods[fs_method_name](x=x_train, y=y_train, num_features=num_features_algo, params=params)
                        #     else:
                        #         if fs_method_name == 'sel_features_ga':
                        #             if params['pred_type'] == 'classification' and isinstance(wrapper, MultinomialNB):
                        #                 # Skip feature selection if the wrapper is MultinomialNB
                        #                 ret_fs = {'idx_sf': range(x_train.shape[1])}
                        #             else:
                        #                 ret_fs = fs_methods[fs_method_name](x=x_train, y=y_train, num_features=num_features_algo, wrapper=wrapper, params=params)
                        #         else:
                        #             ret_fs = fs_methods[fs_method_name](x=x_train, y=y_train, num_features=num_features_algo, wrapper=wrapper, params=params)

                            idx_fs = ret_fs['idx_sf']  # indices of the selected features
                            x_train_fs = x_train[:, idx_fs]
                            x_test_fs = x_test[:, idx_fs]

                        # if fs_method_name == 'SPSA':
                        #     # importance of selected features
                        #     print('Importance of selected features: ', ret_fs['sp_output'].get('importance').round(4))
                        #     print('gains_raw: ', ret_fs['sp_output'].get('iter_results').get('gains_raw'))

                        # fit the _wrapper with the selected features in the train data
                        wrapper.fit(x_train_fs, y_train)

                        # predict the test data with the selected features and compute the error
                        y_predict = wrapper.predict(x_test_fs)
                        fold_error = np.round(1 - metrics.accuracy_score(y_test, y_predict), 4)
                        cv_results = np.append(cv_results, fold_error)
                        print("cv rep.", rep_no, "& fold", fold_no, ': test error =', fold_error)

                cv_error_mean = cv_results.mean().round(3)
                cv_error_std = cv_results.std().round(3)

                ## sm: summary
                results_row_sm = results_row_basic + [fs_method_name,
                                                      cv_error_mean.round(3),
                                                      cv_error_std.round(3)]

                results_dataset.loc[len(results_dataset)] = results_row_sm
                print(results_row_sm)

                # add the rep/ fold results for this fs method
                results_dataset_cv_wrapper['cv_' + fs_method_name] = np.array(cv_results).reshape(-1, 1)

            # now combine cv results of all fs methods for this dataset
            results_dataset_cv = pd.concat([results_dataset_cv, results_dataset_cv_wrapper])

            # get all pairs of fs_methods and do a two-tailed t-test
            fs_methods_list = list(fs_methods.keys())
            fs_method_pairs = list(combinations(fs_methods_list, 2))

            for fs_pair in fs_method_pairs:
                fs_method1 = fs_pair[0]
                fs_method2 = fs_pair[1]

                # convert this to integer so that the comparison below it works
                results_dataset_cv['num_features_algo'] = results_dataset_cv['num_features_algo'].astype(int)

                curr_cv_data = results_dataset_cv[(results_dataset_cv['_wrapper'] == wrapper_name) &
                                                  (results_dataset_cv['num_features_algo'] == num_features_algo)]

                fs_method1_cv = curr_cv_data['cv_' + fs_method1]
                fs_method2_cv = curr_cv_data['cv_' + fs_method2]

                ttest_pvalue = stats.ttest_rel(fs_method1_cv, fs_method2_cv).pvalue.round(3)

                fs_method1_cv_mean = fs_method1_cv.mean().round(3)
                fs_method2_cv_mean = fs_method2_cv.mean().round(3)

                # which method is significantly better than the other?
                ttest_winner = ''
                if ttest_pvalue > params['pvalue_cutoff']:
                    ttest_winner = 'tie'
                else:
                    if fs_method1_cv_mean < fs_method2_cv_mean:
                        ttest_winner = fs_method1
                    else:
                        ttest_winner = fs_method2

                results_row_ttest = results_row_basic + [fs_method1,
                                                         fs_method2,
                                                         fs_method1_cv_mean,
                                                         fs_method2_cv_mean,
                                                         ttest_pvalue,
                                                         ttest_winner]

                results_dataset_ttest.loc[len(results_dataset_ttest)] = results_row_ttest
                print(results_row_ttest)

    # this is at the dataset level:
    results_file_name = params['results_directory'] + params['run_details'] + 'results'
    results_dataset.to_csv(results_file_name + '_' + dataset_name + '.csv', index=False)
    results_dataset_cv.to_csv(results_file_name + '_cv_' + dataset_name + '.csv', index=False)
    results_dataset_ttest.to_csv(results_file_name + '_ttest_' + dataset_name + '.csv', index=False)

    print('results_dataset:')
    print(results_dataset)
    print('results_dataset_ttest:')
    print(results_dataset_ttest)


if __name__ == '__main__':  # need this for parallelism to work
    main()

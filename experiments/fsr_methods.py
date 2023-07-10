import os
import numpy as np
import pandas as pd
from scipy.io import loadmat
from sklearn import preprocessing
from sklearn.decomposition import PCA
from genetic_selection import GeneticSelectionCV
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif, chi2, mutual_info_classif, f_regression, mutual_info_regression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
###
from skfeature.function.similarity_based import fisher_score
from skfeature.function.statistical_based import chi_square
from skfeature.function.information_theoretical_based.MRMR import mrmr
from skfeature.function.information_theoretical_based.CMIM import cmim
#from skfeature.function.similarity_based import reliefF
from skfeature.function.similarity_based.reliefF import reliefF

from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from sklearn.naive_bayes import MultinomialNB
# from spFSR_before_hot_start import SpFSR
from spFSR import SpFSR
from spFSR.SpFSR import SpFSR


def get_datasets(params):
    datasets = list()
    for root, dirs, files in os.walk(params['data_directory']):
        for file in files:
            if file.endswith('csv'):
                # print(file)
                datasets.append(file)
    datasets.sort()
    return datasets


def sel_features_pca(num_features):
    """just get the PCA object - don't do any fitting here"""
    pca = PCA(n_components=num_features)
    # x_fs = pca.fit_transform(_x)
    ret_dict = dict({'pca': pca})
    return ret_dict


def sel_features_full(x, **kwargs):
    """select full set of features"""
    ret_dict = {'idx_sf': np.arange(x.shape[1])}
    return ret_dict


def sel_features_chi2(x, y, num_features, params, **kwargs):
    if params['pred_type'] == 'r':
        raise ValueError('Error: chi2 method can be used only for classification problems!')
    fs_fit = SelectKBest(chi2, k=num_features)
    # chi2 requires non-negative _x
    # x = preprocessing.MinMaxScaler().fit_transform(x)  # scale _x between 0 and 1
    fs_fit.fit_transform(x, y)
    idx_sf = np.where(fs_fit.get_support())[0]
    ret_dict = dict({'idx_sf': idx_sf})
    return ret_dict


def sel_features_fscore(x, y, num_features, params, **kwargs):
    if params['pred_type'] == 'c':
        fs_fit = SelectKBest(f_classif, k=num_features)
    else:
        fs_fit = SelectKBest(f_regression, k=num_features)
    fs_fit.fit_transform(x, y)
    idx_sf = np.where(fs_fit.get_support())[0]
    ret_dict = dict({'idx_sf': idx_sf})
    return ret_dict


def sel_features_mutual_inf(x, y, num_features, params, **kwargs):
    if params['pred_type'] == 'c':
        fs_fit = SelectKBest(mutual_info_classif, k=num_features)
    else:
        fs_fit = SelectKBest(mutual_info_regression, k=num_features)
    fs_fit.fit_transform(x, y)
    idx_sf = np.where(fs_fit.get_support())[0]
    ret_dict = dict({'idx_sf': idx_sf})
    return ret_dict

# added [0] and .astype(int)
def sel_features_mrmr(x, y, num_features, **kwargs):
    idx_sf = mrmr(x, y, n_selected_features=num_features) # here [0]
    idx_sf = idx_sf[:num_features] # here .astype(int)
    # print('mrmr idx_sf -->', idx_sf)
    ret_dict = dict({'idx_sf': idx_sf})
    return ret_dict


def sel_features_cmim(x, y, num_features, **kwargs):
    idx_sf = cmim(x, y, n_selected_features=num_features)
    idx_sf = idx_sf[0:num_features]
    # print('cmim idx_sf -->', idx_sf)
    ret_dict = dict({'idx_sf': idx_sf})
    return ret_dict


def sel_features_relieff(x, y, num_features, **kwargs):
    score = reliefF(x, y)
    #idx_sf = reliefF.feature_ranking(score)  # largest to smallest
    idx_sf = score.argsort()[::-1]
    idx_sf = idx_sf[0:num_features]
    ret_dict = dict({'idx_sf': idx_sf})
    return ret_dict


def sel_features_sfs(x, y, num_features, params, wrapper):
    # sequential forward (non-floating) selection
    sfs_model = SFS(wrapper,
                    k_features=num_features,
                    forward=True,
                    floating=False,
                    verbose=0,
                    cv=0,  # no CV here
                    scoring=params['scoring_metric'])
    sfs_model = sfs_model.fit(x, y)
    ret_dict = dict({'idx_sf': sfs_model.k_feature_idx_})
    # print('sfs_model.k_feature_idx_:', sfs_model.k_feature_idx_)
    return ret_dict

# problem:
# - GeneticSelectionCV
# Testing:
# - from tpot import TPOTClassifier
#from tpot import TPOTClassifier, TPOTRegressor
#from sklearn.model_selection import train_test_split
import re
def sel_features_ga(x, y, num_features, params, wrapper):
    n_population = 20  # default is 40
    n_generations = 60  # default is 300: 20*60 = 1200 = 100 iterations * 4 grad. avg. * 3 fn. eval per iteration
    cv_ga = GeneticSelectionCV(estimator=wrapper,
                               scoring=params['scoring_metric'],
                               cv=params['cv_folds'],
                               n_jobs=params['n_jobs'],
                               n_population=n_population,
                               n_generations=n_generations,
                               n_gen_no_change=int(n_generations/3),
                               max_features=num_features,
                               crossover_proba=0.8,
                               crossover_independent_proba=0.8,
                               mutation_proba=0.1,
                               mutation_independent_proba=0.1,
                               tournament_size=2,
                               verbose=0,
                               caching=False)
    fs_fit = cv_ga.fit(x, y)
    idx_sf = np.where(fs_fit.support_)[0]  # sf: selected features
    ret_dict = dict({'idx_sf': idx_sf})
    # print("GA num_features = ", len(idx_sf))
    return ret_dict

####################################
def sel_features_rf_imp(x, y, num_features, params, **kwargs):
    if params['pred_type'] == 'c':
        model = RandomForestClassifier(n_estimators=50, random_state=1)
    else:
        model = RandomForestRegressor(n_estimators=50, random_state=1)
    model.fit(x, y)
    idx_sf = np.argsort(model.feature_importances_)[::-1][0:num_features]
    ret_dict = dict({'idx_sf': idx_sf})
    return ret_dict


#######################################
def sel_features_spfsr(x, y, num_features, params, wrapper):

    sp_engine = SpFSR(x, y, pred_type=params['pred_type'],
                      scoring=params['scoring_metric'],
                      wrapper=wrapper)

    sp_output = sp_engine.run(num_features=num_features,
                              n_jobs=params['n_jobs'],
                              print_freq=9999,
                              ).results

    ret_dict = dict()
    ret_dict['sp_output'] = sp_output
    ret_dict['idx_sf'] = sp_output.get('selected_features')
    ret_dict['sp_iters'] = sp_output.get('total_iter_for_opt')
    return ret_dict


#######################################
def sel_features_spfsr_filter(x, y, num_features, params, **kwargs):

    sp_engine = SpFSR(x, y, pred_type=params['pred_type'],
                      scoring=params['scoring_metric'],
                      wrapper=None)

    sp_output = sp_engine.run(num_features=num_features,
                              n_jobs=params['n_jobs'],
                              print_freq=9999,
                              ).results

    ret_dict = dict()
    ret_dict['sp_output'] = sp_output
    ret_dict['idx_sf'] = sp_output.get('selected_features')
    ret_dict['sp_iters'] = sp_output.get('total_iter_for_opt')
    return ret_dict


#######################################
def sel_features_bspsa(x, y, num_features, params, wrapper):
    sp_engine = SpFSR(x, y, pred_type=params['pred_type'],
                      scoring=params['scoring_metric'],
                      wrapper=wrapper)

    sp_output = sp_engine.run(num_features=num_features,
                              n_jobs=params['n_jobs'],
                              gain_type='mon',
                              num_grad_avg=1,
                              cv_reps_eval=1,
                              cv_reps_grad=1,
                              use_hot_start=False,
                              print_freq=9999,
                              ).results

    ret_dict = dict()
    ret_dict['sp_output'] = sp_output
    ret_dict['idx_sf'] = sp_output.get('selected_features')
    ret_dict['sp_iters'] = sp_output.get('total_iter_for_opt')
    return ret_dict


# #######################################
# def sel_features_spfsr_filter(x, y, num_features, params, wrapper):
#
#     # sp_engine = SpFSR(x, y, wrapper, params['scoring_metric'])
#     sp_engine = SpFSR(x, y, pred_type=params['pred_type'], scoring=params['scoring_metric'])  # , wrapper=wrapper)
#
#     sp_output = sp_engine.run(num_features=num_features,
#                               n_jobs=params['n_jobs'],
#                               n_samples_max=None,
#                               use_hot_start=True,
#                               print_freq=50,
#                               ).results
#     ###
#     ret_dict = dict()
#     ret_dict['sp_output'] = sp_output
#     ret_dict['idx_sf'] = sp_output.get('selected_features')
#     ret_dict['sp_iters'] = sp_output.get('total_iter_for_opt')
#     return ret_dict


# *** CORRELATION 
def sel_features_correlation_best(x, y, num_features, **kwargs):
    x = pd.DataFrame(x)
    y = pd.Series(y)
    # Compute the correlation between each feature and the target variable
    correlation_scores = abs(x.apply(lambda x: x.corr(y)))
    
    # Select the top k features with the highest correlation scores
    top_features = correlation_scores.nlargest(num_features).index
    
    # Return the selected features as a new DataFrame
    X_selected = x[top_features]
    idx_sf = top_features
    
    return {'X_selected': X_selected, 'idx_sf': idx_sf}
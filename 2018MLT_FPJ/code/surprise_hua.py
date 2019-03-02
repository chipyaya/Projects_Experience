import pandas as pd
import numpy as np
import pickle
import os

from surprise import Dataset
from surprise import Reader
from surprise.model_selection import train_test_split
from surprise import accuracy
from surprise import SVD, SVDpp, NMF
from surprise import NormalPredictor, BaselineOnly
from surprise import KNNBasic, KNNWithMeans, KNNWithZScore, KNNBaseline
from surprise import SlopeOne 
from surprise import CoClustering 
from util import *


user, book, user_test, book_test, rate, user_all, book_all, user_dict, book_dict = read_data()

# Creation of the dataframe. Column names are irrelevant.
ratings_dict = {'itemID': book,
                'userID': user,
                'rating': rate}
df = pd.DataFrame(ratings_dict)

# A reader is still needed but only the rating_scale param is requiered.
reader = Reader(rating_scale=(1, 10))

# The columns must correspond to user id, item id and ratings (in that order).
data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)


# Models
algos = []
algos_name = []

algos_name.append('BS_ALS')
bsl_options = {'method': 'als',
               'n_epochs': 5,
               'reg_u': 1,
               'reg_i': 5
               }
algos.append(BaselineOnly(bsl_options=bsl_options))

algos_name.append('BS_SGD')
bsl_options = {'method': 'sgd',
               'learning_rate': .01,
               'n_epochs': 20
               }
algos.append(BaselineOnly(bsl_options=bsl_options))

algos_name.append('NMF')
algos.append(NMF(n_factors=2,n_epochs=10,biased=True,reg_pu=0.06,reg_qi=0.06,reg_bu=0.01,reg_bi=0.01,lr_bu=0.01,lr_bi=0.01,random_state=1)_

algos_name.append('SVD')
algos.append(SVD(n_factors=5, n_epochs=20, lr_all=0.005, reg_all=0.02, random_state=1))

algos_name.append('SVDpp')
algos.append(SVDpp(n_factors=1, random_state=1))

#algos_name.append('KNN')
#algos.append(KNNBasic())

for name, algo in zip(algos_name, algos):
    print('===', name)
    trainset, testset = train_test_split(data, test_size=0.2, random_state=1)

    # train and test algorithm.
    predictions = algo.fit(trainset).test(testset)

    # Compute and print Root Mean Absolute Error
    accuracy.mae(predictions, verbose=True)

    # predict
    pred_test = []
    for u,b in zip(user_test, book_test):
        pred_test.append(algo.predict(u,b).est)
    pred_test = np.array(pred_test)
    pred_test[pred_test > 10] = 10
    pred_test[pred_test < 1] = 1

    # write output
    output_path_raw = os.path.join('outputs', 'subm_surprise_'+name+'_raw.csv')
    np.savetxt(output_path_raw, pred_test, fmt='%1.4f')
    print('Ouput written to %s' % output_path_raw)
    output_path_round = os.path.join('outputs', 'subm_surprise_'+name+'_round.csv')
    np.savetxt(output_path_round, np.around(pred_test), fmt='%d')
    print('Ouput written to %s' % output_path_round)


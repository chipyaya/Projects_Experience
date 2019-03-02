import pickle
import numpy as np
import os
import pandas as pd
import argparse
import json
from util import *
from collections import Counter

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import Adam
from keras.backend.tensorflow_backend import set_session
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
from keras.callbacks import LambdaCallback
from keras import backend as K


config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.25
set_session(tf.Session(config=config))

DATA_DIR = '../data'
PICKLE_DIR = '../pickles'
seed = 7

def parse_args():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--bs', type=int, default=256, help='batch_size')
    parser.add_argument('--ep', type=int, default=10, help='epoch')
    parser.add_argument('--lr', type=float, default=1e-4, help='learning_rate')
    parser.add_argument('--loss', type=str, default='mape', help='loss: mae or mape')
    args = parser.parse_args()


def main():
    # seed
    np.random.seed(seed)

    # load data
    print('=== Loading data')
    X_data_td,y_data_td,X_test_td = \
            pickle.load(open(os.path.join(PICKLE_DIR, 'title_descr_vec.p'), 'rb'))
    X_data_o,y_data_o,X_test_o = \
            pickle.load(open(os.path.join(PICKLE_DIR, 'others_vec.p'), 'rb'))
    userID_list_test_filtered, isbn_list_test_filtered = \
            pickle.load(open(os.path.join(PICKLE_DIR, 'userID_isbn_list_test_filtered.p'), 'rb'))
    br_test = pd.read_csv(os.path.join(DATA_DIR, 'book_ratings_test.csv'))

    # concat data
    X_data = X_data_o
    X_test = X_test_o
    #X_data = np.concatenate((X_data_o, X_data_td), axis=1)
    #X_test = np.concatenate((X_test_o, X_test_td), axis=1)
    y_data = y_data_o

    # split data to train and validataion
    indices = np.random.permutation(X_data.shape[0])
    X_data, y_data = X_data[indices], y_data[indices]

    trainN = int(0.8 * X_data.shape[0])
    X_train = X_data[:trainN]
    y_train = y_data[:trainN]
    X_val = X_data[trainN:]
    y_val = y_data[trainN:]

    print(sorted(Counter(y_train).items()))
    print('X_train:', X_train.shape, 'y_train:', y_train.shape)

    #from imblearn.combine import SMOTEENN, SMOTETomek
    #from imblearn.under_sampling import RandomUnderSampler
    #rus = RandomUnderSampler(random_state=0)
    #X_train, y_train= rus.fit_sample(X_data, y_data)
    #smote_tomek = SMOTETomek(random_state=0)
    #X_train, y_train = smote_tomek.fit_sample(X_data, y_data)
    #sme = SMOTEENN(random_state=42)
    #X_train, y_train = sme.fit_sample(X_data, y_data)
    #print(sorted(Counter(y_train).items()))
    #print('X_train:', X_train.shape, 'y_train:', y_train.shape)

    # normalize
    print('=== Normalizing')
    X_mean, X_std, X_train_normalized = normalize(X_train)
    X_val_normalized = normalize_given_m_s(X_val, X_mean, X_std)
    X_test_normalized = normalize_given_m_s(X_test, X_mean, X_std)

    global y_mean
    global y_std
    y_mean, y_std, y_train_normalized = normalize(y_train)
    y_val_normalized = normalize_given_m_s(y_val, y_mean, y_std)

    # model
    print('=== Training')
    batch_size = args.bs
    epochs = args.ep

    model = Sequential()
    model.add(Dense(128, input_shape=(X_data.shape[1],), activation='relu'))
    model.add(Dense(64, input_shape=(X_data.shape[1],), activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(1))
    model.summary()
    opt = Adam(lr=args.lr, decay=1e-8) #e-6

    if args.loss == 'mape':
        model.compile(loss=mape_denormalized(y_mean, y_std), optimizer=opt)
    elif args.loss == 'mae':
        model.compile(loss=mae_denormalized(y_mean, y_std), optimizer=opt)

    callbacks = []
    #callbacks.append(EarlyStopping(monitor='val_loss', patience=100))

    if not os.path.exists('checkpoints'):
        os.makedirs('checkpoints')

    best_model_path = os.path.join('checkpoints', 'model_nn_'+args.loss+'.h5')
    callbacks.append(ModelCheckpoint(best_model_path, monitor='val_loss', verbose=0, save_best_only=True))
    json_log = open(os.path.join('checkpoints', 'loss_log_nn_'+args.loss+'.json'), mode='wt', buffering=1)
    json_logging_callback = LambdaCallback(
        on_epoch_end=lambda epoch, logs: json_log.write(
            json.dumps({'epoch': epoch, 'loss': logs['loss'], 'val_loss': logs['val_loss']}) + '\n'),
        on_train_end=lambda logs: json_log.close()
    )
    callbacks.append(json_logging_callback)


    model.fit(X_train_normalized, y_train_normalized,
                  batch_size=batch_size,
                  epochs=epochs,
                  validation_data=(X_val_normalized, y_val_normalized),
                  shuffle=True, 
                  callbacks=callbacks,
                  verbose=1)

    # load best model
    model.load_weights(best_model_path)
    if args.loss == 'mape':
        model.compile(loss=mape_denormalized(y_mean, y_std), optimizer=opt)
    elif args.loss == 'mae':
        model.compile(loss=mae_denormalized(y_mean, y_std), optimizer=opt)

    # predict
    print('=== Predicting')
    predictions = model.predict(X_test_normalized, batch_size=batch_size)
    predictions = denormalize(predictions, y_mean, y_std)

    # subm_dict[(User-ID,ISBN)] = pred
    ## init with mean rating 7.6
    print('=== Making submission')
    subm_dict = {}
    for row in br_test.itertuples():
        subm_dict[(row[1], row[2])] = 7.6

    ## fill in with model pred
    for user_id, isbn, pred in zip(userID_list_test_filtered, isbn_list_test_filtered, predictions.reshape(-1)):
        subm_dict[(user_id, isbn)] = pred

    ## turn pred to an np array and save
    br_test_pred = []
    for row in br_test.itertuples():
        br_test_pred.append(subm_dict[(row[1], row[2])])
        
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    output_path = os.path.join('outputs', 'subm_nn_'+args.loss+'.csv')
    if args.loss == 'mape':
        np.savetxt(output_path, np.array(br_test_pred), fmt='%1.4f')
    elif args.loss == 'mae':
        np.savetxt(output_path, np.around(br_test_pred), fmt='%d')


if __name__ == '__main__':
    parse_args()
    main()

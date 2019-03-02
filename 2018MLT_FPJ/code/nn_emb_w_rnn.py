import pickle
import os
import numpy as np
import argparse
import json
import pandas as pd
from util import *

from keras.optimizers import Adam
from keras.layers import Embedding
from keras.layers import Concatenate
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Bidirectional
from keras.layers import TimeDistributed
from keras.layers import Input
from keras.layers import Conv1D
from keras.layers import MaxPooling1D
from keras.layers import Flatten
from keras.layers import Dropout
from keras.models import Model
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
from keras.callbacks import LambdaCallback
from keras.backend.tensorflow_backend import set_session
import tensorflow as tf

MAX_SEQUENCE_TITLE = 40
MAX_SEQUENCE_DESCR = 200
MAX_NUM_WORDS = 10000
EMBEDDING_DIM = 100
PICKLE_DIR = '../pickles'
DATA_DIR = '../data'
seed = 7

config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.4
set_session(tf.Session(config=config))

def parse_args():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--bs', type=int, default=2048, help='batch_size')
    parser.add_argument('--ep', type=int, default=10, help='epoch')
    parser.add_argument('--lr', type=float, default=1e-4, help='learning_rate')
    parser.add_argument('--loss', type=str, default='mape', help='loss: mae or mape')
    args = parser.parse_args()

def main():
    # seed
    np.random.seed(seed)

    # load data
    print('=== Loading data')
    word_index_title, seq_train_title, seq_test_title, word_index_descr, seq_train_descr, seq_test_descr = \
            pickle.load(open(os.path.join(PICKLE_DIR, 'seq_train_test_title_descr.p'), 'rb'))

    X_data_title, X_data_descr, y_data, X_test_title, X_test_descr = \
            pickle.load(open(os.path.join(PICKLE_DIR, 'title_descr_seq.p'), 'rb'))
    X_data_o, y_data_o, X_test_o = \
            pickle.load(open(os.path.join(PICKLE_DIR, 'others_vec.p'), 'rb'))
    userID_list_test_filtered, isbn_list_test_filtered = \
            pickle.load(open(os.path.join(PICKLE_DIR, 'userID_isbn_list_test_filtered.p'), 'rb'))
    br_test = pd.read_csv(os.path.join(DATA_DIR, 'book_ratings_test.csv'))


    y_data = y_data_o

    #print(seq_train_title.shape)  #(105573, 40)
    #print(seq_test_title.shape)   #(79232, 40)
    #print(seq_train_descr.shape)  #(105573, 200)
    #print(seq_test_descr.shape)   #(79232, 200)

    #print(X_data_o.shape)  #(230393, 6)
    #print(y_data_o.shape)  #(230393,)
    #print(X_test_o.shape)  #(153638, 6)
    

    # split data to train and validataion
    indices = np.random.permutation(X_data_o.shape[0])
    X_data_title, X_data_descr, X_data_o, y_data = \
            X_data_title[indices], X_data_descr[indices], X_data_o[indices], y_data[indices]

    trainN = int(0.8 * X_data_o.shape[0])
    X_train_title = X_data_title[:trainN]
    X_val_title = X_data_title[trainN:]
    X_train_descr = X_data_descr[:trainN]
    X_val_descr = X_data_descr[trainN:]
    X_train_o = X_data_o[:trainN]
    X_val_o = X_data_o[trainN:]
    y_train = y_data[:trainN]
    y_val = y_data[trainN:]

    # normalize
    print('=== Normalizing')
    X_mean_title, X_std_title, X_train_normalized_title = normalize(X_train_title)
    X_val_normalized_title = normalize_given_m_s(X_val_title, X_mean_title, X_std_title)
    X_test_normalized_title = normalize_given_m_s(X_test_title, X_mean_title, X_std_title)

    X_mean_descr, X_std_descr, X_train_normalized_descr = normalize(X_train_descr)
    X_val_normalized_descr = normalize_given_m_s(X_val_descr, X_mean_descr, X_std_descr)
    X_test_normalized_descr = normalize_given_m_s(X_test_descr, X_mean_descr, X_std_descr)

    X_mean_o, X_std_o, X_train_normalized_o = normalize(X_train_o)
    X_val_normalized_o = normalize_given_m_s(X_val_o, X_mean_o, X_std_o)
    X_test_normalized_o = normalize_given_m_s(X_test_o, X_mean_o, X_std_o)

    global y_mean
    global y_std
    y_mean, y_std, y_train_normalized = normalize(y_train)
    y_val_normalized = normalize_given_m_s(y_val, y_mean, y_std)

    # model
    print('=== Training')
    batch_size = args.bs
    epochs = args.ep

    embeddings_index = load_glove()
    embedding_matrix_title = get_emb_matrix(embeddings_index, word_index_title)
    embedding_matrix_descr = get_emb_matrix(embeddings_index, word_index_descr)


    embedding_layer_title = Embedding(len(word_index_title) + 1,
                                EMBEDDING_DIM,
                                weights=[embedding_matrix_title],
                                input_length=MAX_SEQUENCE_TITLE,
                                trainable=False)

    embedding_layer_descr = Embedding(len(word_index_descr) + 1,
                                EMBEDDING_DIM,
                                weights=[embedding_matrix_descr],
                                input_length=MAX_SEQUENCE_DESCR,
                                trainable=False)

    sequence_input_title = Input(shape=(MAX_SEQUENCE_TITLE,), dtype='int32')
    embedded_sequences_title = embedding_layer_title(sequence_input_title)
    #embedded_sequences_title = K.print_tensor(embedded_sequences_title, message='embedded_sequences_title')
    #print(K.eval(embedded_sequences_title))
    x_title = Bidirectional(LSTM(40), input_shape=(MAX_SEQUENCE_TITLE, EMBEDDING_DIM))(embedded_sequences_title)

    sequence_input_descr = Input(shape=(MAX_SEQUENCE_DESCR,), dtype='int32')
    embedded_sequences_descr = embedding_layer_descr(sequence_input_descr)
    x_descr = Bidirectional(LSTM(40), input_shape=(MAX_SEQUENCE_DESCR, EMBEDDING_DIM))(embedded_sequences_descr)

    other_input = Input(shape=(X_data_o.shape[1],), dtype='float32')
    x = Concatenate()([other_input, x_title, x_descr])
    #x = Conv1D(128, 5, activation='relu')(x)
    #x = MaxPooling1D(5)(x)
    #x = Conv1D(128, 5, activation='relu')(x)
    #x = MaxPooling1D(5)(x)
    #x = Conv1D(128, 5, activation='relu')(x)
    #x = MaxPooling1D(35)(x)  # global max pooling
    #x = Flatten()(x)
    x = Dropout(0.1)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.1)(x)
    out = Dense(1, activation='relu')(x)
    model = Model(inputs=[other_input, sequence_input_title, sequence_input_descr], outputs=out)
    model.summary()

    opt = Adam(lr=args.lr, decay=1e-6)

    if args.loss == 'mape':
        model.compile(loss=mape_denormalized(y_mean, y_std), optimizer=opt)
    elif args.loss == 'mae':
        model.compile(loss=mae_denormalized(y_mean, y_std), optimizer=opt)

    callbacks = []
    #callbacks.append(EarlyStopping(monitor='val_loss', patience=100))

    if not os.path.exists('checkpoints'):
        os.makedirs('checkpoints')

    best_model_path = os.path.join('checkpoints', 'model_nn_emb_w_rnn_'+args.loss+'.h5')
    callbacks.append(ModelCheckpoint(best_model_path, monitor='val_loss', verbose=0, save_best_only=True))
    json_log = open(os.path.join('checkpoints', 'loss_log_nn_emb_w_rnn_'+args.loss+'.json'), mode='wt', buffering=1)
    json_logging_callback = LambdaCallback(
        on_epoch_end=lambda epoch, logs: json_log.write(
            json.dumps({'epoch': epoch, 'loss': logs['loss'], 'val_loss': logs['val_loss']}) + '\n'),
        on_train_end=lambda logs: json_log.close()
    )
    callbacks.append(json_logging_callback)

    model.fit([X_train_normalized_o, X_train_normalized_title, X_train_normalized_descr], y_train_normalized,
                  batch_size=batch_size,
                  epochs=epochs,
                  validation_data=([X_val_normalized_o, X_val_normalized_title, X_val_normalized_descr], y_val_normalized),
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
    predictions = model.predict([X_test_normalized_o, X_test_normalized_title, X_test_normalized_descr], batch_size=batch_size)
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

    output_path = os.path.join('outputs', 'subm_nn_emb_w_rnn_'+args.loss+'.csv')
    if args.loss == 'mape':
        np.savetxt(output_path, np.array(br_test_pred), fmt='%1.4f')
    elif args.loss == 'mae':
        np.savetxt(output_path, np.around(br_test_pred), fmt='%d')

if __name__ == '__main__':
    parse_args()
    main()

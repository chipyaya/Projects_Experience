''' MF(+DNN), NMF, SVD++
# MF
time python3 mf_hua.py --bs 1024 --emb_dim 16 --use_dnn 0 --dense_units 256 128 64 32 --ep 40 --lr 0.0001 --norm_ans 1 --loss mape
# MF+DNN
time python3 mf_hua.py --bs 1024 --emb_dim 16 --use_dnn 1 --dense_units 256 128 64 32 --ep 40 --lr 0.0001 --norm_ans 1 --loss mape
# NMF
time python3 mf_hua.py --bs 1024 --emb_dim 16 --use_dnn 0 --dense_units 256 128 64 32 --ep 40 --lr 0.0001 --norm_ans 1 --loss mape --nmf 1
# SVD++
time python3 mf_hua.py --bs 1024 --emb_dim 16 --use_dnn 0 --dense_units 256 128 64 32 --ep 40 --lr 0.0001 --norm_ans 1 --loss mape --use_implicit 1
'''

'''
If you do not want to use GPU
'''
#import os
#os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
#os.environ["CUDA_VISIBLE_DEVICES"] = ""

import re
import sys
import argparse
import pickle
import json
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from keras.models import Model
from keras.layers import Concatenate, Embedding, Dot, Reshape, Lambda
from keras.layers import Input, Add, Dropout, Dense, Flatten
from keras.initializers import Zeros
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
from keras.callbacks import LambdaCallback
from keras.constraints import non_neg
from keras.optimizers import Adam
from keras.preprocessing.sequence import pad_sequences
from keras.regularizers import l2
from keras.engine.topology import Layer
import keras.backend as K
from keras.backend.tensorflow_backend import set_session
import tensorflow as tf
from util import *


# GPU setting
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.2
set_session(tf.Session(config=config))

# Constant
seed = 7

def parse_args():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--bs', type=int, default=256, help='batch_size')
    parser.add_argument('--ep', type=int, default=10, help='epoch')
    parser.add_argument('--emb_dim', type=int, default=16, help='embedding_dim')
    parser.add_argument('--lr', type=float, default=1e-4, help='learning_rate')
    parser.add_argument('--loss', type=str, default='mae', help='loss: mae or mape')
    parser.add_argument('--use_dnn', type=int, default=0)
    parser.add_argument('--norm_ans', type=int, default=1)
    parser.add_argument('--use_implicit', type=int, default=0)
    parser.add_argument('--nmf', type=int, default=0)
    parser.add_argument('--dense_units', type=int, nargs='*')
    parser.add_argument('--only_test', type=int, default=0)
    args = parser.parse_args()

    if args.use_implicit and args.use_dnn:
        print('\nError: should not use implicit with dnn')
        sys.exit(1)



def get_feedback(user_all, book_all, user_num, book_num):
    feedback_u = [[] for u in range(user_num)]
    feedback_b = [[] for i in range(book_num)]

    for u, m in zip(user_all, book_all):
        feedback_u[u].append(m+1)
        feedback_b[m].append(u+1)

    return feedback_u, feedback_b

def load_best_model_and_predict(best_model_path, loss, self=0):
    # load best model
    model.load_weights(best_model_path)
    if args.norm_ans:
        if loss == 'mape':
            model.compile(loss=mape_denormalized(rate_mean, rate_std), optimizer=opt)
        elif loss == 'mae':
            model.compile(loss=mae_denormalized(rate_mean, rate_std), optimizer=opt)
    else:
        model.compile(loss=loss, optimizer=opt)

    # predict
    predictions = model.predict([user_test, book_test], batch_size=args.bs)
    print(predictions)
    if args.norm_ans:
        predictions = denormalize(predictions, rate_mean, rate_std)
        print(predictions)

    # Valid rating: 1, 2, ..., 10
    predictions[predictions > 10] = 10
    predictions[predictions < 1] = 1

    # write output
    if loss == 'mae':
        if self:
            output_path_round = os.path.join('outputs', 'subm_mf_'+out_filename_str+'_'+args.loss+'_round_self.csv')
        else:
            output_path_round = os.path.join('outputs', 'subm_mf_'+out_filename_str+'_'+args.loss+'_round.csv')
        np.savetxt(output_path_round, np.around(predictions), fmt='%d')
        print('Ouput written to %s' % output_path_round)

    if self:
        output_path_raw = os.path.join('outputs', 'subm_mf_'+out_filename_str+'_'+loss+'_raw_self.csv')
    else:
        output_path_raw = os.path.join('outputs', 'subm_mf_'+out_filename_str+'_'+loss+'_raw.csv')
    np.savetxt(output_path_raw, predictions, fmt='%1.4f')
    print('Ouput written to %s' % output_path_raw)

# For SVD++
class WeightedAvgOverTime(Layer):
    def __init__(self, **kwargs):
        self.supports_masking = True
        super(WeightedAvgOverTime, self).__init__(**kwargs)
   
    def call(self, x, mask=None):
        if mask is not None:
            mask = K.cast(mask, K.floatx())
            mask = K.expand_dims(mask, axis=-1)
            s = K.sum(mask, axis=1)
            if K.equal(s, K.zeros_like(s)) is None:
                return K.mean(x, axis=1)
            else:
                return K.cast(K.sum(x * mask, axis=1) / K.sqrt(s), K.floatx())
        else:
            return K.sum(x, axis=1)/K.sqrt(len(x))

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[-1])

    def compute_mask(self, x, mask=None):
        return None

    def get_config(self):
        base_config = super(WeightedAvgOverTime, self).get_config()
        return dict(list(base_config.items()))

def metrics_mape(rate_true, rate_pred):
    if args.norm_ans:
        rate_true = denormalize(rate_true, rate_mean, rate_std)
        rate_pred = denormalize(rate_pred, rate_mean, rate_std)
    diff = K.abs((rate_true - rate_pred) / K.clip(K.abs(rate_true),
					    K.epsilon(),
					    None))
    return 100. * K.mean(diff, axis=-1)

def metrics_mae(rate_true, rate_pred):
    if args.norm_ans:
        rate_true = denormalize(rate_true, rate_mean, rate_std)
        rate_pred = denormalize(rate_pred, rate_mean, rate_std)
    rate_true = K.round(rate_true)
    rate_pred = K.round(rate_pred)
    return K.mean(K.abs(rate_pred - rate_true), axis=-1)

if __name__ == '__main__':

    parse_args()
    np.random.seed(seed)

    # Load data
    user, book, user_test, book_test, rate, user_all, book_all, user_dict, book_dict = read_data()
    if args.norm_ans:
        rate_mean = 7.601225201958479 # mean of rate
        rate_std = 1.844145990351842 # std of rate
        rate = (rate - rate_mean) / rate_std

    rate_num = len(rate)
    user_num = len(user_dict)
    book_num = len(book_dict)

    if args.use_implicit:
        feedback_u, feedback_b = get_feedback(user_all, book_all, user_num, book_num)
        feedback_u, feedback_b = pad_sequences(feedback_u), pad_sequences(feedback_b)

    print('Data prepared')

    # Model
    u_input = Input(shape=[1], name='user')
    if not args.nmf:
        U = Embedding(user_num, args.emb_dim, input_length=1, embeddings_initializer="random_normal", name='user_embed')(u_input)
    else:
        U = Embedding(user_num, args.emb_dim, input_length=1, embeddings_initializer="random_normal", embeddings_constraint=non_neg(), name='user_embed')(u_input)

    U = Dropout(0.3)(U)
    U = Flatten()(U)

    b_input = Input(shape=[1], name='book')

    if not args.nmf:
        B = Embedding(book_num, args.emb_dim, input_length=1, embeddings_initializer="random_normal", name='book_embed')(b_input)
    else:
        B = Embedding(book_num, args.emb_dim, input_length=1, embeddings_initializer="random_normal", embeddings_constraint=non_neg(), name='book_embed')(b_input)

    B = Dropout(0.3)(B)
    B = Flatten()(B)

    U_bias = Embedding(user_num, 1, input_length=1, embeddings_initializer="zeros", name='user_embed_bias')(u_input)
    U_bias = Flatten()(U_bias)

    B_bias = Embedding(book_num, 1, input_length=1, embeddings_initializer="zeros", name='book_embed_bias')(b_input)
    B_bias = Flatten()(B_bias)

    if not args.use_dnn:
        if args.use_implicit:
            F_u = Reshape((feedback_u.shape[1],))(Embedding(user_num, feedback_u.shape[1], trainable=False, weights=[feedback_u])(u_input))
            F_u = Embedding(book_num+1, args.emb_dim, embeddings_initializer=Zeros(), embeddings_regularizer=l2(0.00001), mask_zero=True)(F_u)
            F_u = Dropout(0.1)(F_u)
            F_u = WeightedAvgOverTime()(F_u)

            U = Add()([U, F_u])
            
            #F_b = Reshape((feedback_b.shape[1],))(Embedding(book_num, feedback_b.shape[1], trainable=False, weights=[feedback_b])(b_input))
            #F_b = Embedding(user_num+1, args.emb_dim, embeddings_initializer=Zeros(), embeddings_regularizer=l2(0.00001), mask_zero=True)(F_b)
            #F_b = Dropout(0.1)(F_b)
            #F_b = WeightedAvgOverTime()(F_b)

            #B = Add()([B, F_b])
            
            pred = Dot(axes=-1)([U, B])

            pred = Add()([pred, U_bias, B_bias])
            pred = Lambda(lambda x: x + K.constant(rate_mean, dtype=K.floatx()))(pred)

        else:
            pred = Dot(axes=-1)([U, B])
            pred = Add()([pred, U_bias, B_bias])
    else:
        pred = Concatenate()([U, B])
        for units in args.dense_units:
            pred = Dense(units, activation='selu')(pred)
            pred = Dropout(0.1)(pred)

        if args.norm_ans:
            pred = Dense(1, activation='selu')(pred)
        else:
            pred = Dense(1)(pred)
        pred = Add()([pred, U_bias, B_bias])

    model = Model(inputs=[u_input, b_input], outputs=[pred])
    print(model.summary())

    out_filename_str = str(args.use_dnn)+'_'+str(args.use_implicit)+'_'+str(args.norm_ans)+'_argloss_'+args.loss
    best_model_path_mae = os.path.join('checkpoints', 'model_mf_'+out_filename_str+'_mae.h5')
    best_model_path_mape = os.path.join('checkpoints', 'model_mf_'+out_filename_str+'_mape.h5')
    best_model_path_self = os.path.join('checkpoints', 'model_mf_'+out_filename_str+'_self.h5')

    opt = Adam(lr=args.lr, decay=1e-6)

    if not args.only_test:
        if args.norm_ans:
            if args.loss == 'mape':
                model.compile(loss=mape_denormalized(rate_mean, rate_std), optimizer=opt, metrics=[metrics_mae, metrics_mape])
            elif args.loss == 'mae':
                model.compile(loss=mae_denormalized(rate_mean, rate_std), optimizer=opt, metrics=[metrics_mae, metrics_mape])
        else:
            model.compile(loss=args.loss, optimizer=opt, metrics=[metrics_mae, metrics_mape])


        if not os.path.exists('checkpoints'):
            os.makedirs('checkpoints')

        callbacks = []
        callbacks.append(ModelCheckpoint(best_model_path_mae, monitor='val_metrics_mae', verbose=0, save_best_only=True))
        callbacks.append(ModelCheckpoint(best_model_path_mape, monitor='val_metrics_mape', verbose=0, save_best_only=True))
        callbacks.append(ModelCheckpoint(best_model_path_self, monitor='val_loss', verbose=0, save_best_only=True))
        #callbacks.append(EarlyStopping(monitor='val_loss', patience=5))

        json_log = open(os.path.join('checkpoints', 'loss_log_mf_'+out_filename_str+'.json'), mode='wt', buffering=1)
        json_logging_callback = LambdaCallback(
            on_epoch_end=lambda epoch, logs: json_log.write(
                json.dumps({'epoch': epoch, 'loss': logs['loss'], 'val_loss': logs['val_loss']}) + '\n'),
            on_train_end=lambda logs: json_log.close()
        )
        callbacks.append(json_logging_callback)


        model.fit([user, book], rate, 
                batch_size=args.bs, 
                epochs=args.ep, 
                validation_split=0.2,
                callbacks=callbacks,
                shuffle=True)

    print('=== Predicting')
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    load_best_model_and_predict(best_model_path_mape, 'mape')
    load_best_model_and_predict(best_model_path_mae, 'mae')
    load_best_model_and_predict(best_model_path_self, args.loss, self=1)

    print('Done')

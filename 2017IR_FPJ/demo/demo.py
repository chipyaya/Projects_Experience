import sys
import argparse
import pickle
import numpy as np
import random as rd
from os import listdir
from os.path import isfile, join
from hanziconv import HanziConv
from keras import layers
from keras.datasets import imdb
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Flatten, Reshape, LSTM
from keras.layers.merge import Concatenate
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D 
from keras.layers.pooling import GlobalMaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.optimizers import Adam
import pickle
from hanziconv import HanziConv

def terms2Vec(terms):
    vec = np.zeros(len(embeddings[0]))
    for term in terms:
        ID = word2id.get(HanziConv.toSimplified(term)) 
        if ID == None:
            vec += embeddings[0]
        else:
            vec += embeddings[ID]
    vec /= len(terms)
    return vec

    
def getTrainingDataSenAvg(ptts, i):
    X = np.zeros((1000, len(embeddings[0])))
    y = []
    for j,terms in enumerate(ptts[i]['content']):
        X[j] = embeddings[startS]+terms2Vec(terms)+embeddings[endS]
        print(X[j])
        if ptts[i]['isSponsoredPost'] == True:
            y.append([1,0])
        else:
            y.append([0,1])
        y = np.asarray(y)
        return X, y



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--ptt_id')
    return parser.parse_args()


def countDistribution(y):
    isS_num, notS_num = 0, 0
    total_num = len(y)
    isS_index = []
    notS_index = []
    for i,y_prob in enumerate(y):
        if y_prob[0] == 1:
            isS_num += 1
            isS_index.append(i)
        elif y_prob[1] == 1:
            notS_num += 1
            notS_index.append(i)

    print('isS_num:', isS_num)
    print('notS_num', notS_num)
    print('isSponsered_ratio:', isS_num/total_num*100, '%')
    return isS_index, notS_index, isS_num, notS_num

def balanceData(X, y):
    isS_index, notS_index, isS_num, notS_num = countDistribution(y)
    sample_num = min(isS_num, notS_num)
    X_sample = np.zeros((sample_num+isS_num, X.shape[1], X.shape[2]))
    y_sample = np.zeros((sample_num+isS_num, y.shape[1]))
    i = 0
    for sample_i in rd.sample(notS_index, sample_num):
        X_sample[i] = X[sample_i]
        y_sample[i] = y[sample_i]
        i+=1
    for index in isS_index:
        X_sample[i] = X[index]
        y_sample[i] = y[index]
        i+=1

    print('X:', X.shape, X_sample.shape)
    print('y:', y.shape, y_sample.shape)
    return X_sample, y_sample

def trimBlog(labelledBlogs):
    for i,blog in enumerate(labelledBlogs):
        if len(blog['content']) > 1000:
            labelledBlogs[i]['content'] = blog['content'][:1000]
    return labelledBlogs


if __name__ == '__main__':

    args = parse_args()
    ptt_id = int(args.ptt_id)
    [blogs, ptts, X_train, y_train, X_valid, y_valid, embeddings] = pickle.load(open('../afterProcessing/small/blogs_ptts_sen.p', 'rb'))
    words, embeddings = pickle.load(open('../polyglot-zh.pkl', 'rb'), encoding='latin1')                                    
    word2id = { w:i for (i,w) in enumerate(words) }
    startS = word2id['<S>']
    endS = word2id['</S>']
    x, y = getTrainingDataSenAvg(ptts,ptt_id)
    print(ptts[ptt_id]['href'])
    #print(x,y)

    w_s = pickle.load(open('../activation.p', 'rb'))

    model2 = Sequential()
    layer_i = 0
    model2.add(Conv1D(filters=32, kernel_size=3, padding='same', activation='relu', input_shape=(X_train.shape[1], X_train.shape[2]), weights=w_s[layer_i], trainable=False))
    layer_i += 1

    for i in range(2-1):
        model2.add(Conv1D(filters=32, kernel_size=3, padding='same', activation='relu', weights=w_s[layer_i], trainable=False))
        layer_i += 1
        
    model2.add(MaxPooling1D(pool_size=2))
    model2.add(Dropout(0.25))
    model2.add(Flatten())
    layer_i += 3

    model2.add(Dropout(0.5))
    layer_i += 1
    model2.add(Dense(2, activation='softmax', weights=w_s[layer_i]))
    adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
    model2.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
    print('==word2vec')
    print(x.reshape(X_train[:1].shape))
    print('==label')
    print(y)
    X = x.reshape(X_train[:1].shape)
    pred = model2.predict(X)
    print('==pred')
    print(pred)

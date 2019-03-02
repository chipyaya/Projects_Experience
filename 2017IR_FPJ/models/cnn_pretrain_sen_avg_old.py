import sys
import argparse
import pickle
import numpy as np
import random as rd
from hanziconv import HanziConv
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
from sklearn.preprocessing import Normalizer

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--batch_size')
    parser.add_argument('-l', '--learning_rate')
    parser.add_argument('-e', '--epochs')
    parser.add_argument('-fn', '--filter_num')
    parser.add_argument('-fs', '--filter_size')
    parser.add_argument('-cn', '--conv_layer_num')
    parser.add_argument('-d1', '--dropout_prob1')
    parser.add_argument('-d2', '--dropout_prob2')
    parser.add_argument('-op', '--op')
    parser.add_argument('-sh', '--shuffle')
    parser.add_argument('-ad', '--addOneMoreDense')
    parser.add_argument('-dd', '--one_more_dense_dim')
    parser.add_argument('-gl', '--max_over_time_pooling')
    parser.add_argument('-ty', '--model_type')
    return parser.parse_args()

def terms2Vec(terms, word2id):
    vec = np.zeros(len(embeddings[0]))
    for term in terms:
        ID = word2id.get(HanziConv.toSimplified(term)) #Problem: Some terms are not pretrained, like '食记','咖哩','捷运'
        if ID == None:
            vec += embeddings[0]
        else:
            vec += embeddings[ID]
    vec /= len(terms)
    return vec
def balanceData(X, y):
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
    sample_num = isS_num
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

def getTestingData(blogs, word2id):
    X = np.zeros((len(blogs), 1000, len(embeddings[0])))
    y = []
    y_p = []
    for i in range(len(blogs)):
        for j,terms in enumerate(blogs[i]['content']):
            X[i][j] = embeddings[word2id['<S>']]+terms2Vec(terms, word2id)+embeddings[word2id['</S>']]

        y_p.append([blogs[i]['label']/5,1-blogs[i]['label']/5])
        if blogs[i]['label'] > 3:
            y.append([0,1])
        else:
            y.append([1,0])
    y = np.asarray(y)
    y_p = np.asarray(y)
    return X, y, y_p

def trimBlog(labelledBlogs):
    for i,blog in enumerate(labelledBlogs):
        if len(blog['content']) > 1000:
            labelledBlogs[i]['content'] = blog['content'][:1000]
    return labelledBlogs

if __name__ == '__main__':
    maxL = 4776
    if len(sys.argv) != 29:
        raise ValueError('Incorrect number of arguments')
    args = parse_args()

    batch_size = int(args.batch_size)#128
    learning_rate = float(args.learning_rate)#0.001
    epochs =int(args.epochs)#50

    filter_num = int(args.filter_num)#32
    filter_size = int(args.filter_size) #3
    #filter_size = list(map(int, args.filter_size.split(','))) #3,4,5
    conv_layer_num  =int(args.conv_layer_num)#2
    dropout_prob1 = float(args.dropout_prob1)#0.25
    dropout_prob2 = float(args.dropout_prob2)#0.5
    op=args.op
    if args.shuffle == 'T':
        shuffle = True
    elif args.shuffle == 'F':
        shuffle = False
    else:
        raise ValueError('Wrong arg: shuffle')

    if args.addOneMoreDense== 'T':
        addOneMoreDense = True
    elif args.addOneMoreDense == 'F':
        addOneMoreDense = False
    else:
        raise ValueError('Wrong arg: addOneMoreDense')
    one_more_dense_dim = int(args.one_more_dense_dim)#16
    if args.max_over_time_pooling == 'T':
        max_over_time_pooling = True
    elif args.max_over_time_pooling =='F':
        max_over_time_pooling = False
    else:
        raise ValueError('Wrong arg: max_over_time_pooling')

    np.random.seed(7)
    rd.seed(0)

    [blogs, ptts, X_train, y_train, X_valid, y_valid, embeddings] = pickle.load(open("../afterProcessing/small/blogs_ptts_sen.p", "rb" ))

    # Testing data
    newblogs = pickle.load(open( "../blogs.pickle", "rb" ))
    labelledBlogs = [newblogs[i] for i in range(len(newblogs)) if newblogs[i]['label'] != None and newblogs[i]['label'] != 0]
    labelledBlogs = trimBlog(labelledBlogs)
    words, embeddings = pickle.load(open('../polyglot-zh.pkl', 'rb'), encoding='latin1')
    word2id = { w:i for (i,w) in enumerate(words) }
    X_test, y_test, y_test_p = getTestingData(labelledBlogs, word2id)

    print('train:')#data, sentenceN, embedding size
    X_train_sample, y_train_sample = balanceData(X_train, y_train)


    if shuffle:
        shuffle_indices = np.random.permutation(np.arange(len(y_train_sample)))
        X_train_sample = X_train_sample[shuffle_indices]
        y_train_sample = y_train_sample[shuffle_indices]

    model_type = args.model_type
    model = Sequential()
    if model_type == 'cnn':
        model.add(Conv1D(filters=filter_num, kernel_size=filter_size, padding='same', activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])))

        for i in range(conv_layer_num-1):
            model.add(Conv1D(filters=filter_num, kernel_size=filter_size, padding='same', activation='relu'))
            
        if max_over_time_pooling:
            model.add(GlobalMaxPooling1D())
        else:
            model.add(MaxPooling1D(pool_size=2))
            model.add(Dropout(dropout_prob1))
            model.add(Flatten())

        if addOneMoreDense:
            model.add(Dense(one_more_dense_dim, activation='relu'))
    elif model_type == 'lstm':
        model.add(LSTM(32, input_shape=(X_train.shape[1], X_train.shape[2])))
    else:
        raise ValueError('model_type')

    model.add(Dropout(dropout_prob2))
    model.add(Dense(2, activation='softmax'))
    adam = Adam(lr=learning_rate, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)

    model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
    print(model.summary())
    print(X_train_sample.shape, y_train_sample.shape)
    model.fit(X_train_sample, y_train_sample, epochs=epochs, batch_size=batch_size)

    scores = model.evaluate(X_valid, y_valid, verbose=0)
    print("Loss:", scores[0])
    print("Accuracy:", scores[1])
    print("Test:")
    scores = model.evaluate(X_test, y_test, verbose=0)
    print("Loss:", scores[0])
    print("Accuracy:", scores[1])
    pred = model.predict(X_test, verbose=0)

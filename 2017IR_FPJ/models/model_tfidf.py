import sys
import argparse
from sklearn.metrics import log_loss
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
import pickle
import numpy as np
import random as rd
from os import listdir
def createTFIDF(blogs, ptts):
    n_doc = len(blogs) + len(ptts)

    # index1: term, index2: doc_id, entry: tf
    tfs = {}

    # index: term, entry: idf 
    idfs = {}

    # tf: f_{t,d} / len(d)
    for doc_id, article in enumerate(ptts):
        len_doc = 0
        if article != None:
            for line in article['content']:
                len_doc += len(line)
            appeared = set()
            for line in article['content']:
                for term in line:
                    if term not in tfs:
                        tfs[term] = np.zeros(n_doc)
                    tfs[term][doc_id] += (1 / len_doc)
                    if term not in appeared:
                        appeared.add(term)
                        if term not in idfs:
                            idfs[term] = 1
                        else:
                            idfs[term] += 1
        
    n_ptts = len(ptts)

    for doc_id, article in enumerate(blogs):
        len_doc = 0
        for line in article['content']:
            len_doc += len(line)
        appeared = set()
        for line in article['content']:
            for term in line:
                if term not in tfs:
                    tfs[term] = np.zeros(n_doc)
                tfs[term][doc_id + n_ptts] += (1 / len_doc)
                if term not in appeared:
                    appeared.add(term)
                    if term not in idfs:
                        idfs[term] = 1
                    else:
                        idfs[term] += 1

    dfs = idfs.copy()
    for k in idfs.keys():
        idfs[k] = np.log(n_doc / idfs[k])
    return tfs, idfs, dfs

def tfidf(doc_i, term):
    return tfs[term][doc_i] * idfs[term]

def selectFeatures(dfs, thre):
    vocab_list = []
    count = 0
    for k,v in dfs.items():
        if v > thre:
            vocab_list.append(k)
            count += 1
    print('thre', thre, 'len(dfs):', len(dfs))
    print('df>thred:', count)
    print('count', count, 'len(ptts):', len(ptts))
    print(count/len(dfs)*100, '%')
    return vocab_list


def getTrainingDataByTFIDF(ptts, vocab_list):
    X = np.zeros((len(ptts), len(vocab_list)))
    y = []
    for doc_i, doc in enumerate(ptts):
        if doc != None:
            for j,term in enumerate(vocab_list):
                X[doc_i][j] = tfidf(doc_i, term)
            if ptts[doc_i]['isSponsoredPost'] == True:
                y.append(0)
            else:
                y.append(1)
    y = np.asarray(y)
    return X, y

def getTestingDataByTFIDF(pttsL, blogs, vocab_list):
    X = np.zeros((len(blogs), len(vocab_list)))
    y = []
    y_p = []
    for doc_i, doc in enumerate(blogs):
        for j,term in enumerate(vocab_list):
            X[doc_i][j] = tfidf(doc_i+pttsL, term)
        if blogs[doc_i]['label'] > 3:
            y.append(0)
        else:
            y.append(1)
        y_p.append([blogs[doc_i]['label']/5, 1 - blogs[doc_i]['label']/5])

    y = np.asarray(y)
    y_p = np.asarray(y_p)
    return X, y, y_p

def countDistribution(y):
    isS_num, notS_num = 0, 0
    total_num = len(y)
    isS_index = []
    notS_index = []
    for i,y_prob in enumerate(y):
        if y_prob == 0:
            isS_num += 1
            isS_index.append(i) 
        elif y_prob == 1:
            notS_num += 1
            notS_index.append(i)

    #print('isS_num:', isS_num)
    #print('notS_num', notS_num)
    #print('isSponsered_ratio:', isS_num/total_num*100, '%')
    return isS_index, notS_index, isS_num, notS_num

def balanceData(X, y):
    isS_index, notS_index, isS_num, notS_num = countDistribution(y)
    sample_num = min(isS_num, notS_num)
    X_sample = np.zeros((sample_num+isS_num, X.shape[1]))
    y_sample = np.zeros(sample_num+isS_num)
    i = 0
    for sample_i in np.random.choice(notS_index, sample_num):
        X_sample[i] = X[sample_i]
        y_sample[i] = y[sample_i]
        i+=1
    for index in isS_index:
        X_sample[i] = X[index]
        y_sample[i] = y[index]
        i+=1

    #print('X:', X.shape, X_sample.shape)
    #print('y:', y.shape, y_sample.shape)
    return X_sample, y_sample

def shuffle(X_train_sample, y_train_sample):
    shuffle_indices = np.random.permutation(np.arange(len(y_train_sample)))
    return X_train_sample[shuffle_indices], y_train_sample[shuffle_indices]

def crossEntropy(ans_list, pred_list):
    ce = 0
    for ans,pred in zip(ans_list, pred_list):
        ce += -(ans[0]*np.log(pred[0])+ans[1]*np.log(pred[1]))
    return ce/len(ans_list)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dt', '--data_type', help='big, small')
    parser.add_argument('-th', '--thre', help='thre for feature selection according to dfs')
    parser.add_argument('-m', '--model_type', help='svc, nb, dt')
    parser.add_argument('-t', '--times', help='number of times to train')
    
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    np.random.seed(0)
    thre = int(args.thre)
    times = int(args.times)

    # blog data
    newblogs = pickle.load(open( "/tmp2/GorsachiusMelanolophus/blogs.pickle", "rb" ))
    labelledBlogs = [newblogs[i] for i in range(len(newblogs)) if newblogs[i]['label'] != None and newblogs[i]['label'] != 0]

    # Training and Validation data
    if args.data_type == 'small':
        filepath = "/tmp2/GorsachiusMelanolophus/afterProcessing/small/blogs_ptts_word.p"
        [blogs, ptts, X_train, y_train, X_valid, y_valid, embeddings] = pickle.load(open(filepath, "rb" ))
        # use labelledBlogs
        tfs, idfs, dfs = createTFIDF(labelledBlogs, ptts)
        vocab_list = selectFeatures(dfs, thre)
        X_train, y_train = getTrainingDataByTFIDF(ptts[:int(0.7*len(ptts))], vocab_list)
        X_valid, y_valid = getTrainingDataByTFIDF(ptts[int(0.7*len(ptts)):], vocab_list)
    elif args.data_type == 'big':
        [blogs, ptts] = pickle.load(open( "/tmp2/GorsachiusMelanolophus/afterProcessing/big/newBlogs_newPTTs_sen.p", "rb" ))
        [y_train, X_valid, y_valid, embeddings] = pickle.load(open( "/tmp2/GorsachiusMelanolophus/afterProcessing/big/newBlogs_newPTTs_sen_noXtrain.p", "rb" ))
        # use newblogs
        tfs, idfs, dfs = createTFIDF(labelledBlogs, ptts)
        vocab_list = selectFeatures(dfs, thre)
        path_S='/tmp2/GorsachiusMelanolophus/ptt_posts_new/sponsored/'
        sN = len(listdir(path_S))
        S_X, S_y = getTrainingDataByTFIDF(ptts[:sN], vocab_list)
        notS_X, notS_y = getTrainingDataByTFIDF(ptts[sN:], vocab_list)
        X_train, y_train = np.concatenate((S_X[:int(0.7*len(S_X))], notS_X[:int(0.7*len(notS_X))])), np.concatenate((S_y[:int(0.7*len(S_y))], notS_y[:int(0.7*len(notS_y))]))
        X_valid, y_valid = np.concatenate((S_X[int(0.7*len(S_X)):], notS_X[int(0.7*len(notS_X)):])), np.concatenate((S_y[int(0.7*len(S_y)):], notS_y[int(0.7*len(notS_y)):]))
    else:
        raise ValueError('Wrong arg: model_type')
    
    # Testing data
    X_test, y_test, y_test_p = getTestingDataByTFIDF(len(ptts), labelledBlogs, vocab_list)

    maxAcc_valid = (0,0)
    maxAcc_test = (0,0)
    for i in range(times):
        if args.model_type == 'svc':
            clf = SVC(kernel='linear')
            #clf = SVC(kernel='rbf')
        elif args.model_type == 'nb':
            clf = GaussianNB()
        elif args.model_type == 'dt':
            clf = DecisionTreeClassifier(random_state=0)
        elif args.model_type == 'lr':
            clf = LogisticRegression() 
        else:
            raise ValueError('Wrong arg: model_type')

        X_train_sample, y_train_sample  = balanceData(X_train, y_train)
        X_train_sample, y_train_sample  = shuffle(X_train_sample, y_train_sample)
        clf.fit(X_train_sample, y_train_sample)

        # predict by validation (ptt)
        pred = clf.predict(X_valid)
        acc = np.mean([1 if pred[i] == y_valid[i] else 0 for i in range(len(y_valid))])
        loss = log_loss(y_valid, pred)
        print('Validation loss,acc:', loss, acc)
        if acc > maxAcc_valid[1]:
            maxAcc_valid =  (loss, acc)
        # predict by testing data (blogs)
        pred = clf.predict(X_test)
        acc = np.mean([1 if pred[i] == y_test[i] else 0 for i in range(len(y_test))])
        loss = log_loss(y_test, pred)
        print('Testing loss,acc:', loss, acc)
        if acc > maxAcc_test[1]:
            maxAcc_test =  (loss,acc)
    print('valid:', maxAcc_valid)
    print('test:', maxAcc_test)

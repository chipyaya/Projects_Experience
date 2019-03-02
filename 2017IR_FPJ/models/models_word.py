import sys
import argparse
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
import pickle
import numpy as np
import random as rd

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
    sample_num = isS_num
    X_sample = np.zeros((sample_num+isS_num, X.shape[1]))
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

def rmOneHot(y):
    y_new = np.zeros(y.shape[0])
    for i,y in enumerate(y):
        if y[0] == 1:      #isSponsoredPost
            y_new[i] = 0
        else:
            y_new[i] = 1
    return y_new
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

def getTestingData(blogs, word2id):
    X = np.zeros((len(blogs), 1000, len(embeddings[0])))
    y = []
    for i in range(len(blogs)):
        for j,terms in enumerate(blogs[i]['content']):
            X[i][j] = embeddings[word2id['<S>']]+terms2Vec(terms, word2id)+embeddings[word2id['</S>']]

        y.append([blogs[i]['label']/5,1-blogs[i]['label']/5])
    y = np.asarray(y)
    return X, y

def trimBlog(labelledBlogs):
    for i,blog in enumerate(labelledBlogs):
        if len(blog['content']) > 1000:
            labelledBlogs[i]['content'] = blog['content'][:1000]
    return labelledBlogs

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-dt', '--data_type', help='big, small')
    parser.add_argument('-m', '--model_type', help='svc, nb, dt')
    parser.add_argument('-t', '--times', help='number of times to train')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    # Training and validation data
    if args.data_type == 'big':
        #[blogs, ptts] = pickle.load(open( "/tmp2/GorsachiusMelanolophus/afterProcessing/big/newBlogs_newPTTs_sen.p", "wb" ))
        [blogs_withPol, ptts_withImgPol] = pickle.load(open( "/tmp2/GorsachiusMelanolophus/blogs_withPol_ptts_withImgPol.pickle", "rb" ))
    elif args.data_type == 'small':
        [blogs, ptts, X_train, y_train, X_valid, y_valid, embeddings] = pickle.load(open("/tmp2/GorsachiusMelanolophus/afterProcessing/small/blogs_ptts_word.p", "rb" ))

    # Testing data
    newblogs = pickle.load(open( "/tmp2/GorsachiusMelanolophus/blogs.pickle", "rb" ))
    labelledBlogs = [newblogs[i] for i in range(len(newblogs)) if newblogs[i]['label'] != None and newblogs[i]['label'] != 0]
    labelledBlogs = trimBlog(labelledBlogs)
    words, embeddings = pickle.load(open('/tmp2/GorsachiusMelanolophus/polyglot-zh.pkl', 'rb'), encoding='latin1')
    word2id = { w:i for (i,w) in enumerate(words) }
    X_test, y_test = getTestingData(labelledBlogs, word2id)


    maxAcc = 0
    for i in range(times):
        if args.model_type == 'svc':
            #clf = SVC(kernel='linear')
            clf = SVC(kernel='rbf')
        elif args.model_type == 'nb':
            clf = GaussianNB()
        elif args.model_type == 'dt':
            clf = DecisionTreeClassifier(random_state=0)
        else:
            raise ValueError('Wrong arg: model_type')

        # balanceData
        X_train_sample, y_train_sample  = balanceData(X_train, y_train)
        # shuffle
        X_train_sample, y_train_sample  = shuffle(X_train_sample, y_train_sample)
        clf.fit(X_train_sample, y_train_sample)
        pred = clf.predict(X_valid)
        acc = np.mean([1 if pred[i] == y_valid[i] else 0 for i in range(len(y_valid))])
        print('Validation acc:', acc)
        if acc > maxAcc:
            maxAcc = acc
    print('maxAcc:', maxAcc)

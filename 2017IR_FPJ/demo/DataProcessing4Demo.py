import sys
import argparse
import pickle
import numpy as np
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

args = parse_args()
ptt_id = int(args.ptt_id)
[_, ptts, _, _, _, _, _] = pickle.load(open('../afterProcessing/small/blogs_ptts_sen.p', 'rb'))
words, embeddings = pickle.load(open('../polyglot-zh.pkl', 'rb'), encoding='latin1')                                    
word2id = { w:i for (i,w) in enumerate(words) }
startS = word2id['<S>']
endS = word2id['</S>']
x, y = getTrainingDataSenAvg(ptts,ptt_id)
print(ptts[ptt_id]['href'])
print(x,y)


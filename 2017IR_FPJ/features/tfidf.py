import pickle
import numpy as np


def createTFIDF(blogs, ptts):
    n_doc = len(blogs) + len(ptts)

    # index1: term, index2: doc_id, entry: tf
    tfs = {}

    # index: term, entry: idf 
    idfs = {}

    # tf: f_{t,d} / len(d)
    # idf: log(N/df)
    for doc_id, article in enumerate(ptts):
        len_doc = 0
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

    dfs = idfs
    for k in idfs.keys():
        idfs[k] = np.log(n_doc / idfs[k])
    return tfs, idfs, dfs

def tfidf(doc_id, term):
    return tfs[term][doc_id] * idfs[term]

if __name__ == '__main__':
    filepath = "filepath of blogs_ptts.p"
    [blogs, ptts, X_train, y_train, X_valid, y_valid, embeddings] = pickle.load(open(filepath, "rb" ))
    tfs, idfs, dfs = createTFIDF(blogs, ptts)

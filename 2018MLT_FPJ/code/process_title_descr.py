import pandas as pd
import numpy as np
import os
import re
import math
from collections import Counter
import pickle
import argparse
import sys
from util import *

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

MAX_SEQUENCE_TITLE = 40
MAX_SEQUENCE_DESCR = 200
MAX_NUM_WORDS = 10000
EMBEDDING_DIM = 100

PICKLE_DIR = '../pickles'
DATA_DIR = '../data'

def fill_book_char():
    # fillna with ''
    books['Book-Description'].fillna('', inplace=True)
    books['Publisher'].fillna('', inplace=True)

def preprocess_isbn(df):
    chars_to_remove = ['\\',',','.','#','(',')','"','/',' ','-','+','*',"'",':','=','>','<']
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    df['ISBN'] = df['ISBN'].apply(lambda s: re.sub(rx, '', s)).apply(lambda s: s.replace('o', '0'))
    return df

def tokenize(texts, texts_train, texts_test, max_len):
    tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
    tokenizer.fit_on_texts(texts)
    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))

    sequences_train = tokenizer.texts_to_sequences(texts_train)
    sequences_test = tokenizer.texts_to_sequences(texts_test)

    # pad with 0
    sequences_train = pad_sequences(sequences_train, maxlen=max_len, padding='post')
    sequences_test = pad_sequences(sequences_test, maxlen=max_len, padding='post')

    return word_index, sequences_train, sequences_test

def gen_feature_seq(t, br_t, books_t, seq_descr_t, seq_title_t):
    print('== gen_feature_seq:', t)
    br_t_filtered = br_t[br_t['ISBN'].isin(books_t['ISBN'].values)] 
    X_data = []
    y_data = []
    userID_list_test_filtered = []
    isbn_list_test_filtered = []

    index_list = []
    for i, row in enumerate(br_t_filtered.itertuples()):
        print(i, i/len(br_t_filtered))
        userID, ISBN = row[1], row[2]
        res = books_t[books_t['ISBN'] == ISBN]
        index_list.append(res.index[0])

        if t == 'train':
            y_data.append(row[3])
        elif t == 'test':
            userID_list_test_filtered.append(userID)
            isbn_list_test_filtered.append(ISBN)

    pickle.dump(index_list, open(os.path.join(PICKLE_DIR, 'index_list_'+t+'.p'), 'wb'))
    #index_list = pickle.load(open(os.path.join(PICKLE_DIR, 'index_list_'+t+'.p'), 'rb'))

    if t == 'test':
        pickle.dump([userID_list_test_filtered, isbn_list_test_filtered], open(os.path.join(PICKLE_DIR, 'userID_isbn_list_test_filtered.p'), 'wb'))

    X_data_title = seq_title_t[index_list]
    X_data_descr = seq_descr_t[index_list]

    if t == 'train':
        return X_data_title, X_data_descr, np.array(y_data)
    else:
        return X_data_title, X_data_descr

if __name__ == '__main__':
    ##### load data #####
    br_train = pd.read_csv(os.path.join(DATA_DIR, 'book_ratings_train.csv'))
    br_test = pd.read_csv(os.path.join(DATA_DIR, 'book_ratings_test.csv'))
    books = pd.read_csv(os.path.join(DATA_DIR, 'books.csv'))
    users = pd.read_csv(os.path.join(DATA_DIR, 'users.csv'))

    ##### preprocessing #####
    # books: Book-Description, Book-Title
    fill_book_char()

    # books: isbn
    br_train = preprocess_isbn(br_train)
    br_test = preprocess_isbn(br_test)
    books = preprocess_isbn(books)

    isbn_list_train = br_train['ISBN'].unique()
    isbn_list_test = br_test['ISBN'].unique()
    isbn_list_used = list(set(br_train['ISBN']).union(set(br_test['ISBN'])))

    print('== preprocess_isbn ==')
    print('# unique isbn in br_train:', len(isbn_list_train), '\t# reduced isbn after preprocessing =', 128932-len(isbn_list_train))
    print('# unique isbn in br_test:', len(isbn_list_test), '\t# reduced isbn after preprocessing =', 95592-len(isbn_list_test))
    print('# unique isbn in books:', len(books['ISBN'].unique()), '\t\t# reduced isbn after preprocessing =', 271379-len(books['ISBN'].unique()))

    ##### features #####
    books_filtered = books[books['ISBN'].isin(isbn_list_used)].reset_index()
    books_train = books[books['ISBN'].isin(isbn_list_train)].reset_index()
    books_test = books[books['ISBN'].isin(isbn_list_test)].reset_index()

    
    # books: Book-Author, Publisher
    # books: Book-Title, Book-Description

    print('== Book-Title ==')
    word_index_title, seq_train_title, seq_test_title = tokenize(books_filtered['Book-Title'], books_train['Book-Title'], books_test['Book-Title'], MAX_SEQUENCE_TITLE)

    print('== Book-Description ==')
    word_index_descr, seq_train_descr, seq_test_descr = tokenize(books_filtered['Book-Description'], books_train['Book-Description'], books_test['Book-Description'], MAX_SEQUENCE_DESCR)

    print(seq_train_title.shape)
    print(seq_test_title.shape)
    print(seq_train_descr.shape)
    print(seq_test_descr.shape)

    pickle.dump([word_index_title, seq_train_title, seq_test_title, word_index_descr, seq_train_descr, seq_test_descr], open(os.path.join(PICKLE_DIR, 'seq_train_test_title_descr.p'), 'wb'))
    print('seq_train_test_title_descr.p dumped')

    ##### gen_feature_seq ##### 
    X_data_title, X_data_descr, y_data = gen_feature_seq('train', br_train, books_train, seq_train_descr, seq_train_title)
    X_test_title, X_test_descr = gen_feature_seq('test', br_test, books_test, seq_test_descr, seq_test_title) 
    pickle.dump([X_data_title, X_data_descr, y_data, X_test_title, X_test_descr], open(os.path.join(PICKLE_DIR, 'title_descr_seq.p'), 'wb'))
    print(X_data_title.shape, X_data_descr.shape, y_data.shape)
    print(X_test_title.shape, X_test_descr.shape)
    print('Done')




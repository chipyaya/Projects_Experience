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

MAX_SEQUENCE_LENGTH = 300
MAX_NUM_WORDS = 10000
EMBEDDING_DIM = 100

PICKLE_DIR = '../pickles'
DATA_DIR = '../data'
GLOVE_DIR = '../glove'

def parse_args():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--process_title_descr', type=int, default=0, help='')
    parser.add_argument('--add_feature', type=int, default=0, help='')
    args = parser.parse_args()
    

def fill_user_age(method):
    print('== User Age ==')
    print('missing:', sum(users['Age'].isnull())/len((users)))
    print('mean:', users['Age'].mean())
    print('median:', users['Age'].median())
    if method == 'mean':
        users['Age'].fillna(users['Age'].mean(), inplace=True)
    elif method == 'median':
        users['Age'].fillna(users['Age'].median(), inplace=True)

def fill_book_char():
    # fillna with ''
    books['Book-Description'].fillna('', inplace=True)
    books['Publisher'].fillna('', inplace=True)

def fill_book_year(method):
    #books['Year-Of-Publication'] = books['Year-Of-Publication'].replace(1376, 0).replace(1378, 0)
    print('== Book Year-Of-Publication ==')
    print('missing:', len(books.loc[(books['Year-Of-Publication'] == 0) | (books['Year-Of-Publication'] > 2018), 'Year-Of-Publication'])/len(books))
    print('mean:', books['Year-Of-Publication'].mean())
    print('median:', books['Year-Of-Publication'].median())
    books.loc[(books['Year-Of-Publication'] == 0) | (books['Year-Of-Publication'] > 2018), 'Year-Of-Publication'] = np.nan
    if method == 'mean':
        books['Year-Of-Publication'].fillna(books['Year-Of-Publication'].mean(), inplace=True)
    elif method == 'median':
        books['Year-Of-Publication'].fillna(books['Year-Of-Publication'].median(), inplace=True)

def preprocess_isbn(df):
    chars_to_remove = ['\\',',','.','#','(',')','"','/',' ','-','+','*',"'",':','=','>','<']
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    df['ISBN'] = df['ISBN'].apply(lambda s: re.sub(rx, '', s)).apply(lambda s: s.replace('o', '0'))
    return df

def tokenize(texts, texts_train, texts_test):
    tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
    tokenizer.fit_on_texts(texts)
    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))

    sequences_train = tokenizer.texts_to_sequences(texts_train)
    sequences_test = tokenizer.texts_to_sequences(texts_test)
    return word_index, sequences_train, sequences_test

def emb_col_to_vec(embeddings_index, texts, texts_train, texts_test):
    word_index, sequences_train, sequences_test = tokenize(texts, texts_train, texts_test)
    embedding_matrix = get_emb_matrix(embeddings_index, word_index)
    vec_train = [np.sum([embedding_matrix[ind] for ind in seq], axis=0) if seq != [] else np.zeros(EMBEDDING_DIM) for seq in sequences_train]
    vec_test = [np.sum([embedding_matrix[ind] for ind in seq], axis=0) if seq != [] else np.zeros(EMBEDDING_DIM) for seq in sequences_test]
            
    return vec_train, vec_test


'''
avg_rating_author[author_name] = avg rating of author_name
avg_rating_publisher[publisher_name] = avg rating of publisher_name
'''
def get_avg_rating(label):
    g_label = books.groupby(label)

    rating_sum_cnt_of_isbn = br_train.groupby('ISBN')['Book-Rating'].agg(['sum','count']) #only br_train has rating
    isbn_list = list(rating_sum_cnt_of_isbn.index)
    avg_rating = {}
    nonzero_cnt = 0
    for name, g in g_label:
        avg_rating[name] = 0
        cnt = 0
        isbn_list_per_label = list(g['ISBN'])
        for isbn in isbn_list_per_label:
            if isbn in isbn_list:
                avg_rating[name] += rating_sum_cnt_of_isbn['sum'][isbn]
                cnt += rating_sum_cnt_of_isbn['count'][isbn]
        if cnt != 0:
            avg_rating[name] /= cnt
            nonzero_cnt += 1

    # fill 0 with mean
    if nonzero_cnt != 0:
        mean = sum(avg_rating.values()) / nonzero_cnt

    for k,v in avg_rating.items():
        if v == 0:
            avg_rating[k] = mean
    return avg_rating

def gen_feature_vec(t, br_t, books_t, vec_descr_t, vec_title_t):
    print('== gen_feature_vec:', t)
    br_t_filtered = br_t[br_t['ISBN'].isin(books_t['ISBN'].values)]

    X_data = []
    y_data = []
    userID_list_t_filtered = []
    isbn_list_t_filtered = []

    for i, row in enumerate(br_t_filtered.itertuples()):
        print(i, i/len(br_t_filtered))
        userID, ISBN = row[1], row[2]
        res = books_t[books_t['ISBN'] == ISBN]
        if args.process_title_descr:
            #Description,title
            vec = np.concatenate((vec_title_t[res.index[0]], vec_descr_t[res.index[0]]), axis=0)
        else:
            vec = []
            # users: age
            vec.append(users.loc[users['User-ID'] == userID, 'Age'].values[0])
            # books: Year-Of-Publication
            author_name = res['Book-Author'].values[0]
            publisher_name = res['Publisher'].values[0]
            vec.append(res['Year-Of-Publication'].values[0])
            # books: author avg rating
            vec.append(avg_rating_author[author_name])
            # books: publisher avg rating
            vec.append(avg_rating_publisher[publisher_name])
            # books: author freq
            vec.append(freq_author[author_name])
            # books: publisher freq
            vec.append(freq_publisher[publisher_name])
            # books: len of Book-Description
            vec.append(res['len-of-book-descr'].values[0])
            # books: len of Book-Title
            vec.append(res['len-of-book-title'].values[0])

            vec = np.array(vec)

        X_data.append(vec)

        userID_list_t_filtered.append(userID)
        isbn_list_t_filtered.append(ISBN)

        if t == 'train':
            y_data.append(row[3])

    pickle.dump([userID_list_t_filtered, isbn_list_t_filtered], open(os.path.join(PICKLE_DIR, 'userID_isbn_list_'+t+'_filtered.p'), 'wb'))

    if t == 'train':
        return np.array(X_data), np.array(y_data)
    elif t == 'test':
        return np.array(X_data)

def add_feature_vec(t, br_t, books_t, vec_descr_t, vec_title_t):
    print('== gen_feature_vec:', t)
    br_t_filtered = br_t[br_t['ISBN'].isin(books_t['ISBN'].values)]

    X_data = []
    userID_list_t_filtered = []
    isbn_list_t_filtered = []

    for i, row in enumerate(br_t_filtered.itertuples()):
        print(i, i/len(br_t_filtered))
        userID, ISBN = row[1], row[2]
        res = books_t[books_t['ISBN'] == ISBN]
        vec = []
        # books: len of Book-Description
        vec.append(res['len-of-book-descr'].values[0])
        # books: len of Book-Title
        vec.append(res['len-of-book-title'].values[0])

        X_data.append(np.array(vec))

        userID_list_t_filtered.append(userID)
        isbn_list_t_filtered.append(ISBN)

    pickle.dump([userID_list_t_filtered, isbn_list_t_filtered], open(os.path.join(PICKLE_DIR, 'userID_isbn_list_'+t+'_filtered.p'), 'wb'))

    return np.array(X_data)

if __name__ == '__main__':
    parse_args()
    ##### load data #####
    br_train = pd.read_csv(os.path.join(DATA_DIR, 'book_ratings_train.csv'))
    br_test = pd.read_csv(os.path.join(DATA_DIR, 'book_ratings_test.csv'))
    books = pd.read_csv(os.path.join(DATA_DIR, 'books.csv'))
    users = pd.read_csv(os.path.join(DATA_DIR, 'users.csv'))

    ##### preprocessing #####
    # users: Age
    fill_user_age('mean')

    # books: Book-Description, Book-Title
    fill_book_char()

    # books: Year-Of-Publication
    fill_book_year('mean')

    # books: Book-Author
    books['Book-Author'].fillna('', inplace=True)
    books['Book-Author'] = books['Book-Author'].apply(lambda s: s[1:] if s != '' and (s[0] == ' ' or s[0] == "'" or s[0] == ';') else s)
    books['Book-Author'] = books['Book-Author'].apply(lambda s: s[:-1] if s != '' and s[-1] == '"' else s)

    # books: len of Book-Description, Book-Title
    books['len-of-book-descr'] = books['Book-Description'].apply(lambda s: len(s))
    books['len-of-book-title'] = books['Book-Title'].apply(lambda s: len(s))

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

    
    pickle.dump(list(books_test['ISBN']), open(os.path.join(PICKLE_DIR, 'books_test_isbn_list.p'), 'wb'))
    print('books_test_isbn_list dumped')
    #sys.exit(0)
    

    # books: Book-Author, Publisher
    if args.add_feature:
        X_data, y_data, X_test = pickle.load(open(os.path.join(PICKLE_DIR, 'others_vec.p'), 'rb'))

        vec_title_train, vec_title_test = None, None
        vec_descr_train, vec_descr_test = None, None

        X_data_add = add_feature_vec('train', br_train, books_train, vec_descr_train, vec_title_train)
        X_test_add = add_feature_vec('test', br_test, books_test, vec_descr_test, vec_title_test)
        print(X_data_add.shape)
        print(X_test_add.shape)

        X_data_concat = np.concatenate((X_data, X_data_add), axis=1)
        X_test_concat = np.concatenate((X_test, X_test_add), axis=1)
        print(X_data_concat.shape)
        print(X_test_concat.shape)

        pickle.dump([X_data_concat, y_data, X_test_concat], open(os.path.join(PICKLE_DIR, 'others_vec_add.p'), 'wb'))
    else:
        if not args.process_title_descr:
            print('== Book-Author, Publisher ==')
            ## avg rating
            avg_rating_author = get_avg_rating('Book-Author')
            avg_rating_publisher = get_avg_rating('Publisher')

            ## freq
            '''
            freq_author[author_name]
            freq_publisher[publisher_name]
            '''
            freq_author = dict(Counter(books['Book-Author'].values))
            freq_publisher = dict(Counter(books['Publisher'].values))

            vec_title_train, vec_title_test = None, None
            vec_descr_train, vec_descr_test = None, None

        # books: Book-Title, Book-Description
        else:
            embeddings_index = load_glove()

            print('== Book-Title ==')
            vec_title_train, vec_title_test = emb_col_to_vec(embeddings_index, books_filtered['Book-Title'], books_train['Book-Title'], books_test['Book-Title'])
            print('== Book-Description ==')
            vec_descr_train, vec_descr_test = emb_col_to_vec(embeddings_index, books_filtered['Book-Description'], books_train['Book-Description'], books_test['Book-Description'])

        ##### gen_feature_vec ##### 

        X_data, y_data = gen_feature_vec('train', br_train, books_train, vec_descr_train, vec_title_train)
        print(X_data.shape, y_data.shape)
        X_test = gen_feature_vec('test', br_test, books_test, vec_descr_test, vec_title_test)
        print(X_test.shape)

        ##### dump to pickle ##### 
        if args.process_title_descr:
            pickle.dump([X_data,y_data,X_test], open(os.path.join(PICKLE_DIR, 'title_descr_vec.p'), 'wb'))
        else:
            pickle.dump([X_data,y_data,X_test], open(os.path.join(PICKLE_DIR, 'others_vec.p'), 'wb'))
    print('Done')




import os
import numpy as np
from keras import backend as K
from keras.optimizers import Adam

GLOVE_DIR = '../glove'
DATA_DIR = '../data'
EMBEDDING_DIM = 100

def normalize(a):
    mean = np.mean(a, axis=0)
    std = np.std(a, axis=0)
    return mean, std, (a-mean)/std

def normalize_given_m_s(a, mean, std):
    return (a-mean)/std

def denormalize(a, mean, std):
    return a * std + mean

def mape_denormalized(y_mean, y_std):
    def loss(y_true, y_pred):
        y_true = denormalize(y_true, y_mean, y_std)
        y_pred = denormalize(y_pred, y_mean, y_std)
        diff = K.abs((y_true - y_pred) / K.clip(K.abs(y_true),
                                                K.epsilon(),
                                                None))
        return 100. * K.mean(diff, axis=-1)
    return loss 

def mae_denormalized(y_mean, y_std):
    def loss(y_true, y_pred):
        y_true = denormalize(y_true, y_mean, y_std)
        y_pred = denormalize(y_pred, y_mean, y_std)
        return K.mean(K.abs(y_pred - y_true), axis=-1)
    return loss 

def load_glove():
    embeddings_index = {}
    f = open(os.path.join(GLOVE_DIR, 'glove.6B.100d.txt'))
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    print('== Glove\nFound %s word vectors.' % len(embeddings_index))
    return embeddings_index

def get_emb_matrix(embeddings_index, word_index):
    embedding_matrix = np.zeros((len(word_index) + 1, EMBEDDING_DIM))
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i] = embedding_vector
    return embedding_matrix

# Reduce some isbn noise => This helps!
def preprocess_isbn(df):
    chars_to_remove = ['\\',',','.','#','(',')','"','/',' ','-','+','*',"'",':','=','>','<']
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    df['ISBN'] = df['ISBN'].apply(lambda s: re.sub(rx, '', s)).apply(lambda s: s.replace('o', '0'))
    return df

def read_data():
    traindf = pd.read_csv(os.path.join(DATA_DIR, 'book_ratings_train.csv'))
    testdf = pd.read_csv(os.path.join(DATA_DIR, 'book_ratings_test.csv'))
    #implicit = pd.read_csv(os.path.join(DATA_DIR, 'implicit_ratings.csv'))

    traindf['test'] = 0
    testdf['test'] = 1

    df = pd.concat([traindf, testdf])

    df = preprocess_isbn(df)

    id2user = df['User-ID'].unique()
    id2book = df['ISBN'].unique()

    user_dict= {k: id for id, k in enumerate(id2user)}
    book_dict = {k: id for id, k in enumerate(id2book)}

    df['User-ID'] = df['User-ID'].apply(lambda x: user_dict[x])
    df['ISBN'] = df['ISBN'].apply(lambda x: book_dict[x])

    df_train = df.loc[df['test'] == 0]
    df_test = df.loc[df['test'] == 1]

    return df_train['User-ID'].values, df_train['ISBN'].values, df_test['User-ID'].values, df_test['ISBN'].values, df_train['Book-Rating'].values, df['User-ID'].values, df['ISBN'].values, user_dict, book_dict

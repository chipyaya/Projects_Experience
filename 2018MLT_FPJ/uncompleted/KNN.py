import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# Load data
DATA_DIR = 'data'
books = pd.read_csv(os.path.join(DATA_DIR, 'books.csv'))
print('books:', len(books))
users = pd.read_csv(os.path.join(DATA_DIR, 'users.csv'))
ratings = pd.read_csv(os.path.join(DATA_DIR, 'book_ratings_train.csv'))
test = pd.read_csv(os.path.join(DATA_DIR, 'book_ratings_test.csv'))
test['Book-Rating'] = [0]*len(test)
ratings_and_test = pd.concat([ratings, test])

print('ratings:', len(ratings_and_test))

combine_book_rating = pd.merge(ratings_and_test, books, on='ISBN', how='left')
columns = ['Year-Of-Publication','Publisher','Image-URL-S','Image-URL-M','Image-URL-L','Book-Description','Book-Author','Book-Title']
combine_book_rating = combine_book_rating.drop(columns, axis=1)
#print(combine_book_rating.head()) # User-ID   ISBN    Book-Rating Book-Title
print('combine (ratings & book left join):', len(combine_book_rating))

#combine_book_rating = combine_book_rating.dropna(axis=0, subset=['Book-Title'])

book_ratingCount = (combine_book_rating\
                    .groupby(by=['ISBN'])['Book-Rating'].count().reset_index()\
                    .rename(columns={'Book-Rating':'totalRatingCount'})\
                    [['ISBN', 'totalRatingCount']])
book_ratingCount.head() # ISBN  totalRatingCount
print('book_ratingCount (#ISBN that are ranked):', len(book_ratingCount))

rating_with_totalRatingCount = combine_book_rating.merge(book_ratingCount, left_on='ISBN'\
                                                         , right_on='ISBN', how='inner')
rating_with_totalRatingCount.head() #User-ID ISBN    Book-Rating totalRatingCount
print('rating_with_totalRatingCount (combine combine_book_rating & book_ratingCount):', len(rating_with_totalRatingCount))

#rating_with_totalRatingCount['totalRatingCount'].describe()
#rating_with_totalRatingCount['totalRatingCount'].quantile(np.arange(.9,1,.01))

popularity_threshold = 7
rating_popular_book = rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold').reset_index()
rating_popular_book = rating_popular_book[['User-ID','ISBN','Book-Rating']]
print(rating_popular_book.head()) #User-ID ISBN    Book-Rating totalRatingCount
print('rating_popular_book:', len(rating_popular_book))
import pickle
pickle.dump(rating_popular_book, open('rating_popular_book.p', 'wb'))
print('Done')
import sys
sys.exit(0)

'''
combined = rating_popular_book.merge(users, left_on='User-ID', right_on = 'User-ID', how = 'left')
combined.head() #User-ID    ISBN    Book-Rating Book-Title  totalRatingCount    Location    Age
print('combined (combine rating_popular_book & users:', len(combined))
us_canada_user_rating = combined[combined['Location'].str.contains('usa|canada')]
us_canada_user_rating = us_canada_user_rating.drop('Age', axis = 1)
us_canada_user_rating.head()
'''

print('==pivot')

rating_popular_book_pivot = rating_popular_book.pivot(index='ISBN', columns = 'User-ID', values = 'Book-Rating').fillna(0).astype('int32')

rating_popular_book_matrix = csr_matrix(rating_popular_book_pivot.values)
rating_popular_book_matrix.shape

#rating_popular_book_pivot.head()
print('rating_popular_book_pivot:', rating_popular_book_pivot.shape)

model_knn= NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(rating_popular_book_pivot)

def find_nearest_neighbor(isbn_test, uid_test):
    query_list = np.where(rating_popular_book_pivot.index.values == isbn_test)[0]
    if len(query_list) != 0:
        query_index = query_list[0]
    else:
        return 0

    distances, indices = model_knn.kneighbors(rating_popular_book_pivot.iloc[query_index, :].reshape(1,-1), n_neighbors=6)

    for i in range(0, len(distances.flatten())):
        if i == 0:
            print('Recommendations for {0}:{1}\n'.format(isbn_test, books.loc[books['ISBN'] == isbn_test]['Book-Title'].values))
        else:
            isbn = rating_popular_book_pivot.index[indices.flatten()[i]]
            print('{0}:{1}:{2}, with d = {3}'.format(\
                    i, isbn, books.loc[books['ISBN'] == isbn]['Book-Title'].values, distances.flatten()[i]))
            if uid_test in rating_popular_book_pivot.columns.values:
                print(rating_popular_book_pivot.loc[isbn, uid_test])
            else:
                print(0)
    return 1

print('==test')
br_test = pd.read_csv('data/book_ratings_test.csv')
for row in br_test.itertuples():
    isbn_test, uid_test = row[2], row[1]
    print(isbn_test, uid_test)
    ret = find_nearest_neighbor(isbn_test, uid_test)

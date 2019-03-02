import pandas as pd
import numpy as np
import re

def preprocess_isbn(df):
    chars_to_remove = ['\\',',','.','#','(',')','"','/',' ','-','+','*',"'",':','=','>','<']
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    df['ISBN'] = df['ISBN'].apply(lambda s: re.sub(rx, '', s)).apply(lambda s: s.replace('o', '0'))
    return df


def main():
    print('===load data')
    book_train = pd.read_csv('./data/book_ratings_train.csv')
    book_test = pd.read_csv('./data/book_ratings_test.csv')

    print('===preprocess_isbn')
    book_train = preprocess_isbn(book_train)
    book_test = preprocess_isbn(book_test)
    
    all_rating_mean = np.mean(book_train.iloc[:,2].values)
    
    sorted_train = {}
    for index, row in book_train.iterrows():
        if row['User-ID'] in sorted_train:
            sorted_train[row['User-ID']].append(row['Book-Rating'])
        else:
            sorted_train[row['User-ID']] = [row['Book-Rating']]
            
    sorted_train_isbn = {}
    for index, row in book_train.iterrows():
        if row['ISBN'] in sorted_train_isbn:
            sorted_train_isbn[row['ISBN']].append(row['Book-Rating'])
        else:
            sorted_train_isbn[row['ISBN']] = [row['Book-Rating']]

    ########## avg by user id -> avg by isbn #############
    mean_by_user_id_isbn_result = []
    for index, row in book_test.iterrows():
        if row['User-ID'] in sorted_train:
            mean_by_user_id_isbn_result.append(np.mean(sorted_train[row['User-ID']]))
        else :
            if row['ISBN'] in sorted_train_isbn:
                mean_by_user_id_isbn_result.append(np.mean(sorted_train_isbn[row['ISBN']]))
            else :
                mean_by_user_id_isbn_result.append(all_rating_mean)
                
                
    ###### avg by user id -> avg by isbn #############
    mean_by_user_id_file = open('./data/mean_by_user_isbn.txt', 'w')

    for mean_by_user_id in mean_by_user_id_isbn_result:
        inNumber = mean_by_user_id
        inNumberint = int(mean_by_user_id)
        if inNumber == inNumberint:
            mean_by_user_id_file.write("%d\n" % inNumberint)
        else:
            mean_by_user_id_file.write("%.4f\n" % inNumber)
    mean_by_user_id_file.close()
    
    
    
    
if __name__ == '__main__':
    main()
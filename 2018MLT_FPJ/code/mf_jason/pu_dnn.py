#0.6732
import sys
from keras.models import Model
from keras.layers import Concatenate, Embedding, Dot, Reshape, Input, Add, Dropout, Dense, Flatten, Lambda
import numpy as np
import keras
from keras.callbacks import ModelCheckpoint
import pickle
import keras.backend as K
from keras.constraints import non_neg
from keras.optimizers import Adam
import re
# global var
embedding_size = 16
# / global var
def metrics_mape(y_true, y_pred):
	y_true = (y_true + mean) * std
	y_pred = (y_pred + mean) * std
	diff = K.abs((y_true - y_pred) / K.abs(y_true))
	return 100. * K.mean(diff)
def metrics_mae(y_true, y_pred):
	y_true = (y_true + mean) * std
	y_pred = (y_pred + mean) * std
	y_t_f = K.flatten(y_true)
	y_p_f = K.flatten(y_pred)
	return K.mean((K.abs(y_t_f - y_p_f)))
def my_mape():
	def mape(y_true, y_pred):
		y_true = (y_true + mean) * std
		y_pred = (y_pred + mean) * std
		#K.clip(K.abs(y_true),K.epsilon(),None))
		diff = K.abs((y_true - y_pred) / K.abs(y_true))
		return 100. * K.mean(diff)
	return mape
def my_mae():
	def mae(y_true, y_pred):
		y_true = (y_true + mean) * std
		y_pred = (y_pred + mean) * std
		y_t_f = K.flatten(y_true)
		y_p_f = K.flatten(y_pred)
		return K.mean((K.abs(y_t_f - y_p_f)))
	return mae
def rmse(predict, groundTruth):
    return keras.backend.sqrt(keras.backend.mean(keras.backend.pow(groundTruth - predict, 2))) 

f = open('normalized_rate', 'rb')
rate = pickle.load(f)
f.close()
mean = 7.601225201958479 # mean of rate
std = 1.844145990351842 # std of rate

f = open('tokenized_user', 'rb')
user = pickle.load(f)
f.close()

f = open('tokenized_book', 'rb')
book = pickle.load(f)
f.close()

# input user's name, output integar
f = open('user_tokenizer', 'rb')
user_dict = pickle.load(f)
f.close()

# input book's name, output integar
f = open('book_tokenizer', 'rb')
book_dict = pickle.load(f)
f.close()

user_input = Input(shape=[1], name='user')
movie_input = Input(shape=[1], name='movie')
#user_dense = Dense(units=1, activation='sigmoid', kernel_regularizer=keras.regularizers.l2(0.001))(user_input)
user_embed = Embedding(embeddings_regularizer=keras.regularizers.l2(0.00001), embeddings_initializer="random_normal", output_dim=embedding_size, input_dim=len(user_dict), input_length=1, name='user_embed')(user_input)
movie_embed = Embedding(embeddings_regularizer=keras.regularizers.l2(0.00001), embeddings_initializer="random_normal", output_dim=embedding_size, input_dim=len(book_dict), input_length=1, name='movie_embed')(movie_input)
user_embed_add = Embedding(embeddings_regularizer=keras.regularizers.l2(0.00001), embeddings_initializer="zeros", output_dim=1, input_dim=len(user_dict), input_length=1, name='user_embed_add')(user_input)
movie_embed_add = Embedding(embeddings_regularizer=keras.regularizers.l2(0.00001), embeddings_initializer="zeros", output_dim=1, input_dim=len(book_dict), input_length=1, name='movie_embed_add')(movie_input)


user_drop = Dropout(0.3)(user_embed)
movie_drop = Dropout(0.3)(movie_embed)

user_vec = Flatten()(user_drop)#Reshape([embedding_size])(user_drop)
movie_vec = Flatten()(movie_drop)#Reshape([embedding_size])(movie_drop)
user_vec_add = Flatten()(user_embed_add)#Reshape([1])(user_embed_add)
movie_vec_add = Flatten()(movie_embed_add)#Reshape([1])(movie_embed_add)

#77805
#185816
#y = Dot(1, normalize=False)([user_vec, movie_vec])
y = Concatenate()([user_vec, movie_vec])
y = Dense(units=256, activation='sigmoid', kernel_regularizer=keras.regularizers.l2(0.00001))(y)
y = Dropout(0.1)(y)
y = Dense(units=128, activation='sigmoid', kernel_regularizer=keras.regularizers.l2(0.00001))(y)
y = Dropout(0.1)(y)
y = Dense(units=64, activation='sigmoid', kernel_regularizer=keras.regularizers.l2(0.00001))(y)
y = Dropout(0.1)(y)
y = Dense(units=32, activation='sigmoid', kernel_regularizer=keras.regularizers.l2(0.00001))(y)
y = Dropout(0.1)(y)
y = Dense(units=1, activation='sigmoid', kernel_regularizer=keras.regularizers.l2(0.00001))(y)
u = Add()([movie_vec_add, user_vec_add, y])
model = Model(inputs=[user_input, movie_input], outputs=u)

model.compile(loss=my_mae(), optimizer=Adam(), metrics=[metrics_mae])

print (model.summary())
check_points = ModelCheckpoint('mf_try.h5' , monitor='val_metrics_mae', save_best_only=True)

model.fit([user, book], rate, batch_size=4096, epochs=10, validation_split=0.09, callbacks=[check_points], shuffle=True)
#model.save("mf_no_validation.h5")

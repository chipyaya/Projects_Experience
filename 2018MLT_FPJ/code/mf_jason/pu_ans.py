import sys
from keras.models import load_model
import pickle
import numpy as np
import keras
from math import *
import keras.backend as K
from keras.preprocessing.sequence import pad_sequences
from keras.engine.topology import Layer
import os
import re
os.environ["CUDA_VISIBLE_DEVICES"]="-1" 
class WeightedAvgOverTime(Layer):
    def __init__(self, **kwargs):
        self.supports_masking = True
        super(WeightedAvgOverTime, self).__init__(**kwargs)
   
    def call(self, x, mask=None):
        if mask is not None:
            mask = K.cast(mask, K.floatx())
            mask = K.expand_dims(mask, axis=-1)
            s = K.sum(mask, axis=1)
            if K.equal(s, K.zeros_like(s)) is None:
                return K.mean(x, axis=1)
            else:
                return K.cast(K.sum(x * mask, axis=1) / (K.sqrt(s) + K.constant(1e-10, dtype=K.floatx())), K.floatx())
        else:
            print (x)
            return K.mean(x, axis=1)

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[-1])

    def compute_mask(self, x, mask=None):
        return None

    def get_config(self):
        base_config = super(WeightedAvgOverTime, self).get_config()
        return dict(list(base_config.items()))
def rmse(predict, groundTruth):
    return keras.backend.sqrt(keras.backend.mean(keras.backend.pow(groundTruth - predict, 2))) 

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
if(len(sys.argv) < 3):
	print ('usage : \npython3 pu_ans.py your_model.h5 result_file.csv\nthe result for track 1 will be named int_result_file.csv\nthe result for track 2 will be named result_file.csv')
	exit()

f = open('tokenized_test_user', 'rb')
user = pickle.load(f)
f.close()

f = open('tokenized_test_book', 'rb')
book = pickle.load(f)
f.close()
mean = 7.601225201958479 # mean of rate
std = 1.844145990351842 # std of rate
model = load_model(sys.argv[1], custom_objects={'rmse' : rmse, 'metrics_mae' : metrics_mae, 'metrics_mape' : metrics_mape, 'WeightedAvgOverTime' : WeightedAvgOverTime})
result_track2 = open(sys.argv[2], 'w')
result_track1 = open('int_' + sys.argv[2], 'w')
ans = model.predict([user, book])
ans = np.array(ans)
ans *= std
ans += mean
for i in range(len(ans)):
	now = ans[i][0]
	#now = ((((ans[i][0])) - mean_ans) / std_ans) + 7.4
	if(now > 10.0):
		now = 10.0
	elif(now < 0.0):
		now = 0.0
	result_track2.write("{0:.1f}".format(now) + '\n')
	result_track1.write("{0:1d}".format(int(round(now))) + '\n')
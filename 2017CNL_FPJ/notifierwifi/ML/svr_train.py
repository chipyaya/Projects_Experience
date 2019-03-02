import numpy as np
from sklearn.svm import SVR
import pickle
from math import sqrt

with open('train_data', 'r') as f:
	input_data = [[float(x) for x in line.lstrip().rstrip().split(' ')] for line in f]
input_data = np.array(input_data)

with open('validate_data', 'r') as f:
	validate_data = [[float(x) for x in line.lstrip().rstrip().split(' ')] for line in f]
validate_data = np.array(validate_data)


X = input_data[:, [2, 3, 4]]
Y = input_data[:, 0]
model_x = SVR()
model_x.fit(X, Y)
print('E_in of x:', sqrt(np.mean((model_x.predict(X)-Y)**2)))

X = input_data[:, [2, 3, 4]]
Y = input_data[:, 1]
model_y = SVR()
model_y.fit(X, Y)
print('E_in of y:', sqrt(np.mean((model_y.predict(X)-Y)**2)))

# validation
X = validate_data[:, [2, 3, 4]]
Y = validate_data[:, 0]
print('E_val of x:', sqrt(np.mean((model_x.predict(X)-Y)**2)))

X = validate_data[:, [2, 3, 4]]
Y = validate_data[:, 1]
print('E_val of y:', sqrt(np.mean((model_y.predict(X)-Y)**2)))


pickle.dump(model_x, open('svr_model_x', 'wb'))
pickle.dump(model_y, open('svr_model_y', 'wb'))

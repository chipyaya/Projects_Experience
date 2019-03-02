import numpy as np
from sklearn.svm import SVC
import pickle

def cases(x, y):
	if x >= 2.7:
		if y >= 1.8:
			return 0
		else:
			return 1
	else:
		if y >= 1.8:
			return 2
		else:
			return 3


with open('train_data', 'r') as f:
	input_data = [[float(x) for x in line.lstrip().rstrip().split(' ')] for line in f]
input_data = np.array(input_data)

X = input_data[:, [2, 3, 4]]
Y = np.array([cases(line[0], line[1]) for line in input_data])

model = SVC()
model.fit(X, Y)
print('E_in:', np.mean([1 if model.predict(X)[i] != Y[i] else 0 for i in range(len(Y))]))

with open('validate_data', 'r') as f:
	input_data = [[float(x) for x in line.lstrip().rstrip().split(' ')] for line in f]
input_data = np.array(input_data)

X = input_data[:, [2, 3, 4]]
Y = np.array([cases(line[0], line[1]) for line in input_data])

print('E_val:', np.mean([1 if model.predict(X)[i] != Y[i] else 0 for i in range(len(Y))]))

pickle.dump(model, open('svc_model', 'wb'))


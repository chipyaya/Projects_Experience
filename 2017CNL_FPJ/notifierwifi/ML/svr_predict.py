import sys
import numpy as np
import pickle
from sklearn import linear_model

if len(sys.argv) != 4:
	print('Usage :', sys.argv[0], 'signal_7 signal_12 signal_13')
	exit(1)

test = np.array([[float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])]])


model = pickle.load(open('ML/svr_model_x', 'rb'))
#print(model.predict(test)[0])
x = model.predict(test)[0]

model = pickle.load(open('ML/svr_model_y', 'rb'))
y = model.predict(test)[0]

sys.stderr.writelines(str(x)+' '+str(y))

if x >= 0.6 * 10:
    # on the right
    if y >= 0.6 * 1:
        print(0)
    else:
        print(1)
elif x >= 0.6 * 1:
    # in the middle
    if y >= 0.6 * 1:
        print(2)
    else:
        print(3)

else:
    # on the left
    if y >= 0.6 * 1:
        print(4)
    else:
        print(5)

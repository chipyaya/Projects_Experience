import os
import sys
sys.path.append(os.getcwd() + '/ML/libsvm/python')
print(os.getcwd() + '/ML/libsvm/python')
from svmutil import *

if len(sys.argv) != 4:
	print('Usage :', sys.argv[0], 'signal_7 signal_12 signal_13')
	exit(1)

x = [{i:float(sys.argv[i]) for i in range(1, 4)}]
y = [0]

print(x)

# predict coordinate x
m = svm_load_model('ML/model_x')
p_label, p_acc, p_val = svm_predict(y, x, m, '-q')
x = p_label[0]

# predict coordinate y
m = svm_load_model('ML/model_y')
p_label, p_acc, p_val = svm_predict(y, x, m, '-q')
y = p_label[0]

print(sys.argv, x, y)

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

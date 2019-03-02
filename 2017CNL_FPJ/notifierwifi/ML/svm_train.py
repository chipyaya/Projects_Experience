import sys
sys.path.append('libsvm/python')
from svmutil import *

if len(sys.argv) < 3:
	print('Usage :', sys.argv[0], 'train_data output_model [options]')
	exit(1)

opt = ''
for i in range(3, len(sys.argv)):
	opt = opt + sys.argv[i] + ' '

y, x = svm_read_problem(sys.argv[1])
m = svm_train(y, x, opt)
svm_predict(y, x, m)
svm_save_model(sys.argv[2], m)

import pickle
import sys
import re
import numpy as np
# movie means book :P
train = open(sys.argv[1], 'r', encoding='latin-1') # book_ratings_train.csv
test = open(sys.argv[2], 'r', encoding='latin-1') # book_ratings_test.csv
test.readline()
user_data = open(sys.argv[3], 'r', encoding='latin-1') # users.csv
user_data.readline()
train.readline()
user = []
movie = []
rate = []
ret = (lambda s: re.sub(rx, '', s))
ret2 = (lambda s: s.replace('o', '0'))
chars_to_remove = ['\\',',','.','#','(',')','"','/',' ','-','+','*',"'",':','=','>','<']
rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
while(1):
	jason = train.readline()
	if(not jason):
		break
	if(jason.find('\"') != -1):
		one = jason.find('\"')
		two = jason[one+1:].find('\"') + one + 1
		jason = jason[:one] + jason[one:two].replace(',', '') + jason[two:]
	see = jason.split(',')
	user.append((see[0]))
	movie.append((ret2(ret(see[1]))))
	rate.append(float(see[2].strip()))

test_user = []
test_movie = []
while(1):
	jason = test.readline()
	if(not jason):
		break
	if(jason.find('\"') != -1):
		one = jason.find('\"')
		two = jason[one+1:].find('\"') + one + 1
		jason = jason[:one] + jason[one:two].replace(',', '') + jason[two:]
	see = jason.split(',')
	test_user.append((see[0]))
	test_movie.append((ret2(ret(see[1].strip()))))


user_dict = dict()
rev_user_dict = dict() # not used
movie_dict = dict()
rev_movie_dict = dict() # not used
user_now = 0
for u in user:
	if(not u in user_dict):
		user_dict[u] = user_now
		rev_user_dict[user_now] = u
		user_now += 1
for i in range(len(test_user)):
	if(not test_user[i] in user_dict):
		user_dict[test_user[i]] = user_now
		rev_user_dict[user_now] = test_user[i]
		test_user[i] = user_now
		user_now += 1
	else:
		test_user[i] = user_dict[user[i]]
movie_now = 0
for m in movie:
	if(not m in movie_dict):
		movie_dict[m] = movie_now
		rev_movie_dict[movie_now] = u
		movie_now += 1
for i in range(len(test_movie)):
	if(not test_movie[i] in movie_dict):
		movie_dict[test_movie[i]] = movie_now
		rev_movie_dict[movie_now] = test_movie[i]
		test_movie[i] = movie_now
		movie_now += 1
	else:
		test_movie[i] = movie_dict[movie[i]]


for i in range(len(user)):
	user[i] = user_dict[user[i]]
for i in range(len(movie)):
	movie[i] = movie_dict[movie[i]]

user = np.array(user)
movie = np.array(movie)
rate = np.array(rate)
mean = np.mean(rate)
std = np.std(rate)
rate -= mean
rate /= std


rng_state = np.random.get_state()
np.random.shuffle(user)
np.random.set_state(rng_state)
np.random.shuffle(movie)
np.random.set_state(rng_state)
np.random.shuffle(rate)


f = open('normalized_rate', 'wb')
pickle.dump(rate, f)
f.close()
f = open('tokenized_user', 'wb')
pickle.dump(user, f)
f.close()
f = open('tokenized_book', 'wb')
pickle.dump(movie, f)
f.close()
f = open('user_tokenizer', 'wb')
pickle.dump(user_dict, f)
f.close()
f = open('book_tokenizer', 'wb')
pickle.dump(movie_dict, f)
f.close()
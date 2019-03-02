import sys
import argparse
import jieba
import jieba.analyse
from os import listdir
import pickle
import numpy as np
from hanziconv import HanziConv

def setExternelDicts():
    jieba.set_dictionary('./external/dict.txt.big')
    jieba.analyse.set_stop_words('./external/stop_words.txt')
    jieba.analyse.set_idf_path("./external/idf.txt.big")
    
def cutSentence(sentences):
    return [list(jieba.cut(sentence, cut_all=False)) for sentence in sentences.split(' ')]
    
def rmStopWords(sentences):
    for sentence in sentences:
        for term in sentence:
            if term in stopwords:
                sentence.remove(term)
        if sentence == []:
            sentences.remove(sentence)
    return sentences

def processString(string):
    return rmStopWords(cutSentence(' '.join(re.findall(r'[\u4e00-\u9fff]+', string))))

def processTitle(title):
    return processString(title)

def processContent(content):
    return processString(content)

def processComment(comments):
    for i, comment in enumerate(comments):
        comments[i] = processString(comment)
    return comments

def processTag(tag):
    tag_list = []
    tags = tag.split(',')
    for t in tags:
        t = re.findall(r'[\u4e00-\u9fff]+', t)
        tag_list+=t
    return tag_list

def processUrl(url):
    return re.sub(r'[\n]', '', url)

def processPush(push_list):
    return [processString(push) for push in push_list]

def processBlogs(path):
    filenames = [f for f in listdir(path)]
    blogs = []
    for filename in filenames:
        doc = pickle.load(open( path+filename, "rb" ))
        doc['title'] = processTitle(doc['title'])
        doc['comment'] = processComment(doc['comment'])
        doc['content'] = processContent(doc['content'])
        if 'tag' in doc.keys():
            doc['tag'] = processTag(doc['tag'])
            if doc['tag'] != []:
                firstTag = ' '.join(list(jieba.cut(doc['tag'][0], cut_all=False)))

                cutIndex = len(doc['content'])
                for i in range(len(doc['content'])-1, -1, -1):
                    if doc['content'][i] == firstTag:
                        cutIndex = i
                        break
                doc['content'] = doc['content'][:cutIndex]

        doc['url'] = processUrl(doc['url'])
        blogs.append(doc)
    return blogs

def processOldPtts():
    path='/tmp2/GorsachiusMelanolophus/ptt_posts_old/'
    filenames = [f for f in listdir(path)]
    ptts = []
    for i, filename in enumerate(filenames):
        doc = pickle.load(open( path+filename, "rb" ))
        doc['href'] = 'https://www.ptt.cc' + doc['href']
        doc['title'] = processTitle(doc['title'])
        doc['content'] = processContent(doc['content'])
        cutIndex = len(doc['content'])
        for i in range(len(doc['content'])-1, -1, -1):
            if '轉錄' in doc['content'][i]:
                cutIndex = i
        doc['content'] = doc['content'][:cutIndex]
        doc['push_contents'] = processPush(doc['push_contents'])
        ptts.append(doc)
    return ptts

def processNewPtts():
    path_S='/tmp2/GorsachiusMelanolophus/ptt_posts_new/sponsored/'
    path_notS='/tmp2/GorsachiusMelanolophus/ptt_posts_new/no_sponsored/'
    
    filenames_S = [f for f in listdir(path_S)]
    filenames_notS = [f for f in listdir(path_notS)]
    ptts = [None]*(len(filenames_S)+len(filenames_notS))
    for i, filename in enumerate(filenames_S):
        if filename == 'test.py':
            continue
        doc = pickle.load(open( path_S+filename, "rb" ))
        doc['href'] = 'https://www.ptt.cc' + doc['href']
        doc['title'] = processTitle(doc['title'])
        doc['content'] = processContent(doc['content'])
        cutIndex = len(doc['content'])
        for i in range(len(doc['content'])-1, -1, -1):
            if '轉錄' in doc['content'][i]:
                cutIndex = i
        doc['content'] = doc['content'][:cutIndex]
        doc['push_contents'] = processPush(doc['push_contents'])
        ptts[int(filename[:-2])] = doc
    for i, filename in enumerate(filenames_notS):
        doc = pickle.load(open( path_notS+filename, "rb" ))
        doc['href'] = 'https://www.ptt.cc' + doc['href']
        doc['title'] = processTitle(doc['title'])
        doc['content'] = processContent(doc['content'])
        cutIndex = len(doc['content'])
        for i in range(len(doc['content'])-1, -1, -1):
            if '轉錄' in doc['content'][i]:
                cutIndex = i
        doc['content'] = doc['content'][:cutIndex]
        doc['push_contents'] = processPush(doc['push_contents'])
        ptts[len(filenames_S)+int(filename[:-2])] = doc
    return ptts

def terms2VecIDs(terms):
    ans = []
    for term in terms:
        ID = word2id.get(HanziConv.toSimplified(term)) #Problem: Some terms are not pretrained, like '食记','咖哩','捷运'
        if ID == None:
            ans.append(0)
        else:
            ans.append(ID)
    return ans

def terms2Vec(terms):
    vec = np.zeros(len(embeddings[0]))
    for term in terms:
        ID = word2id.get(HanziConv.toSimplified(term)) #Problem: Some terms are not pretrained, like '食记','咖哩','捷运'
        if ID == None:
            vec += embeddings[0]
        else:
            vec += embeddings[ID]
    vec /= len(terms)
    return vec

def padding(vecIDs):
    vecIDs = vecIDs[:maxL]
    return vecIDs + [pad] * (maxL - len(vecIDs))

def getTrainingDataWord(ptts):
    X = []
    y = []
    for i in range(len(ptts)):
        vecIDs = []
        for terms in ptts[i]['content']:
            vecIDs += [startS]+terms2VecIDs(terms)+[endS]
        X.append(np.asarray(padding(vecIDs)))
        if ptts[i]['isSponsoredPost'] == True:
            y.append([1,0])
        else:
            y.append([0,1])
    X = np.asarray(X)
    y = np.asarray(y)
    return X, y

def getTrainingDataSenAvg(ptts):
    X = np.zeros((len(ptts), max_sentences_num, len(embeddings[0])))
    y = []
    for i in range(len(ptts)):
        try:
            for j,terms in enumerate(ptts[i]['content']):
                X[i][j] = embeddings[startS]+terms2Vec(terms)+embeddings[endS]
            if ptts[i]['isSponsoredPost'] == True:
                y.append([1,0])
            else:
                y.append([0,1])
        except:
            pass
    y = np.asarray(y)
    return X, y
            
'''
def getTestingData(blogs):
    X = np.zeros((len(blogs), max_sentences_num, len(embeddings[0])))
    y = []
    for i in range(len(blogs)):
        for j,terms in enumerate(blogs[i]['content']):
            X[i][j] = embeddings[startS]+terms2Vec(terms)+embeddings[endS]
        X.append(np.asarray(padding(vecIDs)))
    return X, y
'''


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-pt', '--parse_type', help='word or seg')
    parser.add_argument('-dt', '--data_type', help='big or small')
    return parser.parse_args()


# if __name__ == '__main__':
if len(sys.argv) != 5:
    raise ValueError('Incorrect number of arguments')
args = parse_args()
max_sentences_num = 1000
setExternelDicts()
stopwords = [line.rstrip('\n') for line in open('./external/stopwords-zh.txt')]

if args.data_type == 'big':
    blogs = processBlogs('/tmp2/ten/new_post_pickles/')
    ptts = processNewPtts()
elif args.data_type == 'small':
    blogs = processBlogs('/tmp2/GorsachiusMelanolophus/post_pickles/')
    ptts = processOldPtts()


# --------- Load word embedding --------- #
words, embeddings = pickle.load(open('/tmp2/eee/polyglot-zh.pkl', 'rb'), encoding='latin1')
print ('%d Zh word embeddings are loaded.' % len(words))
word2id = { w:i for (i,w) in enumerate(words) }
startS = word2id['<S>']
endS = word2id['</S>']
pad = word2id['<PAD>']
maxL = 4776


if args.data_type == 'big':
    path_S='/tmp2/GorsachiusMelanolophus/ptt_posts_new/sponsored/'
    sN = len(listdir(path_S))
    if args.parse_type == 'word':
        S_X, S_y = getTrainingDataWord(ptts[:sN])
        notS_X, notS_y = getTrainingDataWord(ptts[sN:])
    elif args.parse_type == 'sen':
        S_X, S_y = getTrainingDataSenAvg(ptts[:sN])
        notS_X, notS_y = getTrainingDataSenAvg(ptts[sN:])
    else:
        raise ValueError('Incorrect parse_type')
    X_train, y_train = np.concatenate((S_X[:int(0.7*len(S_X))], notS_X[:int(0.7*len(notS_X))])), np.concatenate((S_y[:int(0.7*len(S_y))], notS_y[:int(0.7*len(notS_y))]))
    X_valid, y_valid = np.concatenate((S_X[int(0.7*len(S_X)):], notS_X[int(0.7*len(notS_X)):])), np.concatenate((S_y[int(0.7*len(S_y)):], notS_y[int(0.7*len(notS_y)):]))
    pickle.dump([blogs, ptts], open( "/tmp2/GorsachiusMelanolophus/afterProcessing/big/newBlogs_newPTTs_"+str(args.parse_type)+".p", "wb" ))

    pickle.dump([X_train[:int(len(ptts)/2)]], open( "/tmp2/GorsachiusMelanolophus/afterProcessing/big/newBlogs_newPTTs_"+str(args.parse_type)+"_train1.p", "wb" ))
    pickle.dump([X_train[int(len(ptts)/2):]], open( "/tmp2/GorsachiusMelanolophus/afterProcessing/big/newBlogs_newPTTs_"+str(args.parse_type)+"_train2.p", "wb" ))

    pickle.dump([y_train, X_valid, y_valid, embeddings], open( "/tmp2/GorsachiusMelanolophus/afterProcessing/big/newBlogs_newPTTs_"+str(args.parse_type)+"_noXtrain.p", "wb" ))

elif args.data_type == 'small':
    if args.parse_type == 'word':
        X_train, y_train = getTrainingDataWord(ptts[:int(0.7*len(ptts))])
        X_valid, y_valid = getTrainingDataWord(ptts[:int(0.7*len(ptts))])
    elif args.parse_type == 'sen':
        X_train, y_train = getTrainingDataSenAvg(ptts[int(0.7*len(ptts)):])
        X_valid, y_valid = getTrainingDataSenAvg(ptts[int(0.7*len(ptts)):])
    else:
        raise ValueError('Incorrect parse_type')
    pickle.dump([blogs, ptts, X_train, y_train, X_valid, y_valid, embeddings], open( "/tmp2/GorsachiusMelanolophus/afterProcessing/small/blogs_ptts_"+str(args.parse_type)+".p", "wb" ))

else:
    raise ValueError('Incorrect data_type')

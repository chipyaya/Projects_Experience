from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET
import pickle

# Read all files to a list of dictionary and them dump to a pickle file
if __name__ == '__main__':
    path='/tmp2/GorsachiusMelanolophus/posts/simplified_doc'
    filenames = [f for f in listdir(path)]
    docs = []
    for filename in filenames:
        tree = ET.parse('/tmp2/GorsachiusMelanolophus/posts/simplified_doc/'+filename)
        root = tree.getroot()
        doc = {}
	if filename[-5] == '-':
            doc['id'] = int(filename[3:-5])
        elif filename[-6:-4] == '-%':
            doc['id'] = int(filename[3:-6])
        else:
            doc['id'] = int(filename[3:-4])
        doc['id'] = int(filename[3:-4])
        doc['title'] = root[0].text
        doc['content'] = root[1].text
        doc['tag'] = root[2].text
        doc['url'] = root[3].text
        docs.append(doc)
    pickle.dump(docs, open( "save.p", "wb" ))

    

from PIL import Image
import numpy as np
import pickle
import os
import sys
import cv2
from face_detect import face_detect


in_path = '/tmp2/GorsachiusMelanolophus/ptt_imgs/' + sys.argv[1]
out_path = '/tmp2/GorsachiusMelanolophus/ptt_imgs_feature/' + sys.argv[1]
if 'no_sponsored' in sys.argv[1]:
    img_num = pickle.load(open(f'img_num_no_sponsored.p', 'rb'))
else:
    img_num = pickle.load(open(f'img_num_sponsored.p', 'rb'))

for i in range(int(sys.argv[2]), int(sys.argv[3])):
    dir_path = f'{in_path}{i}/'
    img_feature = {}
    img_feature['img_num'] = img_num[i]
    img_feature['face'] = []
    img_feature['sharpness'] = []
    if os.path.isdir(dir_path):
        for img_path in os.listdir(dir_path):
            try:
                img_path = dir_path + img_path
                img = cv2.imread(img_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                #im = Image.open(img_path).convert('L')
                array = np.asarray(img, dtype=np.int32)
                dx = np.diff(array)[1:,:] # remove the first row
                dy = np.diff(array, axis=0)[:,1:] # remove the first column
                dnorm = np.sqrt(dx**2 + dy**2)
                sharpness = float(np.average(dnorm))
                img_feature['sharpness'].append(sharpness)
                face = face_detect(img)
                img_feature['face'].append(face)
            except Exception as e:
                print(e)
                pass
    pickle.dump(img_feature, open(f'{out_path}{i}.p', 'wb'))

from os import listdir
import pickle


def addImgFeature(ptts):
    path_S='/tmp2/GorsachiusMelanolophus/ptt_imgs_feature/sponsored/'
    path_notS='/tmp2/GorsachiusMelanolophus/ptt_imgs_feature/no_sponsored/'
    
    filenames_S = [f for f in listdir(path_S)]
    filenames_notS = [f for f in listdir(path_notS)]
    for i, filename in enumerate(filenames_S):
        img_data = pickle.load(open( path_notS+filename, "rb" ))
        ptts[int(filename[:-2])]['face'] = img_data['face']
        ptts[int(filename[:-2])]['img_num'] = img_data['img_num']
        ptts[int(filename[:-2])]['sharpness'] = img_data['sharpness']
    for i, filename in enumerate(filenames_notS):
        img_data = pickle.load(open( path_notS+filename, "rb" ))
        ptts[len(filenames_S)+int(filename[:-2])]['face'] = img_data['face']
        ptts[len(filenames_S)+int(filename[:-2])]['img_num'] = img_data['img_num']
        ptts[len(filenames_S)+int(filename[:-2])]['sharpness'] = img_data['sharpness']
    return ptts

if __name__ == '__main__':
    [blogs, ptts] = pickle.load(open( "/tmp2/GorsachiusMelanolophus/afterProcessing/big/newBlogs_newPTTs_sen.p", "rb" ))
    ptts_withImgData = addImgFeature(ptts)
    #pickle.dump([blogs, ptts_withImgData], open( "/tmp2/GorsachiusMelanolophus/afterProcessing/big/newBlogs_newPTTsWithImgData_sen.p", "wb" ))


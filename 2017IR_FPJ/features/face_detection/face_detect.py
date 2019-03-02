# coding: utf-8
import cv2

face = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

settings = {
    'scaleFactor': 1.2,
    'minNeighbors': 3,
    'minSize': (85, 85)
}

def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def face_detect(img):

    faces = face.detectMultiScale(img, **settings)
    if len(faces):
        return True
    else:
        return False
"""
    for angle in [0, -10, 10]:
        rimg = rotate_image(img, angle)
        detected = face.detectMultiScale(rimg, **settings)
        if len(detected):
            return True
        else:
            return False
"""

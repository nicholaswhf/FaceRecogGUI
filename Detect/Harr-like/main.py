import cv2,sys
import numpy as np
import  keras
from keras.models import load_model
#import train 
import h5py
# 加载级联分类器模型：
CASE_PATH = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(CASE_PATH)

def resize_without_deformation(image, size=(100, 100)):
    height, width, _ = image.shape
    longest_edge = max(height, width)

    top, bottom, left, right = 0, 0, 0, 0

    if height < longest_edge:

        height_diff = longest_edge - height

        top = int(height_diff / 2)

        bottom = height_diff - top
    elif width < longest_edge:

        width_diff = longest_edge - width

        left = int(width_diff / 2)

        right = width_diff - left


    image_with_border = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])


    resized_image = cv2.resize(image_with_border, size)


    return resized_image


# In[3]:


# 打开摄像头，获取图片并灰度化：
cap = cv2.VideoCapture(0) 
#ret, image = cap.read()
route=sys.argv[1]
image = cv2.imread(route)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
print("########################################")


# In[4]:


# 人脸检测：
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2,
                                minNeighbors=5, minSize=(30, 30),) 


# In[5]:


# 加载卷积神经网络模型：
face_recognition_model = keras.Sequential()
MODEL_PATH = 'face_model3.h5'
face_recognition_model = load_model(MODEL_PATH)

print(face_recognition_model)


# In[6]:
'''
f=h5py.File(MODEL_PATH)
for layer,g in f.items():
    print(layer)
    for name,d in g.items():
        print("{}*****".format(name))#print("{}:{}".format(name,d.value))
'''

for (x, y, width, height) in faces:
    img = cv2.imread(route)
    #img = image[y:y+height, x:x+width]
    img = resize_without_deformation(img)
 
    img = img.reshape((1, 100, 100, 3))
    img = np.asarray(img, dtype = np.float32)
    img /= 255.0
 
    result = face_recognition_model.predict_classes(img)
 
    cv2.rectangle(image, (x, y), (x + width, y + height), (255, 0, 0), 1)
    #font = cv2.FONT_HERSHEY_SIMPLEX
    #print("result",type(result),len(result),result)
    #if result[0] == 41:
    #    cv2.putText(image, 'liuxiangchao', (x, y-2), font, 0.7, (0, 255, 0), 2)
    #else:
    #    cv2.putText(image, 'No.%d' % result[0], (x, y-2), font, 0.7, (0, 255, 0), 2)
        
cv2.imshow('', image)
cv2.imwrite(route,image)
cv2.waitKey(1000)
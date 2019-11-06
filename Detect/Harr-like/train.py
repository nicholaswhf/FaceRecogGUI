#!/usr/bin/env python
# coding: utf-8

# In[16]:





# In[11]:


# _*_ coding:utf-8 _*_
import cv2
import os

CASE_PATH = "haarcascade_frontalface_default.xml"
RAW_IMAGE_DIR = 'me/'
DATASET_DIR = 'ORL/s41/'

face_cascade = cv2.CascadeClassifier(CASE_PATH)

def save_feces(img, name,x, y, width, height):
    image = img[y:y+height, x:x+width]
    cv2.imwrite(name, image)

image_list = os.listdir(RAW_IMAGE_DIR) #列出文件夹下所有的目录与文件
count = 1
for image_path in image_list:
    image = cv2.imread(RAW_IMAGE_DIR + image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray,
                                         scaleFactor=1.2,
                                         minNeighbors=5,
                                         minSize=(5, 5), )

    for (x, y, width, height) in faces:
        save_feces(image, '%s%d.pgm' % (DATASET_DIR, count), x, y - 30, width, height+30)
    count += 1


# In[1]:


# 尺寸变换


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


# In[16]:


'''下面是读取照片的函数，可以传入尺寸，默认尺寸是100*100，返回了两个列表，第一个列表中每一个元素都是一张图片，第二个列表中则对应存储了图
片的标签，这里用1、2、3.......来指代，因为我根本不知道这些人的名字是什么:'''


def read_image(size = None):
    data_x, data_y = [], []
    for i in range(1,42):
        for j in range(1,11):
            try:
                #print('ORL/s%d/%d.pgm' % (i,j))
                im = cv2.imread('./ORL/s%d/%d.pgm' % (i,j))
                #im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                #cv2.imshow("gray",im)
                #cv2.waitKey(10000)
                if size is None:
                    size = (100, 100)
                im = resize_without_deformation(im, size)
                data_x.append(np.asarray(im, dtype = np.int8))
                data_y.append(str(int((i-1)%42.0)))
                print("DATA_Y",str(int((i-1)%42.0)))
            except IOError as e:
                print(e)
            except:
                pass
                #print('Unknown Error!')
    print(data_y)
    return data_x, data_y


# In[17]:


# 接下来就是最重要的一步了，训练卷积神经网络

# 引进卷积和池化层，卷积类似于图像处理中的特征提取操作，池化则很类似于降维,常用的有最大池化和平均池化：

from keras.layers import Conv2D, MaxPooling2D

'''引入全连接层、Dropout、Flatten。

全连接层就是经典的神经网络全连接。

Dropout用来在训练时按一定概率随机丢弃一些神经元，以获得更高的训练速度以及防止过拟合。

Flatten用于卷积层与全连接层之间，把卷积输出的多维数据拍扁成一维数据送进全连接层（类似shape方法）：
'''
from keras.layers import  Dense, Dropout, Flatten

# 引入SGD（梯度下降优化器）来使损失函数最小化

from keras.optimizers import SGD
import numpy as np


# In[18]:


# 读入所有图像及标签

IMAGE_SIZE = 100
raw_images, raw_labels = read_image(size=(IMAGE_SIZE, IMAGE_SIZE))
raw_images, raw_labels = np.asarray(raw_images, dtype = np.float32), np.asarray(raw_labels, dtype = np.int32)


# In[19]:


#把图像转换为float类型，方便归一化


'''神经网络需要数值进行计算，需要对字符型类别标签进行编码，最容易想到的就是把他们编码成1、2、3.......这种，但是这样也就出现了强行给它们
 定义了大小的问题，因为如果一个类别是2，一个是4，他们之间就会有两倍的关系，但是实际上他们之间并没有直接的倍数关系，所以这里使用one-hot编
 码规则，做到所有标签的平等化。on-hot编码：
'''
from keras.utils import np_utils
ont_hot_labels = np_utils.to_categorical(raw_labels)
print("##################labels:",ont_hot_labels)


# In[20]:


'''在所有读入的图像和标签中，需要划分一部分用来训练，一部分用来测试，这里使用了sklearn中的train_test_split方法，
不仅可以分割数据，还可以把数据打乱，训练集 ：测试集 = 7 : 3  ：'''
from sklearn.model_selection import  train_test_split
train_input, valid_input, train_output, valid_output =train_test_split(raw_images, 
                  ont_hot_labels,
                  test_size = 0.3)


# In[21]:


# 数据归一化，图像数据只需要每个像素除以255就可以：
train_input /= 255.0
valid_input /= 255.0


# In[22]:


'''添加卷积层，32个卷积核，每个卷积核是3 * 3，边缘不补充，卷积步长向右、向下都为1, 后端运算使用 tf , 图片输入尺寸是（100，100， 3），
使用relu作为激活函数，也可以用sigmoid函数等，relu收敛速度比较快：'''
import keras
from keras.layers.convolutional import Conv2D
face_recognition_model = keras.Sequential()
 
face_recognition_model.add(Conv2D(32, (3, 3), padding='valid',
                                  strides = (1, 1),
                                  
                                  input_shape = (IMAGE_SIZE, IMAGE_SIZE, 3),
                                  activation='relu',
                                  data_format="channels_last"))
 
face_recognition_model.add(Conv2D(32, (3, 3),padding='valid',
                                  strides = (1, 1),
                                  data_format="channels_last",
                                  activation = 'relu'))
# 


# In[23]:


# 池化层，过滤器尺寸是2 * 2：
face_recognition_model.add(MaxPooling2D(pool_size=(2, 2)))


# In[24]:


face_recognition_model.add(Dropout(0.2))


# In[25]:


face_recognition_model.add(Conv2D(64, (3, 3),padding='valid',
                                  strides = (1, 1),
                                  data_format="channels_last",
                                  activation = 'relu'))

face_recognition_model.add(Conv2D(64, (3, 3),padding='valid',
                                  strides = (1, 1),
                                  data_format="channels_last",
                                  activation = 'relu'))
 
face_recognition_model.add(MaxPooling2D(pool_size=(2, 2)))
face_recognition_model.add(Dropout(0.2))


# In[26]:


# Flatten层，处于卷积层与Dense（全连层）之间，将图片的卷积输出压扁成一个一维向量：
face_recognition_model.add(Flatten())
    


# In[27]:


# 全连接层,  经典的神经网络结构，512个神经元：
face_recognition_model.add(Dense(512, activation = 'relu'))
face_recognition_model.add(Dropout(0.4))


# In[28]:


# 输出层，神经元数是标签种类数，使用sigmoid激活函数，输出最终结果：
face_recognition_model.add(Dense(len(ont_hot_labels[0]), activation = 'sigmoid'))


# In[29]:


face_recognition_model.summary()


# In[30]:


'''使用SGD作为反向传播的优化器，来使损失函数最小化，学习率(learning_rate)是0.01，学习率衰减因子(decay)用来随着迭代次数不断减小学习率，防止出现震荡。
引入冲量(momentum),不仅可以在学习率较小的时候加速学习，又可以在学习率较大的时候减速，使用nesterov：
'''
learning_rate = 0.01
decay = 1e-6
momentum = 0.8
nesterov = True
sgd_optimizer = SGD(lr = learning_rate, decay = decay,
                    momentum = momentum, nesterov = nesterov)


# In[31]:


# 编译模型，损失函数使用交叉熵，交叉熵函数随着输出和期望的差距越来越大，输出曲线会越来越陡峭，对权值的惩罚力度也会增大，如果其他的损失函数，如均方差可以可以的，各有优劣：
face_recognition_model.compile(loss = 'categorical_crossentropy',
                               optimizer = sgd_optimizer,
                               metrics = ['accuracy'])


# In[32]:


# 开始训练，训练100次（epochs），每次训练分几个批次，每批（batch_size）20个，shuffle用来打乱样本顺序
batch_size = 20 #每批训练数据量的大小
epochs = 1
face_recognition_model.fit(train_input, train_output,
                           epochs = epochs,
                           batch_size = batch_size, 
                           shuffle = True,
                           validation_data = (valid_input, valid_output))


# In[34]:


print(face_recognition_model.evaluate(valid_input, valid_output, verbose=0))
print("##output",face_recognition_model.predict_classes(valid_input))
print("##input",valid_output,len(valid_output),valid_output[0])
print(len(valid_input),len(valid_output))


MODEL_PATH = 'face_model31.h5'
face_recognition_model.save(MODEL_PATH)


# In[37]:


#要开始写在识别时正式运行的程序了


# In[2]:




import cv2
import numpy as np
import  keras
from keras.models import load_model
# 加载级联分类器模型：
CASE_PATH = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(CASE_PATH)


# In[3]:


# 打开摄像头，获取图片并灰度化：
cap = cv2.VideoCapture(0) 
ret, image = cap.read()
#image = cv2.imread('10.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 


# In[4]:


# 人脸检测：
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2,
                                minNeighbors=5, minSize=(30, 30),) 


# In[5]:


# 加载卷积神经网络模型：
face_recognition_model = keras.Sequential()
MODEL_PATH = 'face_model3.h5'
face_recognition_model = load_model(MODEL_PATH)


# In[6]:


for (x, y, width, height) in faces:
    img = image[y:y+height, x:x+width]
    img = resize_without_deformation(img)
 
    img = img.reshape((1, 100, 100, 3))
    img = np.asarray(img, dtype = np.float32)
    img /= 255.0
 
    result = face_recognition_model.predict_classes(img)
 
    cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    if result[0] == 41:
        cv2.putText(image, 'liuxiangchao', (x, y-2), font, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(image, 'No.%d' % result[0], (x, y-2), font, 0.7, (0, 255, 0), 2)
        
cv2.imshow('', image)
cv2.waitKey(10000)


# In[7]:





# In[ ]:





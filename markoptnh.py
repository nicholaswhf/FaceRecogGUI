import cv2
import sys
import numpy as np
import math
import os
import glob
import Nh
import copy
def goss(frame):
    img=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    N_h,I_avg=Nh.Nh(img,1)
    size=img.shape
    img_op=img
    mat_gamma=np.zeros(size)
    pixels=0
    for i in range(0,size[0]):
        for j in range(0,size[1]):
            #img_op[i][j]=(255-img[i][j][0],255-img[i][j][1],255-img[i][j][2])
            pixels=pixels+img[i][j]
            img_op[i][j]=255-img[i][j]
            #print(img_op[i][j])
    #cv2.imshow("opposite",img_op)
    kernel_size=(5,5)
    sigma=1.5
    alpha=0.0
    img_gu=cv2.GaussianBlur(img_op,kernel_size,sigma)
    #cv2.imshow("gaussian",img_gu)
    #cv2.waitKey(10000)
    #print("pixels:",pixels/(size[0]*size[1]))
    pixels=pixels/(size[0]*size[1])
    if(pixels<128):
        #alpha=math.log(pixels/255)/math.log(0.5)
        alpha=math.log(pixels/255)/math.log(0.5)
    else:
        alpha=math.log(0.5)/math.log(pixels/255)
    #print("alpha",alpha)
    alpha0=alpha
    #print("pre",mat_gamma)
    for i in range(0,size[0]):
        for j in range(0,size[1]):
            #print("alpha",alpha)
            #A
            alpha=alpha0+(N_h[i][j]/alpha0)
            #B
            #alpha=alpha0*(N_h[i][j])
            mat_gamma[i][j]=math.pow(alpha,(128-img_gu[i][j])/128)
    #print("after",mat_gamma)

    img_pre=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #cv2.imshow("pre",img_pre)
    #cv2.waitKey(10000)
    img_after=img_pre
    for i in range(0,size[0]):
        for j in range(0,size[1]):
            #print("pow",img_pre[i][j]/255,mat_gamma[i][j],math.pow(0.9,0.9))
            img_after[i][j]=math.pow(img_pre[i][j]/255,mat_gamma[i][j])*255
    #cv2.imshow("after",img_after)
    #cv2.waitKey(10000)
    return img_after
def batch(in_dir,out_dir):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    if not os.path.exists(in_dir):
        return -1
    for file in glob.glob(in_dir+"/*"):
        filepath,filename=os.path.split(file)
        file=filepath+"/"+filename
        print(file)
        img=goss(file)
        cv2.imwrite(out_dir+"/"+filename,img)

if __name__ == '__main__':
    
    in_dir=sys.argv[1]
    out_dir=sys.argv[2]
    batch(in_dir,out_dir)
    '''
    filename=sys.argv[1]
    goss(filename)
    '''

from tkinter import *
import cv2
import Alib
from PIL import Image,ImageTk
import os
import argparse
import aligndlib
import subprocess
import openface
import pickle
import dlib
import time
import numpy as np

def getRep(frame):
    start=time.time()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    bbs = align.getAllFaceBoundingBoxes(frame)
    reps=[]
    for bb in bbs:
        alignedFace=align.align(96,frame,bb,landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        rep=net.forward(alignedFace)
        reps.append((bb.center().x,rep,bb))
    sreps=sorted(reps,key=lambda x:x[0])
    return sreps

def verification(img,clf):
    reps=getRep(img)
    person=" "
    for r in reps:
        rep=r[1].reshape(1,-1)
        face_rect=r[2]
        cv2.rectangle(img,(face_rect.left(), face_rect.top()),(face_rect.right(), face_rect.bottom()),(0,255,255),3);
        start=time.time()
        predictions = clf.predict_proba(rep).ravel()
        maxI = np.argmax(predictions)
        person = le.inverse_transform([maxI])[0]
        confidence = predictions[maxI]
        font=cv2.FONT_HERSHEY_SIMPLEX
        if(confidence<0.90):
            person="ERROR"
    return img,person  

		


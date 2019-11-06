import cv2
import numpy as np

def lk(path,fps):
	cap = cv2.VideoCapture(path)
	ret, frame1 = cap.read()
	prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
	hsv = np.zeros_like(frame1)
	hsv[...,1] = 255
	name=0
	while(name<15):
		ret, frame2 = cap.read()
		next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
		flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
		mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
		hsv[...,0] = ang*180/np.pi/2
		hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
		rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
		cv2.imwrite('./Record/LK/real/'+str(name)+'.png',rgb)
		if(name<14):
			ret, frame1 = cap.read()
			prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
		name+=1
	cap.release()
	print("LK Generate Over...")
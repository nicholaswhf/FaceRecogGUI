import cv2
import sys
import numpy as np
import copy


def Nh(frame,h):
	img=copy.deepcopy(frame)
	size=img.shape
	I_m=copy.deepcopy(img)
	I_mm=copy.deepcopy(img)
	S_h=copy.deepcopy(img)
	M_h=np.empty(size)
	N_h=np.empty(size)
	I_avg=np.empty(size)

	for i in range(0,size[0]):
		for j in range(0,size[1]):
			if(i>0 and i<(size[0]-1) and j>0 and j<(size[1]-1)) :
				b=np.array([img[i-1][j],img[i+1][j],img[i-1][j-1],img[i-1][j+1],img[i+1][j-1],img[i+1][j+1],img[i][j+1],img[i][j-1]])
				b.sort()
				#print(b)
				I_m[i][j]=b[7]
				I_avg[i][j]=(int(b[1])+int(b[2])+int(b[3])+int(b[4])+int(b[5])+int(b[6]))/6
			else:
				I_m[i][j]=img[i][j]
	#print("img size",size)
	#print("Imshape",I_m.shape)

	for i in range(0,size[0]):
		for j in range(0,size[1]):
			if(i>0 and i<(size[0]-1) and j>0 and j<(size[1]-1)) :
				b=np.array([I_m[i-1][j],I_m[i+1][j],I_m[i-1][j-1],I_m[i-1][j+1],I_m[i+1][j-1],I_m[i+1][j+1],I_m[i][j+1],I_m[i][j-1]])
				b.sort()
				I_mm[i][j]=(int(b[3])+int(b[4]))/2
			else:
				#print("iM:",I_m[i][j])
				#print("xy",i,j)
				b=np.array([I_m[i][j]])
				I_mm[i][j]=int(b[0])
	
	for i in range(0,size[0]):
		for j in range(0,size[1]):
			if(i>0 and i<(size[0]-1) and j>0 and j<(size[1]-1)):
				a=np.array([I_mm[i-1][j],I_mm[i-1][j+1],I_mm[i-1][j-1],I_mm[i+1][j],I_mm[i+1][j+1],I_mm[i+1][j-1],I_mm[i][j-1],I_mm[i][j+1]])
				a.sort()
				#print("a",a)
				S_h[i,j]=a[8-int(h)]
			else:
				S_h[i][j]=I_mm[i][j]
	
	for i in range(0,size[0]):
		for j in range(0,size[1]):
			if(S_h[i][j]==0):
				#print("ZEROS")
				M_h[i][j]=1
			else:
				#print(type(float(img[i][j])))
				#print(68/86)
				if(img[i][j]==0):
					img[i][j]=1
				M_h[i][j]=float(img[i][j])/float(S_h[i][j])
				#print("*:",img[i][j],S_h[i][j],M_h[i][j])
			if(M_h[i][j]<=1):
				N_h[i][j]=M_h[i][j]
			else:
				N_h[i][j]=1
	#cv2.imshow("N_h",N_h)
	#cv2.imshow("Img",img)
	#cv2.imshow("I_m",I_m)
	#cv2.imshow("I_mm",I_mm)
	#cv2.imshow("S_h",S_h)
	#print("N_h",N_h)
	#print("Img",img)
	#print("S_h",S_h)
	#cv2.waitKey(3000)
	#print(I_m)
	return N_h,I_avg

if __name__ == '__main__':
	filename=sys.argv[1]
	h=sys.argv[2]
	Nh(filename,h)
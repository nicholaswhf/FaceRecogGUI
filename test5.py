from PyQt5 import QtCore,QtGui,QtWidgets,QtSql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette,QBrush,QPixmap,QColor
import sys
import qtawesome
import cv2
import Alib
import openface
import numpy as np
import dlib
import pickle
import time
import markoptnh
import datetime 

import torch
import torchvision
import torch.nn as nn
import torchvision.transforms as transforms
from torch.autograd import Variable

import EVM2 as evm

from PIL import Image
import lk2 as lk

class MainGui(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
		db.setDatabaseName('./Manager/FaceEntrance.sqlite')
		res=db.open()
		print("connect:",res)
		self.person='ERROR'
		self.id='0000'
		self.time='2019-04-20 19:30:30'
		self.init_gui()
		self.qtawesome()
		self.timer_camera = QtCore.QTimer()
		self.timer_camera.start(30)
		self.timer_camera.timeout.connect(self.show_camera)
		self.flag_recog=0
		self.transform=transforms.Compose([transforms.Resize((227,227)),transforms.CenterCrop(227),transforms.ToTensor()])
		self.predictor_model="./shape_predictor_68_face_landmarks.dat"
		self.align = Alib.AlignDlib(self.predictor_model)
		self.spoofyingnet=torch.load("../Spoofying/Models/alexnet-418-20.pkl",map_location='cpu')
		self.face_pose_predictor=dlib.shape_predictor(self.predictor_model)
		self.face_detector=dlib.get_frontal_face_detector()
		self.c=0
		self.net = openface.TorchNeuralNet("nn4.small2.v1.t7",imgDim=96,cuda=False)
		with open("./Train-Features/classifier.pkl",'rb+') as f:
			if sys.version_info[0]<3:
				(self.le,self.clf)=pickle.load(f)
			else:
				(self.le,self.clf)=pickle.load(f,encoding='latin1')
		
		self.video="http://admin:admin@192.168.31.48:8081/"   #此处@后的ipv4 地址需要修改为自己的地址
		self.cap = cv2.VideoCapture(0)
		#self.cap=cv2.VideoCapture(self.video)
		#self.cap = cv2.VideoCapture("../DataSets/MySpoofyingAttack/attack/001photo.avi")
		#self.cap = cv2.VideoCapture("../DataSets/MySpoofyingAttack/real/001.avi")
		#self.cap = cv2.VideoCapture(0)
		flag,self.pre_image=self.cap.read()
	def camera(self):
		self.timer_camera = QtCore.QTimer()
		self.cap = cv2.VideoCapture(self)
		self.show_camera()
	def show_camera(self):
		flag, self.image = self.cap.read()
		width, height = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		timeF=30
		show = cv2.resize(self.image, (360, 270))
		show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
		video_tensor=np.zeros((2,height,width,3),dtype='float')
		if(self.flag_recog==1):
			'''
			video_tensor[0]=self.pre_image
			video_tensor[1]=self.image
			self.evm(video_tensor)
			self.spoofying()
			'''
			self.spoofyingdetect()
			detected_faces=self.face_detector(show)

			if(len(detected_faces)>0):
				print("Verification...")
				self.verification(show)
			else:
				self.flag_recog=0
				print("NOFACE!!!!!!!!!!!!!",len(detected_faces),self.c%timeF)
				#for i,face_rect in enumerate(detected_faces):
				#	pass
				#   cv2.rectangle(show,(face_rect.left(), face_rect.top()),(face_rect.right(), face_rect.bottom()),(0,255,255),3);
			
			self.c=self.c+1
			if(self.c>100):
				self.c=0
		showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
		self.camera.setPixmap(QtGui.QPixmap.fromImage(showImage))
		self.pre_image=self.image

	def init_gui(self):
		self.setFixedSize(360,500)
		self.set_gui()
		self.qtawesome()
	def set_gui(self):
		self.setObjectName('Main_Window')
		self.camera=QtWidgets.QLabel('Video',self)
		self.camera.setObjectName('Camera')
		self.camera.setFixedSize(360,270)
		self.camera.setAutoFillBackground(True)
		self.camera.move(0,0)
		palette=QPalette()
		background_color=QColor()
		background_color.setNamedColor('#a6a6a6')
		palette.setColor(QPalette.Window,background_color)
		self.camera.setPalette(palette)
		self.camera.setAlignment(Qt.AlignCenter)

		self.photo=QtWidgets.QLabel('Photo',self)
		self.photo.setObjectName('Camera')
		self.photo.setFixedSize(68,78)
		self.photo.setAutoFillBackground(True)
		self.photo.move(240,370)
		palette=QPalette()
		background_color=QColor()
		background_color.setNamedColor('#a6a6a6')
		palette.setColor(QPalette.Window,background_color)
		self.photo.setPalette(palette)
		self.photo.setAlignment(Qt.AlignCenter)

		self.button_recog=QtWidgets.QPushButton('RECOG',self)
		self.button_recog.setObjectName('Button_Recog')
		self.button_recog.setFixedSize(88,40)
		self.button_recog.move(135,290)

		self.button_recog.clicked.connect(self.recognition)

		self.label_name=QtWidgets.QLabel(self.person,self)
		self.label_name.setObjectName('Label_Name')
		self.label_name.setFixedSize(94,24)
		self.label_name.move(50,370)

		self.label_id=QtWidgets.QLabel('ID:'+self.id,self)
		self.label_id.setObjectName('Label_Id')
		self.label_id.setFixedSize(81,14)
		self.label_id.move(50,400)

		self.label_time=QtWidgets.QLabel('TIME：'+self.time,self)
		self.label_time.setObjectName('Label_Time')
		self.label_time.setFixedSize(125,14)
		self.label_time.move(50,420)

		self.label_sp=QtWidgets.QLabel('Spoofying',self)
		self.label_sp.setObjectName('Label_Sp')
		self.label_sp.setFixedSize(120,14)
		self.label_sp.move(50,440)

		print("########################")

	def qtawesome(self):
		self.camera.setStyleSheet('''QLabel{background:#a6a6a6;}''')
		self.button_recog.setStyleSheet('''QPushButton{background:#2a82e4;font-size:19px;font-weight:550;color:white;border-radius:20px;}''')
		self.label_name.setStyleSheet('''QLabel{font-size:16px;font-weight:500}''')
		self.label_id.setStyleSheet('''QLabel{font-size:10px;color:#505050}''')
		self.label_time.setStyleSheet('''QLabel{font-size:10px;color:#505050}''')
		self.label_sp.setStyleSheet('''QLabel{font-size:10px;color:#505050}''')
		#self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
	def recognition(self):
		print('here')
		self.flag_recog=1
		print(time.time())
	def getRep(self,frame):
		bbs = self.align.getAllFaceBoundingBoxes(frame)
		reps=[]
		for bb in bbs:
			alignedFace=self.align.align(96,frame,bb,landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
			#start=time.time()
			#alignedFace=markoptnh.goss(alignedFace)
			#end=time.time()
			#print("###################",end-start)
			rep=self.net.forward(alignedFace)
			reps.append((bb.center().x,rep,bb))
		sreps=sorted(reps,key=lambda x:x[0])
		return sreps
	def verification(self,frame):
		reps=self.getRep(frame)
		for r in reps:
			rep=r[1].reshape(1,-1)
			face_rect=r[2]
			#cv2.rectangle(frame,(face_rect.left(), face_rect.top()),(face_rect.right(), face_rect.bottom()),(0,255,255),3);
			predictions = self.clf.predict_proba(rep).ravel()
			maxI = np.argmax(predictions)
			self.id = self.le.inverse_transform([maxI])[0]
			confidence = predictions[maxI]
			print("###",self.id,confidence)
			#if(confidence<0.90):
			#	self.id='ERROR'
			#query = QtSql.QSqlQuery()
			cmd="SELECT * FROM information WHERE ID= "+str(self.id)
			#cmd="SELECT * FROM information "
			print("cmd",cmd)
			query = QtSql.QSqlQuery(cmd)
			while query.next():
				value_0=query.value(0)
				value_1=query.value(1)
				value_2=query.value(2)
				idpic_path="./ID/"+str(value_0)+".jpg"
				idpic=cv2.imread(idpic_path)
				idpic= cv2.resize(idpic, (68, 78))
				idpic = cv2.cvtColor(idpic, cv2.COLOR_BGR2RGB)
				idpic = QtGui.QImage(idpic.data, idpic.shape[1], idpic.shape[0], QtGui.QImage.Format_RGB888)
				self.photo.setPixmap(QtGui.QPixmap.fromImage(idpic))
				self.person=value_1
				self.label_id.setText(self.id)
				self.label_name.setText(self.person)
				t_all,year,month,day,hour=self.gettime()
				#t_all=self.gettime()
				self.label_time.setText(year+"-"+month+"-"+day+" "+hour)
				cmd="insert into record values("+str(value_0)+",'"+year+"','"+month+"','"+day+"','"+hour+"','"+str(confidence)+"','./record/"+t_all+".jpg'"+")"
				res=QtSql.QSqlQuery(cmd)
				archi = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
				cv2.imwrite("./Record/"+t_all+".jpg",archi)
				print(res)
				self.flag_recog=0
	def gettime(self):
		t = time.time()
		all_t=str(datetime.datetime.fromtimestamp(t))
		#2019-00-00
		year=all_t[0:4]
		month=all_t[5:7]
		day=all_t[8:10]
		hour=all_t[11:19]
		return all_t,year,month,day,hour
	def evm(self,video_tensor):
		#print("EVM...")
		low=1
		high=1.6
		levels=3
		amplification=2
		fps = int(self.cap.get(cv2.CAP_PROP_FPS))
		lap_video_list=evm.laplacian_video(video_tensor,levels=levels)
		filter_tensor_list=[]
		for i in range(levels):
			filter_tensor=evm.butter_bandpass_filter(lap_video_list[i],low,high,fps)
			filter_tensor*=amplification
			filter_tensor_list.append(filter_tensor)
		recon=evm.reconstract_from_tensorlist(filter_tensor_list)
		final=video_tensor+recon
		evm.save_video(final,"./Record/DIYA-R1.avi")
		#self.lk(final)
	def lk(self,video_tensor):
		#print("LK...")
		cap = cv2.VideoCapture("./Record/DIYA-R1.avi")
		ret, frame1 = cap.read()
		ret, frame2 = cap.read()
		hsv = np.zeros_like(frame1)
		#hsv = np.zeros_like(video_tensor[0])
		hsv[...,1] = 255
		prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
		latter = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
		flow = cv2.calcOpticalFlowFarneback(prvs,latter, None, 0.5, 3, 15, 3, 5, 1.2, 0)
		mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
		hsv[...,0] = ang*180/np.pi/2
		hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
		rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
		#cv2.imwrite("./Record/LK/attack/LK.jpg",rgb)
		cv2.imwrite("./Record/LK/real/LK.jpg",rgb)
	def spoofying(self):
		f=open("spoofyingtest.txt","a+")
		print("SPOOOFYING...")
		testloader=self.loadTestDataSet()
		for i,data in enumerate(testloader,0):
			inputs,labels=data
			inputs,labels=Variable(inputs),Variable(labels)
			outputs=self.spoofyingnet(inputs)
			_,predicted=torch.max(outputs.data,1)
			print("Predicted",predicted.data)
			score=(predicted).sum().item()
			print("SCORE",score)
			if(score>=10):
				print("real")
				self.label_sp.setText("REAL")
			else:
				print("spoofying")
				self.label_sp.setText("ATTACK")
			f.write(str(predicted.data)+"\n")
	def spoofyingdetect(self):
		fps = int(self.cap.get(cv2.CAP_PROP_FPS))
		frame_count=30
		width, height = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		video_tensor=np.zeros((frame_count,height,width,3),dtype='float')
		x=0
		while(x<=frame_count):
			ret,frame=self.cap.read()
			if(x<frame_count):
				video_tensor[x]=frame
				x+=1
			if(x==frame_count):
				x+=1
				self.evm(video_tensor)
		lk.lk("./Record/DIYA-R1.avi",30)
		self.spoofying()

	def loadTestDataSet(self):
		fps = int(self.cap.get(cv2.CAP_PROP_FPS))
		path="./Record/LK/"
		testset=torchvision.datasets.ImageFolder(path,transform=transforms.Compose([transforms.Resize((227,227)),transforms.ToTensor()]))
		testloader=torch.utils.data.DataLoader(testset,batch_size=15,shuffle=True,num_workers=2)
		return testloader

if __name__ == '__main__':
	app=QApplication(sys.argv)
	gui=MainGui()
	gui.show()
	sys.exit(app.exec_())

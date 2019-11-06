import sys
import dlib
import cv2
import numpy as np
TEMPLATE = np.float32([
    (0.0792396913815, 0.339223741112), (0.0829219487236, 0.456955367943),
    (0.0967927109165, 0.575648016728), (0.122141515615, 0.691921601066),
    (0.168687863544, 0.800341263616), (0.239789390707, 0.895732504778),
    (0.325662452515, 0.977068762493), (0.422318282013, 1.04329000149),
    (0.531777802068, 1.06080371126), (0.641296298053, 1.03981924107),
    (0.738105872266, 0.972268833998), (0.824444363295, 0.889624082279),
    (0.894792677532, 0.792494155836), (0.939395486253, 0.681546643421),
    (0.96111933829, 0.562238253072), (0.970579841181, 0.441758925744),
    (0.971193274221, 0.322118743967), (0.163846223133, 0.249151738053),
    (0.21780354657, 0.204255863861), (0.291299351124, 0.192367318323),
    (0.367460241458, 0.203582210627), (0.4392945113, 0.233135599851),
    (0.586445962425, 0.228141644834), (0.660152671635, 0.195923841854),
    (0.737466449096, 0.182360984545), (0.813236546239, 0.192828009114),
    (0.8707571886, 0.235293377042), (0.51534533827, 0.31863546193),
    (0.516221448289, 0.396200446263), (0.517118861835, 0.473797687758),
    (0.51816430343, 0.553157797772), (0.433701156035, 0.604054457668),
    (0.475501237769, 0.62076344024), (0.520712933176, 0.634268222208),
    (0.565874114041, 0.618796581487), (0.607054002672, 0.60157671656),
    (0.252418718401, 0.331052263829), (0.298663015648, 0.302646354002),
    (0.355749724218, 0.303020650651), (0.403718978315, 0.33867711083),
    (0.352507175597, 0.349987615384), (0.296791759886, 0.350478978225),
    (0.631326076346, 0.334136672344), (0.679073381078, 0.29645404267),
    (0.73597236153, 0.294721285802), (0.782865376271, 0.321305281656),
    (0.740312274764, 0.341849376713), (0.68499850091, 0.343734332172),
    (0.353167761422, 0.746189164237), (0.414587777921, 0.719053835073),
    (0.477677654595, 0.706835892494), (0.522732900812, 0.717092275768),
    (0.569832064287, 0.705414478982), (0.635195811927, 0.71565572516),
    (0.69951672331, 0.739419187253), (0.639447159575, 0.805236879972),
    (0.576410514055, 0.835436670169), (0.525398405766, 0.841706377792),
    (0.47641545769, 0.837505914975), (0.41379548902, 0.810045601727),
    (0.380084785646, 0.749979603086), (0.477955996282, 0.74513234612),
    (0.523389793327, 0.748924302636), (0.571057789237, 0.74332894691),
    (0.672409137852, 0.744177032192), (0.572539621444, 0.776609286626),
    (0.5240106503, 0.783370783245), (0.477561227414, 0.778476346951)])

TPL_MIN, TPL_MAX = np.min(TEMPLATE, axis=0), np.max(TEMPLATE, axis=0)
MINMAX_TEMPLATE = (TEMPLATE - TPL_MIN) / (TPL_MAX - TPL_MIN)


class AlignDlib:
	"""
	使用‘dlib’的landmark estimation 来校正人脸：
	1-人脸尺寸重置：96×96
	2-landmarks的位置规范化
	"""

	#landmark indices
	INNER_EYES_AND_BOTTOM_LIP=[39,42,57]
	OUTER_EYES_AND_NOSE=[36,45,33]

	def __init__(self,facePredictor):
		"""
		初始化一个对象.
		:param of facePredictor:the path to dlib's
		:type of facePredictor:str
		"""
		assert facePredictor is not None

		self.detector=dlib.get_frontal_face_detector()
		self.predictor=dlib.shape_predictor(facePredictor)
	def getAllFaceBoundingBoxes(self,rgbImg):
		"""
		找到图片中的所有bounding box（限制框）
		rgbImg:待处理的图像；shape(height,width,3)
		return:找到的所有限制框；类型 dlib.rectangles
		"""

		assert rgbImg is not None

		try:
			return self.detector(rgbImg,1)
			# we should upsample the image 1 time.  
		except Exception as e:
			print("warning:{}".format(e))
			return []

	def getLargestFaceBoundingBox(self,rgbImg,skipMulti=False):
		"""
		找到图像中最大的限制框
		rgbImg：待处理的图像；shaple(height,width，3)
		skipMulti：如果有多个人脸检测出来，则跳过改图像，默认为False
		return:最大的人脸限制框；dlib.rectangles
		"""
		assert rgbImg is not None
		faces=self.getAllFaceBoundingBoxes(rgbImg)
		if (not skipMulti and len(faces)>0) or len(faces)==1:
			return max(faces,key=lambda rect:rect.width()*rect.height())
		else:
			return None

	def findLandmarks(self,rgbImg,bb):
		"""
		找到人脸中的landmarks
		rgnImg：待处理的人脸图像；shape（height，width，3）
		bb：在bounding box上找landmarks
		return：jiancedaoderenlianlandmarks的位置；
		返回类型：list（x,y）元组
		"""
		assert rgbImg is not None
		assert bb is not None
		points=self.predictor(rgbImg,bb)
		return list(map(lambda p:(p.x,p.y),points.parts()))

	def align(self,imgDim,rgbImg,bb=None,landmarks=None,landmarkIndices=INNER_EYES_AND_BOTTOM_LIP,skipMulti=False):
		#align(534,image,face_rect,landmakIndices=Alib.AlignDlib.OUTER_EYES_AND_NOSE)
		#                                               landmarkIndices
		"""
		校正人脸
		rgbImg：待处理的图像
		bb：人脸的限制框
		landmarks：检测出的人脸landmarks的位置
		landmarkIndices：校准的基准
		skipMutli：当有多个face检测出来的时候是否跳过
		返回值：校准的RGB图像 shape（height，width，3）
		imgDim：int-图像尺寸重置的边长长度
		
		"""
		assert imgDim is not None
		assert rgbImg is not None
		assert landmarkIndices is not None

		if bb is None:
			bb=self.getLargestFaceBoundingBox(rgbImg,skipMulti)
			if bb is None:
				return
		if landmarks is None:
			landmarks=self.findLandmarks(rgbImg,bb)
		npLandmarks=np.array(landmarks)
		npLandmarks=np.float32(landmarks)
		npLandmarkIndices=np.array(landmarkIndices)

		H=cv2.getAffineTransform(npLandmarks[npLandmarkIndices],imgDim*MINMAX_TEMPLATE[npLandmarkIndices])
		thumbnail=cv2.warpAffine(rgbImg,H,(imgDim,imgDim))
		return thumbnail

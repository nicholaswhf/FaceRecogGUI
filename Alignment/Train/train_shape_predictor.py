
import os
import sys
import glob

import dlib
import cv2

import numpy as np

if len(sys.argv) != 2:
    print(
        "Give the path to the examples/faces directory as the argument to this "
        "program. For example, if you are in the python_examples folder then "
        "execute this program by running:\n"
        "    ./train_shape_predictor.py ../examples/faces")
    exit()
faces_folder = sys.argv[1]

options = dlib.shape_predictor_training_options()

options.oversampling_amount = 300
options.nu = 0.05
options.tree_depth = 4
options.cascade_depth=3
options.be_verbose = True


training_xml_path = os.path.join(faces_folder, "training_with_face_landmarks.xml")
dlib.train_shape_predictor(training_xml_path, "predictor.dat", options)

print("\nTraining accuracy: {}".format(
    dlib.test_shape_predictor(training_xml_path, "predictor.dat")))

testing_xml_path = os.path.join(faces_folder, "testing_with_face_landmarks.xml")
print("Testing accuracy: {}".format(
    dlib.test_shape_predictor(testing_xml_path, "predictor.dat")))

'''
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

predictor = dlib.shape_predictor("predictor.dat")
detector = dlib.get_frontal_face_detector()

TMP=np.zeros_like(TEMPLATE)
print(TMP)

LAND=np.zeros_like(TEMPLATE)

TPL_MIN, TPL_MAX = np.min(TEMPLATE, axis=0), np.max(TEMPLATE, axis=0)
MINMAX_TEMPLATE = (TEMPLATE - TPL_MIN) / (TPL_MAX - TPL_MIN)


INNER_EYES_AND_BOTTOM_LIP=[39,42,57]
OUTER_EYES_AND_NOSE=[36,45,33]
landmarkIndices=INNER_EYES_AND_BOTTOM_LIP
npLandmarkIndices=np.array(landmarkIndices)


print("Showing detections and predictions on the images in the faces folder...")
win = dlib.image_window()
for f in glob.glob(os.path.join(faces_folder, "*.png")):
    print("Processing file: {}".format(f))
    img = dlib.load_rgb_image(f)

    win.clear_overlay()
    win.set_image(img)

    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))
    frame=cv2.imread(f)
    frame2=cv2.imread(f)
    frame3=cv2.imread(f)
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
        width=d.right()-d.left()
        height=d.bottom()-d.top()
        # Get the landmarks/parts for the face in box d.
        shape = predictor(img, d)
        print("Part 0: {}, Part 1: {} ...".format(shape.part(0),
                                                  shape.part(1)))
        # Draw the face landmarks on the screen.
        #print(shape)
        #print(TEMPLATE)
        #print(frame2.shape)
        for i in range(68):
        	cv2.circle(frame,(shape.part(i).x,shape.part(i).y),1,(0,255,255),-1)
        	cv2.circle(frame2,(int(TEMPLATE[i][0]*width+d.left()+0),int(TEMPLATE[i][1]*height)+d.top()-20),1,(0,0,255),-1)
        	print("HHH",(int(TEMPLATE[i][0]*width+d.left()+20),int(TEMPLATE[i][1]*height)+d.top()-20))
        	LAND[i]=(shape.part(i).x,shape.part(i).y)
        	print("222",(int(TEMPLATE[i][0]*width+d.left()+0),int(TEMPLATE[i][1]*height)+d.top()-20))
        	TMP[i]=(int(TEMPLATE[i][0]*width+d.left()+0),int(TEMPLATE[i][1]*height+d.top()-20))
        	print(TMP[i])
        
        cv2.imshow("68",frame)
        cv2.imshow("sta",frame2)
       
        cv2.imwrite("68-1.jpg",frame)
        cv2.imwrite("68-2.jpg",frame2)
        H=cv2.getAffineTransform(LAND[npLandmarkIndices],TMP[npLandmarkIndices])
        #print("HHH",H)
        #print(LAND[npLandmarkIndices],TMP[npLandmarkIndices])
        thumbnail=cv2.warpAffine(frame3,H,(frame2.shape[1],frame2.shape[0]))
        cv2.imshow("AFF",thumbnail)
        cv2.imwrite("AFF.jpg",thumbnail)
        cv2.waitKey(3000) 
        win.add_overlay(shape)

    win.add_overlay(dets)
    dlib.hit_enter_to_continue()
    '''


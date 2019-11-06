import argparse
import cv2
import numpy as np
import os
import random
import shutil
import Alib
import errno
print("[ALIGN]LOADING MODELS...")

fileDir = os.path.dirname(os.path.realpath(__file__))
print("filedirr",fileDir)
modelDir = os.path.join(fileDir,'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')
print("[ALIGN]LOADED OVER.")

def write(vals, fName):
    if os.path.isfile(fName):
        print("{} exists. Backing up.".format(fName))
        os.rename(fName, "{}.bak".format(fName))
    with open(fName, 'w') as f:
        for p in vals:
            f.write(",".join(str(x) for x in p))
            f.write("\n")

def mkdirP(path):
    assert path is not None
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def alignMain(inputDir,outputDir,landmarks='outerEyesAndNose'):
    mkdirP(outputDir)
    imgs = list(iterImgs(inputDir))

    random.shuffle(imgs)

    landmarkMap = {
        'outerEyesAndNose': Alib.AlignDlib.OUTER_EYES_AND_NOSE,
        'innerEyesAndBottomLip': Alib.AlignDlib.INNER_EYES_AND_BOTTOM_LIP
    }

    if landmarks not in landmarkMap:
        raise Exception("Landmarks unrecognized: {}".format(landmarks))

    landmarkIndices = landmarkMap[landmarks]

    dlibFacePredictor=os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat")
    align = Alib.AlignDlib(dlibFacePredictor)

    nFallbacks = 0
    
    print("[ALIGN]START ALIGNMENT...")
    for imgObject in imgs:
        outDir = os.path.join(outputDir, imgObject.cls)
        mkdirP(outDir)
        outputPrefix = os.path.join(outDir, imgObject.name)
        imgName = outputPrefix + ".png"

        if os.path.isfile(imgName):
            print("[WARINGS]Aleady exsist.")
            pass
        else:
            rgb = imgObject.getRGB()
            if rgb is None:
                print("[ERROR]Unable to load.")
                outRgb = None
            else:
                outRgb = align.align(96, rgb,landmarkIndices=landmarkIndices)
                if outRgb is None:
                    print("[ERROR]Unable to align.")

            if outRgb is not None:
                outBgr = cv2.cvtColor(outRgb, cv2.COLOR_RGB2BGR)
                cv2.imwrite(imgName, outBgr)
                print("[ALIGN]Current end ...")
class Image:
    def __init__(self, cls, name, path):
        assert cls is not None
        assert name is not None
        assert path is not None
        self.cls = cls
        self.name = name
        self.path = path
    def getBGR(self):
        try:
            bgr = cv2.imread(self.path)
        except:
            bgr = None
        return bgr
    def getRGB(self):
        bgr = self.getBGR()
        if bgr is not None:
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        else:
            rgb = None
        return rgb
    def __repr__(self):
        return "({}, {})".format(self.cls, self.name)

def iterImgs(directory):
    assert directory is not None
    exts = [".jpg", ".jpeg", ".png",".pgm"]
    for subdir, dirs, files in os.walk(directory):
        for path in files:
            (imageClass, fName) = (os.path.basename(subdir), path)
            (imageName, ext) = os.path.splitext(fName)
            if ext.lower() in exts:
                yield Image(imageClass, imageName, os.path.join(subdir, fName))

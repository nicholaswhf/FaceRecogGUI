import os
import cv2
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

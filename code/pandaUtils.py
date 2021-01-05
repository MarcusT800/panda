# -*- coding: utf-8 -*-
import cv2 as cv
from panda3d.core import *

def getPandaTexture(img):
    # panda3D texture from camera stream image
    shape = img.shape
    img = cv.flip(img, 0) # cv2 image is upside down
    tex = Texture("detect")
    tex.setCompression(Texture.CMOff) # 1 to 1 copying - default, so is unnecessary
    tex.setup2dTexture(shape[1], shape[0],
                            Texture.TUnsignedByte, Texture.FRgb)#FRgba8) # 3,4 channel
    p = PTAUchar.emptyArray(0)
    p.setData(img)
    tex.setRamImage(CPTAUchar(p)) 
    
    return tex

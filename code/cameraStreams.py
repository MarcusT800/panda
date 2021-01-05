# -*- coding: utf-8 -*-
import cv2 as cv

class cameraStreams:
    def __init__(self):
        self.lastColorFrame = None
        self.cap = cv.VideoCapture('../data/videoCapture/video.mp4')
        
    def updateColorFrame(self, panda):
        success, img = self.cap.read()
        if success:
            self.lastColorFrame = img
        else:
            # Loop video:
            print('End of video, looping')
            #self.cap.set(cv.CAP_PROP_POS_FRAMES, 0) # buggy
            self.cap = cv.VideoCapture('../data/videoCapture/video.mp4') # reload video
            success, img = self.cap.read()
            self.lastColorFrame = img

    def getColorFrame(self):
        return self.lastColorFrame    

    # Used one time in renderAR.py init:
    def getColorImage(self):
        success, img = self.cap.read()
        return img
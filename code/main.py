# -*- coding: utf-8 -*-
import numpy as np
import cv2 as cv
import cv2.aruco as aruco
import math
import time
from direct.showbase.ShowBase import ShowBase # Panda3D
# Inhouse:
from renderAR import * # panda AR renderer
from pandaUtils import * # helper functions
from cameraStreams import cameraStreams # class
from poseEstimation import poseEstimation # class
print ('- Start -')

# ####################################################################################
# MAIN CLASS:
class MainApp(ShowBase):    
    def __init__(self):
        ShowBase.__init__(self)
        # POSE ESTIMATION DATA (updated in poseEstimation.py):
        self.poseData = {
            'pandaCamPose': { # Camera pose in the panda world (calculated from ArUco marker data):
                'trans' : [], # x,y,z
                'rot'   : []  # h,p,r
            }
        }
        # CAMERA/VIDEO STREAM SETUP:
        self.cameraStreams = cameraStreams() # cameraStreams.py class
        # POSE ESTIMATION SETUP:
        self.poseEstimation = poseEstimation() # poseEstimation.py
        # PANDA3D SETUP:
        self.renderAR = renderAR(self) # renderAR.py class
        # RENDER LOOP:
        self.updateTask = taskMgr.add(self.renderLoop, 'renderLoop') # Task manager


    def renderLoop(self, task):
        # GET VIDEO FEED FRAME:
        self.cameraStreams.updateColorFrame(self) # cameraStreams.py
        # WORLD POSE UPDATE (Pose estimation):
        self.poseEstimation.update(self) # poseEstimation.py
        # UPDATE PANDA BACKGROUND VIDEO FEED:
        self.renderAR.updatePandaBackground(self) # renderAR.py
        # UPDATE PANDA CAMERA POSITION:
        self.renderAR.updateCamPos(self) # renderAR.py
        # RETURN LOOP:
        return task.cont


app = MainApp()
app.run()
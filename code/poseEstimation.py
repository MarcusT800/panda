# -*- coding: utf-8 -*-
import cv2 as cv
import cv2.aruco as aruco
from panda3d.core import *
from calibrationData import *

class poseEstimation:
    def __init__(self):
        # Pose estimation data: 
        self.rvecs = []
        self.tvecs = []
        # ArUco SETUP:
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.markerLength = 0.079 # metres
        self.parameters = aruco.DetectorParameters_create()
        self.parameters.cornerRefinementMethod = aruco.CORNER_REFINE_CONTOUR
        self.cameraMatrix = rsCameraMatrix # calibrationData.py
        self.distCoeffs = rsDistCoeffs # calibrationData.py
        self.axisLength = self.markerLength
        self.board0 = aruco.GridBoard_create(
            markersX=2, # number of markers in col
            markersY=2, # -//- row
            markerLength=0.079, # meters
            markerSeparation=0.039, # meters
            dictionary=self.aruco_dict,
            firstMarker=0 # id of first marker in dict to use on board
        )



    # POSE ESTIMATION METHOD:
    def update(self, panda):
        # GET VIDEO FEED RGB IMAGE:
        img = panda.cameraStreams.getColorFrame() # cameraStreams.py

        # Flush last frame pose estimation data:
        self.rvecs = []
        self.tvecs = []

        # Detect markers, returns lists of ids and the corners belonging to each id:
        corners, ids, rejectedImgPoints = aruco.detectMarkers(img, self.aruco_dict, parameters=self.parameters)
        if ids is None:
            # No markers detected in image
            return

        if len(ids) > 3:
            # AR markers detected in image (4 markers in single grid board)
            # Pose estimation (ArUco board):
            retval, self.rvecs, self.tvecs = aruco.estimatePoseBoard( corners, ids, self.board0, self.cameraMatrix, self.distCoeffs, None, None )
            if retval == 0:
                # retval == 0 means the pose has not been estimated
                return
            # Draw board axis:
            img = aruco.drawAxis(img, self.cameraMatrix, self.distCoeffs, self.rvecs, self.tvecs, self.axisLength) 


            # #################################################################################
            # NOTE: POSE DATA CONVERSION STARTS HERE: <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            # Convert rotation vector to a rotation matrix:
            mat, jacobian = cv.Rodrigues(self.rvecs) # cv.Rodrigues docs: https://docs.opencv.org/master/d9/d0c/group__calib3d.html#ga61585db663d9da06b68e70cfbf6a1eac
            # Transpose the matrix (following approach found at stackoverflow):
            mat = cv.transpose(mat) # cv.transpose docs: https://docs.opencv.org/master/d2/de8/group__core__array.html#ga46630ed6c0ea6254a35f447289bd7404
            # Invert the matrix (following approach found at stackoverflow, supposed to convert pose data from marker coordinate space to camera coordinate space): 
            retval, mat = cv.invert(mat) # cv.invert docs: https://docs.opencv.org/master/d2/de8/group__core__array.html#gad278044679d4ecf20f7622cc151aaaa2

            # Create panda matrix so we can apply the data to a node via '.setMat()':
            mat3 = Mat3() 
            mat3.set(mat[0][0], mat[0][1], mat[0][2], mat[1][0], mat[1][1], mat[1][2], mat[2][0], mat[2][1], mat[2][2] )
            mat4 = Mat4(mat3)
            
            # From here on, pretty much all the values are assigned by trial-and-error, to see what works and what doesn't.
            
            # ROTATION:
            # Apply pose estimation rotation matrix to a dummy node:
            panda.matrixNode.setMat( mat4 ) 
            # Apply the matrixNode HPR to another dummy node with some trial-and-error modifications:
            # H=zRot, P=xRot, R=yRot
            panda.transNode.setH( - panda.matrixNode.getR() ) # zRot
            panda.transNode.setP( panda.matrixNode.getP() + 180 ) # xRot
            panda.transNode.setR( - panda.matrixNode.getH() ) # yRot
            
            # TRANSLATION:
            # Place dummy node to a marker position in panda world coordinates (marker is at 0,0,0)
            panda.transNode.setPos(0, 0, 0) 
            # Use translation data from pose estimation:
            xTrans = self.tvecs[0][0]
            yTrans = self.tvecs[1][0]
            zTrans = self.tvecs[2][0]
            # Apply translation with negative values, seems to work (trial-and-error):
            panda.transNode.setPos(panda.transNode, -xTrans, -zTrans, yTrans)


            # SET DATA STRUCTURE (camera position in panda world coordinates):
            camX = panda.transNode.getX()
            camY = panda.transNode.getY()
            camZ = panda.transNode.getZ()
            camH = panda.transNode.getH()
            camP = panda.transNode.getP()
            camR = panda.transNode.getR()
            panda.poseData['pandaCamPose']['trans'] = [camX, camY, camZ] 
            panda.poseData['pandaCamPose']['rot']   = [camH, camP, camR]

            # ... transformation is applied to panda camera in 'renderAR.py' from dataset poseData['pandaCamPose']
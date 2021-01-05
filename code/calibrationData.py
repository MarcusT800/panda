import numpy as np

# CAMERA: ---------------------------------------------------
# camera D435i calibration data for 640x480 res:
cx = 327.812622070313
cy = 240.73991394043
fx = 612.173095703125
fy = 612.461486816406
# opencv requires numpy array:
rsCameraMatrix = np.array([
                [ fx, 0, cx ],
                [ 0, fy, cy ],
                [ 0, 0, 1.0]
                ])
# D435i has undistorted rgb stream:
rsDistCoeffs = np.array([ [0.0], [0.0], [0.0], [0.0], [0.0] ])

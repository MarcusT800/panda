# -*- coding: utf-8 -*-
from direct.gui.OnscreenImage import OnscreenImage
from pandaUtils import * # helper functions

class renderAR:
    def __init__(self, panda):
        self.panda = panda

        # Basic Panda3D setup:
        winProperties = WindowProperties()
        winProperties.setSize( 640, 480 )
        panda.win.requestProperties(winProperties) # applies window properties
        globalClock.setMode(ClockObject.MLimited)
        globalClock.setFrameRate(30) # set Panda framerate to match video framerate
        base.setFrameRateMeter(True)
        panda.disableMouse()
        panda.camLens.setFar(100)
        panda.camLens.setNear(0.001)
        panda.camLens.setFov(55.19465455, 42.79658875)

        # PANDA NODE LIST: 
        '''
        - banner (static blender model, textured cube)
        - pivotNode (dummy node, camera reparented to this node)
        - matrixNode (dummy node to apply matrix operations, gets camera HPR)
        - transNode (dummy node to apply transformations)
            - .transNodeInner (dummy node to apply transformations)
        '''
        
        # *  
        # Banner (BLENDER CUBE MODEL):
        panda.banner = panda.loader.loadModel("../data/models/modelBlender")
        panda.banner.reparentTo(panda.render)
        # *

        # **
        # Pivot (container for camera):
        panda.pivotNode = panda.render.attachNewNode("environ-pivot")
        # panda.pivotNode.setHpr(0,-90, 0) # Rotate node Pitch?
        panda.pivotNode.reparentTo(panda.render)
        # Reparent camera to pivot node:
        panda.camera.reparentTo(panda.pivotNode)
        # **

        # ***        
        # Matrix node (dummy node to apply matrix operations):
        panda.matrixNode = panda.render.attachNewNode("environ-matrix")
        # ***

        # ****
        # Trans node (dummy node to apply transformations):
        panda.transNode = panda.render.attachNewNode("environ-trans")
        # Trans node inner (dummy node to apply transformations):
        panda.transNodeInner = panda.transNode.attachNewNode("environ-trans-inner")
        # ****


        # PANDA BACKGROUND VIDEO FEED CONTAINER:
        # Prepare texture for background image object:
        cameraStreamImage = panda.cameraStreams.getColorImage() # cameraStreams.py class
        # Create Panda3D texture:
        tex = getPandaTexture(cameraStreamImage) # pandaUtils.py helper functions
        panda.bgCamImageObj = OnscreenImage(parent=render2dp, image=tex) # Set background image object, for cam feed texture
        base.cam2dp.node().getDisplayRegion(0).setSort(-20) # Force the rendering to render the background image first (so that it will be put to the bottom of the scene since other models will be necessarily drawn on top)



    # METHODS: ------------------------------------------------------------------------------------------------
    def updatePandaBackground(self, panda):
        # Update panda background texture with video feed image:
        # Get RGB image:
        cameraStreamImage = panda.cameraStreams.getColorFrame() # cameraStreams.py
        # Create Panda3D texture from RGB image:
        tex = getPandaTexture(cameraStreamImage) # pandaUtils.py
        # Apply texture to Panda3D object
        panda.bgCamImageObj.setImage(tex)


    def updateCamPos(self, panda):
        # Update camera position by world pose.
        #   cam is inside container 'panda.pivotNode', we're manipulating the container position
        panda.pivotNode.setX( panda.poseData['pandaCamPose']['trans'][0] )
        panda.pivotNode.setY( panda.poseData['pandaCamPose']['trans'][1] )
        panda.pivotNode.setZ( panda.poseData['pandaCamPose']['trans'][2] )
        panda.pivotNode.setH( panda.poseData['pandaCamPose']['rot'][0] )
        panda.pivotNode.setP( panda.poseData['pandaCamPose']['rot'][1] )
        panda.pivotNode.setR( panda.poseData['pandaCamPose']['rot'][2] )
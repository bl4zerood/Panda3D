from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from panda3d.core import DirectionalLight, AmbientLight
from math import pi, sin, cos
from panda3d.core import WindowProperties
from panda3d.core import CollisionTraverser, CollisionNode, CollisionRay, CollisionHandlerQueue, CollisionBox






def degToRad(degrees):
    return degrees * (pi / 180)
class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.cameraSwingActivated = False
        self.selectedBlockType = 'grass'
        self.lastmouseX = 0
        self.lastmouseY = 0
        self.load_model()
        self.setupCamera()
        self.setupLights()
        self.setupKeyControls()
        self.disableMouse()
        self.taskMgr.add(self.update, "update")
        self.captureMouse()
        for x in range(10):
            for y in range(10):
                for z in range(10):
                    self.createNewBlock(x, y, z, 'dirt')
        

    def load_model(self):
        self.grass = loader.loadModel('grass-block.glb')
        self.dirt = loader.loadModel('dirt-block.glb')
        self.sand = loader.loadModel('sand-block.glb')
        self.stone = loader.loadModel('stone-block.glb')
    
    def createNewBlock(self, x,y,z, type):
        newBlockNode = render.attachNewNode('new-block-placeholder')
        newBlockNode.setPos(x,y,z)


        if type == 'grass': self.grass.instanceTo(newBlockNode)
        elif type == 'dirt': self.dirt.instanceTo(newBlockNode)
        elif type == 'sand': self.sand.instanceTo(newBlockNode)
        elif type == 'stone': self.stone.instanceTo(newBlockNode)
        blockSolid = CollisionBox((-1,-1,-1), (1,1,1))
        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = newBlockNode.attachNewNode(blockNode)
        collider.setPythonTag('owner', newBlockNode)
                
    
    def setupCamera(self):
        self.camera.setPos(0,0,3)
        self.camLens.setFov(80)
        crosshairs = OnscreenImage(image='crosshair.png', pos=(0, 0, 0), scale=0.05)
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

        self.cTrav = CollisionTraverser()
        ray = CollisionRay()
        ray.setFromLens(self.camNode, 0, 0)
        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)
        rayNodePath = self.camera.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)
    
    def setupLights(self):
        directionalLight = DirectionalLight('directionalLight')
        directionalLight.setDirection((-5, -5, -5))
        directionalLight.setColor((1, 1, 1, 1))
        directionalLightNode = render.attachNewNode(directionalLight)
        render.setLight(directionalLightNode)

        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor((0.2, 0.2, 0.2, 1))
        ambientLightNode = render.attachNewNode(ambientLight)
        render.setLight(ambientLightNode)
    
    def update(self, task):
        dt = globalClock.getDt()
        playerMovementSpeed = 10
        x_movement, y_movement, z_movement = 0, 0, 0
        if self.KeyMap["forward"]:
            x_movement -= dt * playerMovementSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMovementSpeed * cos(degToRad(self.camera.getH()))
        if self.KeyMap["backward"]:
            x_movement += dt * playerMovementSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMovementSpeed * cos(degToRad(self.camera.getH()))
        if self.KeyMap["left"]:
            x_movement -= dt * playerMovementSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMovementSpeed * sin(degToRad(self.camera.getH()))
        if self.KeyMap["right"]:
            x_movement += dt * playerMovementSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMovementSpeed * sin(degToRad(self.camera.getH()))
        if self.KeyMap["up"]:
            z_movement += dt * playerMovementSpeed
        if self.KeyMap["down"]:
            z_movement -= dt * playerMovementSpeed
        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement
        )
        if self.cameraSwingActivated:
            md= self.win.getPointer(0)
            mouseX = md.getX()
            mouseY = md.getY()
            mouseChangeX = mouseX - self.lastmouseX
            mouseChangeY = mouseY - self.lastmouseY
            currentH= self.camera.getH()
            currentP= self.camera.getP()
            self.cameraSwingFactor = 100
            self.camera.setHpr(
                currentH - mouseChangeX * dt * self.cameraSwingFactor,
                min(360, max(-360, currentP - mouseChangeY * dt * self.cameraSwingFactor)),0
            )
            self.lastmouseX = mouseX
            self.lastmouseY = mouseY
        return task.cont
    def setupKeyControls(self):
        self.KeyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False
        }
        self.accept("w", self.updateKeyMap, ["forward", True])
        self.accept("w-up", self.updateKeyMap, ["forward", False])
        self.accept("s", self.updateKeyMap, ["backward", True])
        self.accept("s-up", self.updateKeyMap, ["backward", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("space", self.updateKeyMap, ["up", True])
        self.accept("space-up", self.updateKeyMap, ["up", False])
        self.accept("shift", self.updateKeyMap, ["down", True])
        self.accept("shift-up", self.updateKeyMap, ["down", False])
        self.accept('escape', self.releaseMouse)
        self.accept('mouse1', self.removeBlock)
        self.accept('mouse3', self.placeBlock)
        
    
    def updateKeyMap(self, key, value):
        self.KeyMap[key] = value
    
    def captureMouse(self):
        self.cameraSwingActivated = True
        
        md= self.win.getPointer(0)
        self.lastmouseX = md.getX()
        self.lastmouseY = md.getY()

        properties= WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)
        self.win.requestProperties(properties)
    
    def releaseMouse(self):
        self.cameraSwingActivated = False
        properties = WindowProperties()
        properties.setCursorHidden(False)
        properties.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(properties)
    
    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitBlockPos = hitObject.getPos()
                newBlockPos = hitBlockPos + normal * 2
                self.createNewBlock(newBlockPos.x, newBlockPos.y, newBlockPos.z, self.selectedBlockType)
    
    def removeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')
            distanceFromPlayer = hitObject.getDistance(self.camera)

            if distanceFromPlayer < 14:
                hitNodePath.clearPythonTag('owner')
                hitObject.removeNode()


game = Game()
game.run()
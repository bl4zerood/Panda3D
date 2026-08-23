from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from panda3d.core import DirectionalLight, AmbientLight







class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.load_model()
        self.setupCamera()
        self.setupLights()
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
    
    def setupCamera(self):
        self.camera.setPos(0,0,3)
        self.camLens.setFov(80)
        crosshairs = OnscreenImage(image='crosshair.png', pos=(0, 0, 0), scale=0.05)
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)
    
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

game = Game()
game.run()
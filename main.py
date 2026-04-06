import pygame
import math

# I suck at this
# Example file showing a basic pygame "game loop"

# pygame setup
pygame.init()

display = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

cameraX = 0
cameraY = 0

# please please please
gridSizeInPixels = 80

velocityUpdate = "pre" # "pre" or "post"

def resetLevel():
    global floorY,ceilingY
    floorY = 0
    ceilingY = gridSizeInPixels*500
    for block in blocksInLevel:
        block.resetHitbox()

class Player(): # Most likely will be a shell, with a function called "tickPlayer" to actually tick the physics.
    # actually nevermind that comment. I want to do many, many things with this?
    def __init__(self):
        #GAMEPLAY
        #use center to position rects
        self.x = -gridSizeInPixels*8
        self.y = 40
        self.yVelocity = 0 # there is no x velocity dum dum
        self.gamemode = "cube"
        self.grounded = False
        self.mini = False
        self.gravity = 1 # 1 = normal gravity, -1 = flipped gravity, 0 = wuttttt
        self.speed = (gridSizeInPixels*10.3761348898)/60 # adjust later
        self.rotation = 90 # in degrees
        self.orbBuffer = False # If can orb buffer
        # \|/ change these based on gamemode
        self.maxYVel = 100
        self.minYVel = -100

        # Gamemode dependent variables
        # self.terminalVelocity = 100 # cube terminal velocity

        #LOCKED
        self.cubeSize = gridSizeInPixels

        # TODO: Move these into gameplay constants class possibly?
        # Probably not
        self.baseGravity = 2.1 #adjusttt
        self.jumpForce = 26.5 #adjust

        #Hitboxrects
        self.damageHitboxRect = pygame.Rect(0,0,self.cubeSize,self.cubeSize)
        self.dhrOffsets = [0,0] #hitbox offset. Like when I move it to current (in updatehitbox) it does that.
        
        self.specialHitboxRect = pygame.Rect(0,0,self.cubeSize,self.cubeSize)
        self.shrOffsets = [0,0]

        self.blockHurtHitboxRect = pygame.Rect(0,0,self.cubeSize*0.3,self.cubeSize*0.3)
        self.bhhrOffsets = [0,0]

        self.floorHitboxRect = pygame.Rect(0,0,self.cubeSize,2)
        self.fhrOffsets = [0,(self.cubeSize*0.5)-1]

        self.ceilingHitboxRect = pygame.Rect(0,0,self.cubeSize,2)
        self.chrOffsets = [0,1-(self.cubeSize*0.5)]
        
        #self.sprite = pygame.sprite.Sprite()
        #pygame.sprite.Sprite.__init__(self.sprite)
        #self.sprite.add(spriteGroup)
        self.imageIdiot = pygame.image.load("./resources/icons/missing.png").convert_alpha()

        return
    def update(self):
        #Stupid sprite
        return
    def resetGameplayVariables(self):
        self.x = -gridSizeInPixels*8
        self.y = 40
        self.yVelocity = 0
        self.gamemode = "cube"
        self.grounded = False
        self.mini = False
        self.gravity = 1
        self.speed = (gridSizeInPixels*10.3761348898)/60
        self.rotation = 90
    def die(self):
        print("I'm dead!")
        self.resetGameplayVariables()
        resetLevel() # cus classes
    def updateHitbox(self): # kinda like scratch gd (NOT PHYSICS)
        # bean
        self.damageHitboxRect.center = (self.x + self.dhrOffsets[0], -self.y + self.dhrOffsets[1])
        self.specialHitboxRect.center = (self.x + self.shrOffsets[0], -self.y + self.shrOffsets[1])
        self.blockHurtHitboxRect.center = (self.x + self.bhhrOffsets[0], -self.y + self.bhhrOffsets[1])
        self.floorHitboxRect.center = (self.x + self.fhrOffsets[0], -self.y + self.fhrOffsets[1])
        self.ceilingHitboxRect.center = (self.x + self.chrOffsets[0], -self.y + self.chrOffsets[1])
        """self.damageHitboxRect.update()
        self.specialHitboxRect.update()
        self.blockHurtHitboxRect.update()
        self.floorHitboxRect.update()
        self.ceilingHitboxRect.update()"""
        return
    def blitIcon(self):
        tempImage = pygame.transform.scale(self.imageIdiot,[self.cubeSize,self.cubeSize])
        tempImage = pygame.transform.rotate(tempImage,-(self.rotation-90)%360)
        tempRect = pygame.Rect(0,0,self.cubeSize,self.cubeSize)
        tempRect.center = (self.x-cameraX,-self.y+cameraY)
        tempRect = tempImage.get_rect(center=tempRect.center)
        #self.sprite.update(rect=tempRect,image=tempImage)
        display.blit(tempImage,tempRect)
    def physicsTick(self): # physicstick
        #for block in blocksInLevel:
            #block.updateHitbox()
        # tick velocity
        global floorY,ceilingY
        currentGamemode = self.gamemode

        if velocityUpdate == "pre":
            self.y += self.yVelocity*dMult # DO NOT PUT A DELTA MULTIPLIER ON THIS DO NOT PUT IT ON THERE PLEASE
            self.x += self.speed*dMult
            self.updateHitbox() #update hitbox because ye

        #orb bufferism
        # Also make sure this stays up here, not after the block check because it causes the next orb to buffer
        # Also problem with the next block of code because "self.grounded = False"
        if mouseClick and not self.grounded:
            #print("orb buffer enabled")
            self.orbBuffer = True
            self.clickBuffer = True
        if (not mouseHeld) or self.grounded:
            #print("orb buffer disabled roses")
            self.orbBuffer = False
            self.clickBuffer = False

        floorHitbox = self.floorHitboxRect
        ceilingHitbox = self.ceilingHitboxRect
        if (self.gravity/abs(self.gravity)) == -1:
            floorHitbox = self.ceilingHitboxRect
            ceilingHitbox = self.floorHitboxRect

        # TODO: this collide with floor so we can change floor height

        theFloorSon = floorY
        theCeilingSon = ceilingY
        if self.gravity/abs(self.gravity) == -1:
            theFloorSon = ceilingY
            theCeilingSon = floorY

        if floorHitbox.centery*(self.gravity/abs(self.gravity)) >= -theFloorSon*(self.gravity/abs(self.gravity)):
            self.grounded = True
            self.y += ((floorHitbox.centery+theFloorSon)-self.gravity/abs(self.gravity))
        else:
            self.grounded = False

        if currentGamemode == "ball":
            if ceilingHitbox.centery*(self.gravity/abs(self.gravity))<= -theCeilingSon*(self.gravity/abs(self.gravity)):
                self.y += ceilingHitbox.centery+theCeilingSon-self.gravity/abs(self.gravity)
                self.yVelocity = 0

        
        collidableBlocks = []
        for block in blocksInLevel:
            if abs(block.x-self.x) < 80*3 and abs(block.y-self.y) < 80*3:
                collidableBlocks.append(block)
        
        for block in collidableBlocks:
            if block.blockHitboxRect != False:
                f = abs(floorHitbox.centery-block.blockHitboxRect.top)
                if (self.gravity/abs(self.gravity)) == -1:
                    f = abs(floorHitbox.centery-block.blockHitboxRect.bottom)
                """isInHitrange = abs(floorHitbox.centery-block.blockHitboxRect.top) < 20
                if (self.gravity/abs(self.gravity)) == -1:
                    isInHitrange = abs(floorHitbox.centery-block.blockHitboxRect.bottom) < 20
                """
                isInHitrange = f < 20+abs(self.yVelocity)
                #if not pygame.Rect(floorHitbox.x,floorHitbox.y,floorHitbox.width,floorHitbox.height).colliderect(block.blockHitboxRect) and abs(self.yVelocity) > 10:
                    #isInHitrange = True
                if floorHitbox.colliderect(block.blockHitboxRect) == True and isInHitrange and self.yVelocity*(self.gravity/abs(self.gravity)) <= 0:
                    self.grounded = True
                    exit = False
                    originalY = self.y
                    while not exit:
                        self.y += (self.gravity/abs(self.gravity))
                        self.updateHitbox()
                        if not floorHitbox.colliderect(block.blockHitboxRect):
                            exit = True
                            self.y -= (self.gravity/abs(self.gravity))
                            #if abs(originalY-self.y) > 20:
                                #self.y = originalY
                if self.blockHurtHitboxRect.colliderect(block.blockHitboxRect) == True:
                    self.die()
            if block.damageHitboxRect != False:
                if self.damageHitboxRect.colliderect(block.damageHitboxRect) == True:
                    self.die()
            if block.specialHitboxRect != False:
                touchingCase = self.specialHitboxRect.colliderect(block.specialHitboxRect)
                orbCase = touchingCase and (mouseClick == True or self.orbBuffer == True)
                def disableOrb():
                    global mouseClick
                    self.orbBuffer = False
                    mouseClick = False
                    self.grounded = False
                    block.specialHitboxRect = False
                    return
                match block.blockType:
                    case "blueRing":
                        if orbCase:
                            disableOrb()
                            self.gravity *= -1
                            self.yVelocity = -10*(self.gravity/abs(self.gravity))
                    case "yellowRing":
                        if orbCase:
                            disableOrb()
                            self.yVelocity = self.jumpForce*(self.gravity/abs(self.gravity))
                    case "pinkRing":
                        if orbCase:
                            disableOrb()
                            self.yVelocity = 18*(self.gravity/abs(self.gravity)) #17-20 range
                    case "portalBall":
                        if touchingCase:
                            block.specialHitboxRect = False
                            self.gamemode = "ball"
                            floorY = round((block.y-40)/80)*80 - 3*80
                            ceilingY = round((block.y-40)/80)*80 + 4*80
        
        if not self.grounded:
            self.yVelocity -= self.gravity*self.baseGravity*dMult
        else:
            #manual minimum fucking retard
            if self.yVelocity*(self.gravity/abs(self.gravity)) < 0:
                self.yVelocity = 0
        
        match currentGamemode:
            case "cube":
                if not self.grounded:
                    self.rotation += 7*self.gravity*dMult
                else:
                    self.rotation = (round(self.rotation/90)*90)%360
            case "ball":
                self.rotation += 7*self.gravity*(self.grounded*2-1)*dMult
            

        #terminal velocity
        if self.yVelocity > self.maxYVel:
            self.yVelocity = self.maxYVel
        if self.yVelocity < self.minYVel:
            self.yVelocity = -self.minYVel

        if mouseHeld and self.grounded and currentGamemode == "cube":
            #jump
            self.yVelocity = self.jumpForce*(self.gravity/abs(self.gravity))
            pass

        if (mouseClick or self.clickBuffer) and self.grounded:
            match currentGamemode:
                case "ball":
                    self.gravity *= -1
                    self.clickBuffer = False

        if velocityUpdate == "post":
            self.y += self.yVelocity*dMult
            self.x += self.speed*dMult
            self.updateHitbox()
        #print(self.grounded)
        return
    # def jump(): (Like an idiot would...)

class Block():
    def __init__(self,x,y,blocktype,texture,rotation,scale):
        self.x = x
        self.y = y
        ## self.texture = "./blocks/square_01_001.png"
        self.blockType = blocktype
        self.textureStr = texture
        self.textureImage = pygame.image.load(self.textureStr).convert_alpha()
        self.scale = scale # multiplier
        self.rotation = rotation
        self.blockSize = gridSizeInPixels*self.scale

        self.blockHitboxRect = False
        self.bhOffsets = [0,0]

        self.damageHitboxRect = False
        self.dhOffsets = [0,0]
        
        self.specialHitboxRect = False
        self.shOffsets = [0,0]

        self.textureOffsets = self.getTextureOffsets()

        self.imageCache = {}

        self.resetHitbox()
        return
    def getTextureOffsets(self,textureString=False):
        # scales should be based on if the block is one grid size long, and multiply for scale and rotation and whatnot
        if not textureString:
            textureString = self.textureStr
        return {
            "spike_02_001.png": [0,22]
        }.get(str.split(textureString,"/")[3],[0,0])
    def rotateOffsets(self,offsets=False): #by default it does texture offsets
        if offsets == False:
            offsets = self.textureOffsets
        roundedRotation = (round(-(self.rotation - 90)/90)*90)%360
        match roundedRotation:
            case 0:
                return offsets
            case 90:
                return [offsets[1],-offsets[0]]
            case 180:
                return [-offsets[0],-offsets[1]]
            case 270:
                return [-offsets[1],offsets[0]]
    def rotateSize(self,sizeX,sizeY):
        roundedRotation = (round(-(self.rotation - 90)/90)*90)%180
        match roundedRotation:
            case 0:
                return (sizeX,sizeY)
            case 90:
                return (sizeY,sizeX)
    def resetHitbox(self):
        # TODO: Maybe make this better using the dict method from getTextureOffsets?
        self.imageCache = {}
        match self.blockType:
            case "fullBlock":
                self.blockHitboxRect = pygame.Rect(0,0,self.blockSize,self.blockSize)
                self.bhOffsets = [0,0]
            case "fullSpike":
                self.damageHitboxRect = pygame.Rect(0,0,self.blockSize*0.2,self.blockSize*0.4)
                self.dhOffsets = [0,0]
            case "blueRing":
                self.specialHitboxRect = pygame.Rect(0,0,self.blockSize*1.2,self.blockSize*1.2)
                self.shOffsets = [0,0]
            case "yellowRing":
                self.specialHitboxRect = pygame.Rect(0,0,self.blockSize*1.2,self.blockSize*1.2)
                self.shOffsets = [0,0]
            case "pinkRing":
                self.specialHitboxRect = pygame.Rect(0,0,self.blockSize*1.2,self.blockSize*1.2)
                self.shOffsets = [0,0]
            case "smallSpike":
                self.damageHitboxRect = pygame.Rect(0,0,self.blockSize*0.3,self.blockSize*0.2)
                self.dhOffsets = [0,20*self.scale]
            case "portalBall":
                self.specialHitboxRect = pygame.Rect(0,0,self.blockSize*0.8,self.blockSize*2.7)
                self.shOffsets = [0,0]
        #self.bhOffsets = self.rotateOffsets(self.bhOffsets)
        #self.dhOffsets = self.rotateOffsets(self.dhOffsets)
        #self.shOffsets = self.rotateOffsets(self.shOffsets)
        #print("resetting hitboxes")
        if self.blockHitboxRect:
            rotX,rotY = self.rotateSize(self.blockHitboxRect.width,self.blockHitboxRect.height)
            self.blockHitboxRect.update((0,0,rotX,rotY))
        if self.damageHitboxRect:
            rotX,rotY = self.rotateSize(self.damageHitboxRect.width,self.damageHitboxRect.height)
            self.damageHitboxRect.update((0,0,rotX,rotY))
        if self.specialHitboxRect:
            rotX,rotY = self.rotateSize(self.specialHitboxRect.width,self.specialHitboxRect.height)
            self.specialHitboxRect.update((0,0,rotX,rotY))
        self.updateHitbox()
    def updateHitbox(self):
        rotBHOffsets,rotDHOffsets,rotSHOffsets = self.rotateOffsets(self.bhOffsets),self.rotateOffsets(self.dhOffsets),self.rotateOffsets(self.shOffsets)
        if self.blockHitboxRect:
            self.blockHitboxRect.center = (self.x+rotBHOffsets[0],-self.y+rotBHOffsets[1])
        if self.damageHitboxRect:
            self.damageHitboxRect.center = (self.x+rotDHOffsets[0],-self.y+rotDHOffsets[1])
        if self.specialHitboxRect:
            self.specialHitboxRect.center = (self.x+rotSHOffsets[0],-self.y+rotBHOffsets[1])
    def blitTexture(self):
        if not ((cameraX+300)-self.x < 80*5 and (cameraX+300)-self.x > -80*13 and (cameraY-520)-self.y < 80*4 and (cameraY-520)-self.y > -80*7):
            return
        # Make this work with textures not block sized
        # basically just 120 is the base size in the textures, 80 is the base size here. Do the math
        if not self.imageCache.get("tempImage",False):
            sizeWidth,sizeHeight = (self.textureImage.get_width() * 80/120,self.textureImage.get_height() * 80/120) # convert uhd
            #tempImage = pygame.transform.scale(self.textureImage,[self.blockSize,self.textureImage.get_height()*(self.blockSize/self.textureImage.get_width())])
            tempImage = pygame.transform.scale(self.textureImage,(sizeWidth,sizeHeight))
            tempImage = pygame.transform.rotate(tempImage,-(self.rotation-90)%360)
            self.imageCache["tempImage"] = tempImage
        tempImage = self.imageCache["tempImage"]
        tempRect = pygame.Rect(0,0,self.blockSize,self.blockSize)
        #print(self.blockType + ": " + str(self.textureOffsets[0]) + ", " + str(self.textureOffsets[1]))
        rotTexOffsets = self.rotateOffsets(self.textureOffsets)
        tempRect.center = (self.x-cameraX + rotTexOffsets[0],-self.y+cameraY + rotTexOffsets[1])
        tempRect = tempImage.get_rect(center=tempRect.center)
        #self.sprite.update(rect=tempRect,image=tempImage)
        #print(self.x-player1.x)
        #print("op:")
        #print(player1.x-self.x)
        display.blit(tempImage,tempRect)

player1 = Player()
player1.__init__()

"""blocksInLevel = [
    Block(80*2,40,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*2,40+80,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*3,40+80,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*4,40+80,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*5,40+80,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*6,40+80,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*6,40+80*2,"fullSpike","./resources/blocks/spike_01_001.png",90,1),
    Block(80*7,40+80,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*7,40+80*2,"fullSpike","./resources/blocks/spike_01_001.png",90,1),
    Block(80*8,40+80,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*8,40+80*2,"fullSpike","./resources/blocks/spike_01_001.png",90,1),
    Block(80*9,40+80,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*10,40+80,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*11,40+80,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*13,40+80,"blueRing","./resources/blocks/gravring_01_001.png",90,1),
    Block(80*14,40+80*4,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*15,40+80*4,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*16,40+80*4,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*17,40+80*4,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*18,40+80*4,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*19,40+80*3.9,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*20,40+80*3.8,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*21,40+80*3.7,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*21,40+80*3.7,"blueRing","./resources/blocks/gravring_01_001.png",90,1),
    Block(80*22,40+80*3.6,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*23,40+80*3.5,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*24,40+80*3.4,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*25,40+80*3.3,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*26,40+80*3.2,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*27,40+80*3.1,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*28,40+80*3,"fullBlock","./resources/blocks/square_01_001.png",90,1),
    Block(80*34,40+80*2,"yellowRing","./resources/blocks/ring_01_001.png",90,1),
    Block(80*38,40,"smallSpike","./resources/blocks/spike_02_001.png",90,1)
]
tsblock = Block(80*39,40,"smallSpike","./resources/blocks/spike_02_001.png",0,1)
blocksInLevel.append(tsblock)"""

"""blocksInLevel = [
    Block(0,40+80*5,"fullBlock","./resources/blocks/square_01_001.png",1),
    Block(-80*1,40+80*5,"fullBlock","./resources/blocks/square_01_001.png",1),
    Block(-80*2,40+80*5,"fullBlock","./resources/blocks/square_01_001.png",1),
    Block(-80*3,40+80*5,"fullBlock","./resources/blocks/square_01_001.png",1),
    Block(-80*4,40+80*5,"fullBlock","./resources/blocks/square_01_001.png",1),
    Block(-80*5,40+80*5,"fullBlock","./resources/blocks/square_01_001.png",1),
]"""

blocksInLevel = []

def sortBlocks(): # This is so I can do some magic so performance goes up, do this at the start of the game, never again oke?
    global blocksInLevel
    blocksClone = blocksInLevel.copy()
    sortedList = []
    
    done = False
    #iterations = 0
    while not done:
        #if iterations > 1000:
            #print("Sorting Failed!")
            #done = True
        if blocksClone.__len__() == 0:
            done = True
        lowest = False
        for block in blocksClone:
            #currentIndex = blocksClone.index(block)
            if not lowest:
                lowest = block
                continue
            if block.x < lowest.x:
                lowest = block
        if lowest:
            sortedList.append(lowest)
            blocksClone.remove(lowest)
    return sortedList

"""blocksInLevel = [
    Block(20,0,"fullblock","./resources/blocks/square_01_001.png",90,1),
    Block(0,0,"fullblock","./resources/blocks/square_01_001.png",90,1),
    Block(60,0,"fullblock","./resources/blocks/square_01_001.png",90,1),
    Block(-60,0,"fullblock","./resources/blocks/square_01_001.png",90,1)
]"""

blocksInLevel = sortBlocks()

for block in blocksInLevel:
    print(block.x, blocksInLevel.index(block))

def lerp(x,y,alpha):
    return x + (y - x)*alpha

def perFrameUpdate():
    player1.physicsTick()

def updateCamera():
    global cameraX
    global cameraY
    cameraX = player1.x - 300
    if not editorMode:
        if abs(ceilingY - floorY) < 1280:
            cameraY = (floorY+ceilingY)/2+720/2
            return
        yPosOnScreen = abs(-player1.y+cameraY)
        if (yPosOnScreen<200):
            cameraY+=((200-yPosOnScreen)/10)*dMult
        if (-player1.y+cameraY>720-200):
            cameraY-=((-player1.y+cameraY-520)/10)*dMult
        return
    cameraY = lerp(cameraY,player1.y + 720 - 200,0.3*dMult)

showHitboxes = True

def drawHitboxes():
    def drawTransparentRect(rect,color):
        newRect = pygame.Rect(0,0,rect.width,rect.height)
        newRect.center = (rect.center[0]-cameraX,rect.center[1]+cameraY)
        surface = pygame.Surface(newRect.size)
        surface.set_alpha(128)
        surface.fill(color)
        display.blit(surface, newRect.topleft)
    for block in blocksInLevel:
        if block.blockHitboxRect:
            """newRect = pygame.Rect(0,0,block.blockHitboxRect.width,block.blockHitboxRect.height)
            newRect.center = (block.blockHitboxRect.center[0]-cameraX,block.blockHitboxRect.center[1]+cameraY)
            surface = pygame.Surface(newRect.size)
            surface.set_alpha(128)
            surface.fill((255,255,0))
            display.blit(surface, newRect.topleft)"""
            drawTransparentRect(block.blockHitboxRect,(255,255,0))
            #pygame.draw.rect(display,(255,255,0),newRect)
        if block.damageHitboxRect:
            """newRect = pygame.Rect(0,0,block.damageHitboxRect.width,block.damageHitboxRect.height)
            newRect.center = (block.damageHitboxRect.center[0]-cameraX,block.damageHitboxRect.center[1]+cameraY)
            surface = pygame.Surface(newRect.size)
            surface.set_alpha(128)
            surface.fill((255,0,0))
            display.blit(surface, newRect.topleft)"""
            drawTransparentRect(block.damageHitboxRect,(255,0,0))
            #pygame.draw.rect(display,(255,0,0),newRect)
        if block.specialHitboxRect:
            """newRect = pygame.Rect(0,0,block.specialHitboxRect.width,block.specialHitboxRect.height)
            newRect.center = (block.specialHitboxRect.center[0]-cameraX,block.specialHitboxRect.center[1]+cameraY)
            surface = pygame.Surface(newRect.size)
            surface.set_alpha(128)
            surface.fill((0,255,0))
            display.blit(surface, newRect.topleft)"""
            drawTransparentRect(block.specialHitboxRect,(0,255,0))
            #pygame.draw.rect(display,(0,255,0),newRect)
    drawTransparentRect(player1.damageHitboxRect,(255,0,0))
    drawTransparentRect(player1.ceilingHitboxRect,(0,255,0))
    drawTransparentRect(player1.floorHitboxRect,(0,255,0))
    drawTransparentRect(player1.blockHurtHitboxRect,(0,0,255))
    

floorY = 0
ceilingY = gridSizeInPixels*500

def drawDisplay():
    for block in blocksInLevel:
        block.blitTexture()
    if showHitboxes:
        drawHitboxes()
    #draw ground
    groundRect = pygame.Rect(0,0,1280,400)
    groundRect.topleft = (0,-floorY+cameraY)
    pygame.draw.rect(display,(255,0,0),groundRect)

    ceilingRect = pygame.Rect(0,0,1280,400)
    ceilingRect.bottomleft = (0,-ceilingY+cameraY)
    pygame.draw.rect(display,(255,0,0),ceilingRect)

    player1.blitIcon()

    font = pygame.font.Font("./resources/fonts/MSGOTHIC.TTC",28)
    def renderBoldFont(string,x,y):
        logoStr = string
        font.set_bold(800)
        surface = font.render(logoStr,True,(255,255,255))
        font.bold = False
        surface2 = font.render(logoStr,True,(0,0,0))
        display.blit(surface,(x-abs(surface.get_size()[0]-surface2.get_size()[0]),y-abs(surface.get_size()[1]-surface2.get_size()[1])))
        display.blit(surface2,(x,y))
    renderBoldFont("PyDash made by rschoolu",0,0)
    renderBoldFont("FPS: " + str(round(60/dMult)) + "/" + str(fps),0,30)
    #renderBoldFont("Debug",0,30*2)
    #renderBoldFont("playerX: " + str(player1.x) + " playerY: " + str(player1.y),0,30*3)
    
    #pygame.draw.rect(display,(0,255,0),player1.specialHitboxRect)
    #pygame.draw.rect(display,(255,255,0),player1.floorHitboxRect)

mouseClick = False
mouseHeld = False

fps = 240 # game fps
dMult = 1/fps

editorMode = True

#realCursorX, realCursorY = 0,0

blockTypeTexture = {
    "fullBlock": "./resources/blocks/square_01_001.png",
    "fullSpike": "./resources/blocks/spike_01_001.png",
    "blueRing": "./resources/blocks/gravring_01_001.png",
    "yellowRing": "./resources/blocks/ring_01_001.png",
    "pinkRing": "./resources/blocks/ring_03_001.png",
    "smallSpike": "./resources/blocks/spike_02_001.png",
    "portalBall": "./resources/blocks/spike_02_001.png", #placeholder
}

class EditorBrush(): #for editor
    def __init__(self):
        self.x = 0
        self.y = 0
        self.blockType = "fullBlock"
        self.texture = blockTypeTexture.get(self.blockType)
        self.rotation = 90
        self.scale = 1
        self.mode = "draw"
        self.selectedBlockIndex = 0 #index in blocksInLevel
        self.textureImage = pygame.image.load(self.texture).convert_alpha()
    def updateTexture(self):
        self.texture = blockTypeTexture.get(self.blockType)
        self.textureImage = pygame.image.load(self.texture).convert_alpha()
    def updatePosition(self):
        screenCursorX, screenCursorY = pygame.mouse.get_pos()
        self.x, self.y = (screenCursorX+cameraX,-screenCursorY+cameraY)
    def cycleBlockType(self,back=False):
        self.blockType = list(blockTypeTexture.keys())[(list(blockTypeTexture.keys()).index(self.blockType)+(((not back)*2)-1))%(list(blockTypeTexture.keys()).__len__())]
        self.texture = blockTypeTexture.get(self.blockType)
        self.updateTexture()
    def paint(self):
        collisionRect = pygame.Rect(self.x-cameraX,-self.y+cameraY,1,1)
        if collisionRect.colliderect(buildButtonRect):
            self.mode = "draw"
            return
        if collisionRect.colliderect(editButtonRect):
            self.mode = "edit"
            return
        match self.mode:
            case "draw":
                self.placeBlock()
            case "edit":
                self.selectBlock()
    def selectBlock(self):
        collisionRect = pygame.Rect(self.x-cameraX,-self.y+cameraY,1,1)
        for block in blocksInLevel:
            if blocksInLevel.index(block) == blocksInLevel[self.selectedBlockIndex]:
                continue
            newRect = pygame.Rect(0,0,80,80)
            newRect.center = (block.x-cameraX,-block.y+cameraY)
            if collisionRect.colliderect(newRect):
                self.selectedBlockIndex = blocksInLevel.index(block)
                break
    def blitSelectedBlock(self):
        if self.selectedBlockIndex == -1:
            return
        if self.selectedBlockIndex > blocksInLevel.__len__()-1:
            self.selectedBlockIndex = -1
            return
        surface = pygame.Surface((80,80))
        surface.fill((255,255,255))
        surface.set_alpha(128)
        screenX = blocksInLevel[self.selectedBlockIndex].x-cameraX
        screenY = -blocksInLevel[self.selectedBlockIndex].y+cameraY
        display.blit(surface,(screenX-40,screenY-40))
    def placeBlock(self):
        newBlock = Block(round(self.x/80)*80,round((self.y-40)/80)*80+40,self.blockType,self.texture,self.rotation,self.scale)
        blocksInLevel.append(newBlock)
        self.selectedBlockIndex = blocksInLevel.index(newBlock)
    def editSelectedObject(self,xPos=0,yPos=0,rotation=0,scale=0):
        if self.selectedBlockIndex == -1:
            return
        block = blocksInLevel[self.selectedBlockIndex]
        block.x += xPos
        block.y += yPos
        block.rotation += rotation
        block.rotation %= 360
        block.scale += scale
        block.resetHitbox()
        return
    def blitBrush(self):
        if self.mode == "edit":
            return
        sizeWidth,sizeHeight = (self.textureImage.get_width() * 80/120,self.textureImage.get_height() * 80/120) # convert uhd
        #tempImage = pygame.transform.scale(self.textureImage,[self.blockSize,self.textureImage.get_height()*(self.blockSize/self.textureImage.get_width())])
        tempImage = pygame.transform.scale(self.textureImage,(sizeWidth,sizeHeight))
        tempImage = pygame.transform.rotate(tempImage,-(self.rotation-90)%360)
        tempRect = pygame.Rect(0,0,self.scale*80,self.scale*80)
        rotTexOffsets = Block.rotateOffsets(self,Block.getTextureOffsets(self,self.texture))
        tempRect.topleft = (self.x-cameraX + rotTexOffsets[0],-self.y+cameraY + rotTexOffsets[1])
        tempRect = tempImage.get_rect(center=tempRect.center)
        display.blit(tempImage,tempRect)
    def erase(self): #no point
        collisionRect = pygame.Rect(self.x-cameraX,-self.y+cameraY,1,1)
        for block in blocksInLevel:
            newRect = pygame.Rect(0,0,80,80)
            newRect.center = (block.x-cameraX,-block.y+cameraY)
            if collisionRect.colliderect(newRect):
                currentSelectedBlock = "not a block lmao"
                if self.selectedBlockIndex > -1:
                    currentSelectedBlock = blocksInLevel[self.selectedBlockIndex]
                blocksInLevel.remove(block)
                if block != currentSelectedBlock and self.selectedBlockIndex > -1:
                    self.selectedBlockIndex = blocksInLevel.index(currentSelectedBlock)
                else:
                    self.selectedBlockIndex = -1
                break

currentBrush = EditorBrush()

def editorDrawPre():
    for i in range(17):
        vRect = pygame.Rect(0,0,3,720)
        vRect.centerx = 80*i+round((cameraX+300)/80)*80-40-80*3-cameraX
        #vRect.centerx = -40+80*i+round((player1.x)/80)*80-80*3-cameraX
        pygame.draw.rect(display,(255,255,0),vRect)
    for i in range(9):
        hRect = pygame.Rect(0,0,1280,3)
        hRect.centery = 80*i+round(-(cameraY-520)/80)*80-80*6+cameraY
        pygame.draw.rect(display,(255,255,0),hRect)
    spawnRect = pygame.Rect(0,0,40,40)
    spawnRect.center = (-gridSizeInPixels*8-cameraX,-40+cameraY)
    pygame.draw.rect(display,(0,255,0),spawnRect)

buildButtonRect = pygame.Rect(0,0,200,50)
buildButtonRect.topright = (1280-40,40)

editButtonRect = pygame.Rect(0,0,200,50)
editButtonRect.topright = (1280-40,40 + buildButtonRect.height*1.1)

def editorDrawPost():
    currentBrush.blitBrush()
    currentBrush.blitSelectedBlock()

    #Draw buttons:
    font = pygame.font.Font("./resources/fonts/MSGOTHIC.TTC",30)
    buildText = font.render("Draw Mode",True,(0,0,0))

    editText = font.render("Edit Mode",True,(0,0,0))

    drawColor = False
    editColor = False
    if currentBrush.mode == "draw":
        drawColor = (0,255,0)
        editColor = (255,255,255)
    else:
        drawColor = (255,255,255)
        editColor = (0,255,0)

    pygame.draw.rect(display,drawColor,buildButtonRect)
    display.blit(buildText,(buildButtonRect.centerx-buildText.get_width()/2,buildButtonRect.centery-buildText.get_height()/2))

    pygame.draw.rect(display,editColor,editButtonRect)
    display.blit(editText,(editButtonRect.centerx-editText.get_width()/2,editButtonRect.centery-editText.get_height()/2))

def editorLoop():
    global keys, mouse
    global prevKeys, prevMouse
    global showHitboxes
    speed = 10
    if (keys[pygame.K_LSHIFT]):
        speed = 1
    if currentBrush.mode == "edit":
        speed = 0
    player1.y += (speed*dMult)*(keys[pygame.K_w])
    player1.y -= (speed*dMult)*(keys[pygame.K_s])
    player1.x += (speed*dMult)*(keys[pygame.K_d])
    player1.x -= (speed*dMult)*(keys[pygame.K_a])
    
    currentBrush.updatePosition()

    if keys[pygame.K_e] and not prevKeys[pygame.K_e]:
        match currentBrush.mode:
            case "draw":
                currentBrush.rotation += 90/(keys[pygame.K_LSHIFT]+1)
                currentBrush.rotation %= 360
            case "edit":
                currentBrush.editSelectedObject(rotation=90/(keys[pygame.K_LSHIFT]+1))
    if keys[pygame.K_q] and not prevKeys[pygame.K_q]:
        match currentBrush.mode:
            case "draw":
                currentBrush.rotation -= 90/(keys[pygame.K_LSHIFT]+1)
                currentBrush.rotation %= 360
            case "edit":
                currentBrush.editSelectedObject(rotation=-90/(keys[pygame.K_LSHIFT]+1))

    if currentBrush.mode == "edit":
        moveMultiplier = 1/((keys[pygame.K_LSHIFT]*9)+1)
        if keys[pygame.K_w] and not prevKeys[pygame.K_w]:
            currentBrush.editSelectedObject(yPos=gridSizeInPixels*moveMultiplier)
        if keys[pygame.K_a] and not prevKeys[pygame.K_a]:
            currentBrush.editSelectedObject(xPos=-gridSizeInPixels*moveMultiplier)
        if keys[pygame.K_s] and not prevKeys[pygame.K_s]:
            currentBrush.editSelectedObject(yPos=-gridSizeInPixels*moveMultiplier)
        if keys[pygame.K_d] and not prevKeys[pygame.K_d]:
            currentBrush.editSelectedObject(xPos=gridSizeInPixels*moveMultiplier)
    
    if mouse[2] and not prevMouse[2]:
        currentBrush.erase()

    if keys[pygame.K_f] and not prevKeys[pygame.K_f]:
        currentBrush.cycleBlockType()
    if keys[pygame.K_r] and not prevKeys[pygame.K_r]:
        currentBrush.cycleBlockType(True)
    if keys[pygame.K_h] and not prevKeys[pygame.K_h]:
        showHitboxes = not showHitboxes

    if mouseClick:
        currentBrush.paint()

mouse = pygame.mouse.get_pressed()
keys = pygame.key.get_pressed()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    prevMouse = mouse
    prevKeys = keys
    mouse = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_g] and not prevKeys[pygame.K_g]:
        editorMode = not editorMode
        if not editorMode:
            for block in blocksInLevel:
                block.resetHitbox()
            player1.yVelocity = 0


    #everything at the end of time
    if not editorMode:
        perFrameUpdate()
    else:
        editorLoop()
    updateCamera()

    display.fill("blue")
    
    inputValue = pygame.mouse.get_pressed()[0]
    if mouseHeld != inputValue and inputValue == True:
        mouseClick = True
    elif mouseHeld == inputValue and inputValue == True:
        mouseHeld = True
        mouseClick = False
    mouseHeld = inputValue

    if editorMode:
        editorDrawPre()
    drawDisplay()
    if editorMode:
        editorDrawPost()

    ## pygame.draw.rect(display,(0,255,0),player1.damageHitboxRect)

    # flip() the display to put your work on screen
    pygame.display.flip()
    dMult = (clock.tick(fps)/1000)/(1/60)  # limits FPS to WHATEVER

pygame.quit()
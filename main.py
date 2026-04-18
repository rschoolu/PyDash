import pygame, math, pathlib, os, datetime

os.chdir(pathlib.Path(__file__).parent)

# I suck at this
# Example file showing a basic pygame "game loop"

# pygame setup
pygame.init()

# just saying, I could possibly use opengl or SDL2 rendering to speed up the game.
# right now its lots to do w cpu so its not too fast and it lags a lot
# so yeah I am thinking this could definitely change
# but the rendering code would have to be rewritten. at least physics wise its good because thats more annoying lol
display = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

pygame.display.set_caption("PyDash")

class Player(): # Most likely will be a shell, with a function called "tickPlayer" to actually tick the physics.
    # actually nevermind that comment. I want to do many, many things with this?
    def __init__(self):
        #GAMEPLAY
        #use center to position rects
        self.x = -Game.gridSizeInPixels*8
        self.y = 40
        self.yVelocity = 0 # there is no x velocity dum dum
        self.gamemode = "cube"
        self.grounded = False
        self.mini = False
        self.gravity = 1 # 1 = normal gravity, -1 = flipped gravity, 0 = wuttttt
        self.gamemodeGravity = 1
        #self.gamemodeOrbForce = 1
        #self.gamemodePadForce = 1
        #self.gamemodeJumpForce = 1
        self.speed = (Game.gridSizeInPixels*10.3761348898)/60 # adjust later
        self.rotation = 90 # in degrees
        # self.editorTrailPositionTestingThing = [] #delete ts soon bruh lol
        #self.orbBuffer = False # If can orb buffer
        self.clickBuffer = False #if click can buffer deprecates orb bufferrr
        # \|/ change these based on gamemode
        self.maxYVel = 100
        self.minYVel = -100

        # Gamemode dependent variables
        # self.terminalVelocity = 100 # cube terminal velocity

        #LOCKED
        self.cubeSize = Game.gridSizeInPixels

        #### EXPLAINING GRAVITIES!!!!
        # self.gravity <- trigger changable gravity/portal and orb gravity
        # self.gamemodeGravity <- gamemode-depended gravity multiplier
        # self.baseGravity <- CONSTANT!! DO NOT CHANGE UNLESS YOU ARE MODIFYING GAME-WIDE GRAVITY!!!

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
        self.x = -Game.gridSizeInPixels*8
        self.y = 40
        self.yVelocity = 0
        self.gamemode = "cube"
        self.grounded = False
        self.mini = False
        self.gravity = 1
        self.speed = (Game.gridSizeInPixels*10.3761348898)/60
        self.rotation = 90
    def die(self):
        #print("I'm dead!")
        self.resetGameplayVariables()
        currentGame.resetLevel() # cus classes
    def updateHitbox(self): # kinda like scratch gd (NOT PHYSICS)
        # bean
        self.damageHitboxRect.center = (self.x + self.dhrOffsets[0], -self.y + self.dhrOffsets[1])
        self.specialHitboxRect.center = (self.x + self.shrOffsets[0], -self.y + self.shrOffsets[1])
        self.blockHurtHitboxRect.center = (self.x + self.bhhrOffsets[0], -self.y + self.bhhrOffsets[1])
        self.floorHitboxRect.center = (self.x + self.fhrOffsets[0], -self.y + self.fhrOffsets[1])
        self.ceilingHitboxRect.center = (self.x + self.chrOffsets[0], -self.y + self.chrOffsets[1])
        return
    def blitIcon(self):
        tempImage = pygame.transform.scale(self.imageIdiot,[self.cubeSize*currentGame.cameraZoom,self.cubeSize*currentGame.cameraZoom])
        match self.gamemode:
            case "ufo":
                tempImage = pygame.transform.flip(tempImage,False,int((1-self.gravity/abs(self.gravity))/2))
        tempImage = pygame.transform.rotate(tempImage,-(self.rotation-90)%360)
        tempRect = pygame.Rect(0,0,self.cubeSize,self.cubeSize)
        tempRect.center = (self.x-currentGame.cameraX,-self.y+currentGame.cameraY)
        # how do I transform this by the center, not the top left corner?
        # I know! center = (centerx+720)*zoom-720, same but with y)
        tempRect.center = ((tempRect.centerx-640)*currentGame.cameraZoom+640,(tempRect.centery-360)*currentGame.cameraZoom+360)
        tempRect = tempImage.get_rect(center=tempRect.center)
        #self.sprite.update(rect=tempRect,image=tempImage)
        display.blit(tempImage,tempRect)
    def updateGamemodeDependentVariables(self,gamemode):
        # basically just update max velocities and gravity values based on gamemode
        # match case time
        match gamemode:
            case "cube":
                self.maxYVel = 100
                self.minYVel = -100
                self.gamemodeGravity = 1
            case "ball":
                self.maxYVel = 30
                self.minYVel = -30
                self.gamemodeGravity = 0.7
            case "ufo": # ufo values
                self.maxYVel = 50
                self.minYVel = -15
                self.gamemodeGravity = 0.5
        return
    def physicsTick(self): # physicstick
        #for block in blocksInLevel:
            #block.updateHitbox()
        # tick velocity
        currentGamemode = self.gamemode
        self.updateGamemodeDependentVariables(currentGamemode)

        if Game.velocityUpdate == "pre":
            self.y += self.yVelocity*dMult # DO NOT PUT A DELTA MULTIPLIER ON THIS DO NOT PUT IT ON THERE PLEASE
            self.x += self.speed*dMult
            self.updateHitbox() #update hitbox because ye

        #orb bufferism
        # Also make sure this stays up here, not after the block check because it causes the next orb to buffer
        # Also problem with the next block of code because "self.grounded = False"
        if currentGame.mouseClick and not self.grounded:
            #print("orb buffer enabled")
            #self.orbBuffer = True
            self.clickBuffer = True
        if (not currentGame.mouseHeld) or self.grounded:
            #print("orb buffer disabled roses")
            #self.orbBuffer = False
            self.clickBuffer = False

        floorHitbox = self.floorHitboxRect
        ceilingHitbox = self.ceilingHitboxRect
        if (self.gravity/abs(self.gravity)) == -1:
            floorHitbox = self.ceilingHitboxRect
            ceilingHitbox = self.floorHitboxRect

        theFloorSon = currentGame.floorY
        theCeilingSon = currentGame.ceilingY
        if self.gravity/abs(self.gravity) == -1:
            theFloorSon = currentGame.ceilingY
            theCeilingSon = currentGame.floorY

        if floorHitbox.centery*(self.gravity/abs(self.gravity)) >= -theFloorSon*(self.gravity/abs(self.gravity)):
            self.grounded = True
            self.y += ((floorHitbox.centery+theFloorSon)-self.gravity/abs(self.gravity))
        else:
            self.grounded = False

        if currentGamemode == "ball" or currentGamemode == "ufo":
            if ceilingHitbox.centery*(self.gravity/abs(self.gravity))<= -theCeilingSon*(self.gravity/abs(self.gravity)):
                self.y += ceilingHitbox.centery+theCeilingSon-self.gravity/abs(self.gravity)
                self.yVelocity = 0

        # emulate ground and ceiling rects
        groundRect = pygame.Rect(0,0,1280,400)
        groundRect.topleft = (self.x-300,-currentGame.floorY)
        ceilingRect = pygame.Rect(0,0,1280,400)
        ceilingRect.bottomleft = (self.x-300,-currentGame.ceilingY)
        #pygame.draw.rect(display,(0,255,0),groundRect)

        if self.blockHurtHitboxRect.colliderect(groundRect) or self.blockHurtHitboxRect.colliderect(ceilingRect):
            self.die()
            return
        
        collidableBlocks = []
        for block in currentGame.blocksInLevel:
            if abs(block.x-self.x) < 80*3 and abs(block.y-self.y) < 80*3:
                collidableBlocks.append(block)
        
        for block in collidableBlocks:
            if block.blockHitboxRect != False:
                f = abs(floorHitbox.centery-block.blockHitboxRect.top)
                c = abs(ceilingHitbox.centery-block.blockHitboxRect.bottom)
                if (self.gravity/abs(self.gravity)) == -1:
                    f = abs(floorHitbox.centery-block.blockHitboxRect.bottom)
                    c = abs(ceilingHitbox.centery-block.blockHitboxRect.top)
                isInHitrangeFloor = f < 20+abs(self.yVelocity)
                isInHitrangeCeiling = c < 20+abs(self.yVelocity)
                #if not pygame.Rect(floorHitbox.x,floorHitbox.y,floorHitbox.width,floorHitbox.height).colliderect(block.blockHitboxRect) and abs(self.yVelocity) > 10:
                    #isInHitrange = True
                if floorHitbox.colliderect(block.blockHitboxRect) and isInHitrangeFloor and self.yVelocity*(self.gravity/abs(self.gravity)) <= 0:
                    self.grounded = True
                    exit = False
                    #originalY = self.y
                    while not exit:
                        self.y += (self.gravity/abs(self.gravity))
                        self.updateHitbox()
                        if not floorHitbox.colliderect(block.blockHitboxRect):
                            exit = True
                            self.y -= (self.gravity/abs(self.gravity))
                            #if abs(originalY-self.y) > 20:
                                #self.y = originalY
                if currentGamemode == "ball" or currentGamemode == "ufo": # ceiling only hits with ball LIAR
                    if ceilingHitbox.colliderect(block.blockHitboxRect) and isInHitrangeCeiling and self.yVelocity*(self.gravity/abs(self.gravity)) >= 0: # more than zero this time
                        self.yVelocity = 0
                        exit = False
                        while not exit:
                            self.y -= (self.gravity/abs(self.gravity))
                            self.updateHitbox()
                            if not ceilingHitbox.colliderect(block.blockHitboxRect):
                                exit = True
                                self.y += (self.gravity/abs(self.gravity))
                if self.blockHurtHitboxRect.colliderect(block.blockHitboxRect):
                    self.die()
                    return
            if block.damageHitboxRect != False:
                if self.damageHitboxRect.colliderect(block.damageHitboxRect) == True:
                    self.die()
                    return
            if block.specialHitboxRect != False:
                touchingCase = self.specialHitboxRect.colliderect(block.specialHitboxRect)
                orbCase = touchingCase and (currentGame.mouseClick == True or self.clickBuffer == True)
                def disableOrb():
                    #self.orbBuffer = False
                    self.clickBuffer = False
                    currentGame.mouseClick = False
                    self.grounded = False
                    block.specialHitboxRect = False
                    return
                match currentGamemode:
                    case "cube":
                        blueRingForce = 1
                        yellowRingForce = 1
                        pinkRingForce = 1
                        greenRingForce = 1
                        bluePadForce = 1
                        pinkPadForce = 1
                        yellowPadForce = 1
                    case "ball":
                        blueRingForce = 0.8
                        yellowRingForce = 0.8
                        pinkRingForce = 0.8
                        greenRingForce = 0.8
                        bluePadForce = 0.7
                        pinkPadForce = 0.7
                        yellowPadForce = 0.7
                    case "ufo":
                        blueRingForce = 1.2
                        yellowRingForce = 0.75
                        pinkRingForce = 0.6
                        greenRingForce = 1.2
                        bluePadForce = 1.2
                        pinkPadForce = 0.6
                        yellowPadForce = 0.5
                match block.blockType:
                    case "blueRing":
                        if orbCase:
                            disableOrb()
                            self.gravity *= -1
                            self.yVelocity = -10*(self.gravity/abs(self.gravity)) * blueRingForce # IMPORTANT: Not sure if this is good
                    case "yellowRing":
                        if orbCase:
                            disableOrb()
                            self.yVelocity = self.jumpForce*(self.gravity/abs(self.gravity)) * yellowRingForce # IMPORTANT: Not sure if this is good
                    case "pinkRing":
                        if orbCase:
                            disableOrb()
                            #17-20 range
                            self.yVelocity = 19*(self.gravity/abs(self.gravity)) * pinkRingForce # IMPORTANT: Not sure if this is good
                    case "greenRing":
                        if orbCase:
                            disableOrb()
                            self.gravity *= -1
                            self.yVelocity = self.jumpForce(self.gravity/abs(self.gravity)) * greenRingForce
                    case "portalBall":
                        if touchingCase:
                            block.specialHitboxRect = False
                            self.gamemode = "ball"
                            floorY = round((block.y-40)/80)*80 - 4*80
                            if floorY < 0:
                                floorY = 0
                            currentGame.ceilingY = floorY + 8*80
                    case "portalUfo":
                        if touchingCase:
                            block.specialHitboxRect = False
                            self.gamemode = "ufo"
                            floorY = round((block.y-40)/80)*80 - 5*80
                            if floorY < 0:
                                floorY = 0
                            currentGame.ceilingY = floorY + 10*80
                    case "portalCube":
                        if touchingCase:
                            block.specialHitboxRect = False
                            self.gamemode = "cube"
                            floorY = 0
                            currentGame.ceilingY = Game.gridSizeInPixels*500
                    case "portalNormalGrav":
                        if touchingCase:
                            block.specialHitboxRect = False
                            if self.gravity/abs(self.gravity) == -1:
                                self.gravity *= -1
                                self.yVelocity *= 0.5
                    case "portalFlippedGrav":
                        if touchingCase:
                            block.specialHitboxRect = False
                            if self.gravity/abs(self.gravity) == 1:
                                self.gravity *= -1
                                self.yVelocity *= 0.5
                    # https://gdforum.freeforums.net/thread/55538/easy-speed-maths-numbers-speeds
                    case "speed0":
                        if touchingCase:
                            block.specialHitboxRect = False
                            self.speed = (Game.gridSizeInPixels*8.36820083682)/60
                    case "speed1":
                        if touchingCase:
                            block.specialHitboxRect = False
                            self.speed = (Game.gridSizeInPixels*10.3761348898)/60
                    case "speed2":
                        if touchingCase:
                            block.specialHitboxRect = False
                            self.speed = (Game.gridSizeInPixels*12.9032258065)/60
                    case "speed3":
                        if touchingCase:
                            block.specialHitboxRect = False
                            self.speed = (Game.gridSizeInPixels*15.5945419103)/60
                    case "bluePad":
                        if touchingCase: 
                            block.specialHitboxRect = False
                            self.grounded = False # VERY IMPORTANT
                            # why did I write it like this
                            rot = round(((block.rotation-90)%360)/90)
                            if -self.gravity/abs(self.gravity)+1 == rot or round(rot/2)!=rot/2:
                                self.gravity *= -1
                                self.yVelocity = -10*(self.gravity/abs(self.gravity)) * bluePadForce
                    case "pinkPad":
                        if touchingCase: 
                            block.specialHitboxRect = False
                            self.grounded = False # VERY IMPORTANT
                            # less than self.jumpForce but more than pinkOrb okeee
                            self.yVelocity = 25*(self.gravity/abs(self.gravity)) * pinkPadForce # IMPORTANT: Not sure if this is good
                    case "yellowPad":
                        if touchingCase: 
                            block.specialHitboxRect = False
                            self.grounded = False # VERY IMPORTANT
                            # beats me
                            self.yVelocity = 38*(self.gravity/abs(self.gravity)) * yellowPadForce # IMPORTANT: Not sure if this is good
        
        if not self.grounded:
            self.yVelocity -= self.gravity*self.baseGravity*self.gamemodeGravity*dMult
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
                self.rotation += 7*(self.speed/((Game.gridSizeInPixels*10.3761348898)/60))*self.gravity*(self.grounded*2-1)*dMult
            case "ufo":
                self.rotation = 90 + abs(self.yVelocity)/2
            
        # gravity dependent terminal velocity

        if self.yVelocity*(self.gravity/abs(self.gravity)) > self.maxYVel:
            self.yVelocity = self.maxYVel*(self.gravity/abs(self.gravity))
        if self.yVelocity*(self.gravity/abs(self.gravity)) < self.minYVel:
            self.yVelocity = self.minYVel*(self.gravity/abs(self.gravity))

        if currentGame.mouseHeld and self.grounded and currentGamemode == "cube":
            #jump
            self.yVelocity = self.jumpForce*(self.gravity/abs(self.gravity))
            pass
        
        if currentGame.mouseClick and currentGamemode == "ufo":
            # ufo jump
            self.yVelocity = 15.5*(self.gravity/abs(self.gravity))
            pass

        if (currentGame.mouseClick or self.clickBuffer) and self.grounded and currentGamemode == "ball":
            self.gravity *= -1
            self.yVelocity = -8*(self.gravity/abs(self.gravity))
            self.clickBuffer = False

        if Game.velocityUpdate == "post":
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
        self.specialTextureImage = self.getSpecialTextureImage()
        self.scale = scale # multiplier
        self.rotation = rotation
        self.blockSize = Game.gridSizeInPixels*self.scale

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
            "spike_02_001.png": [0,22],
            "bump_01_001.png": [0,36],
            "bump_03_001.png": [0,35],
            "gravbump_01_001.png": [0,32]
        }.get(str.split(textureString,"/")[3],[0,0])
    def rotateOffsets(self,offsets=False): #by default it does texture offsets
        if offsets == False:
            offsets = self.textureOffsets
        rotation = (self.rotation-90)%360
        # I'm gonna be so honest I don't even know trigonometry.
        # I just googled this because it was relatively sort of in my knowledge that to rotate a point in degrees trigonometry was involved
        # So yes I larp trig
        return [offsets[0]*math.cos(math.radians(rotation)) - offsets[1]*math.sin(math.radians(rotation)),offsets[0]*math.sin(math.radians(rotation)) + offsets[1]*math.cos(math.radians(rotation))]
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
        self.bhOffsets = [0,0]
        self.dhOffsets = [0,0]
        self.shOffsets = [0,0]
        match self.blockType:
            case "fullBlock":
                self.blockHitboxRect = pygame.Rect(0,0,self.blockSize,self.blockSize)
                #self.bhOffsets = [0,0]
            case "fullSpike":
                self.damageHitboxRect = pygame.Rect(0,0,self.blockSize*0.2,self.blockSize*0.4)
                #self.dhOffsets = [0,0]
            case "blueRing" | "yellowRing" | "pinkRing" | "greenRing":
                self.specialHitboxRect = pygame.Rect(0,0,self.blockSize*1.2,self.blockSize*1.2)
                #self.shOffsets = [0,0]
            case "smallSpike":
                self.damageHitboxRect = pygame.Rect(0,0,self.blockSize*0.3,self.blockSize*0.2)
                self.dhOffsets = [0,20]
            case "portalBall" | "portalCube" | "portalWave" | "portalUfo" | "portalFlippedGrav" | "portalNormalGrav":
                self.specialHitboxRect = pygame.Rect(0,0,self.blockSize*0.8,self.blockSize*2.7)
                #self.shOffsets = [0,0]
            # TODO: Make these do things
            case "speed0":
                self.specialHitboxRect = pygame.Rect(0,0,self.blockSize*1.2,self.blockSize*1.5)
                #self.shOffsets = [0,0]
            case "speed1":
                self.specialHitboxRect = pygame.Rect(0,0,self.blockSize*1.2,self.blockSize*2)
                #self.shOffsets = [0,0]
            case "speed2":
                self.specialHitboxRect = pygame.Rect(0,0,self.blockSize*1.8,self.blockSize*2)
                #self.shOffsets = [0,0]
            case "speed3":
                self.specialHitboxRect = pygame.Rect(0,0,self.blockSize*2.1,self.blockSize*2)
            case "yellowPad" | "pinkPad":
                self.specialHitboxRect = pygame.Rect(0,0,self.blockSize*0.9,self.blockSize*0.1)
                self.shOffsets = [0,36]
            case "bluePad":
                self.specialHitboxRect = pygame.Rect(0,0,self.blockSize*0.9,self.blockSize*0.2)
                self.shOffsets = [0,34]
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
            self.specialHitboxRect.center = (self.x+rotSHOffsets[0],-self.y+rotSHOffsets[1])
    def getSpecialTextureImage(self):
        if self.textureStr.count("portals") < 1 or self.textureStr.count("speed") > 0:
            return False
        return pygame.image.load(self.textureStr.replace("front","back")).convert_alpha()
    def getOnScreen(self):
        return ((currentGame.cameraX+300-self.x)*currentGame.cameraZoom < 80*5 and ((currentGame.cameraX+300)-self.x)*currentGame.cameraZoom > -80*13 and ((currentGame.cameraY-520)-self.y)*currentGame.cameraZoom < 80*4 and ((currentGame.cameraY-520)-self.y)*currentGame.cameraZoom > -80*7)
    def blitSpecialTexture(self):
        if not self.specialTextureImage:
            return
        # blit special portal texture the underside yuh
        if not self.getOnScreen():
            return
        if not self.imageCache.get("specialTextureImage",False):
            sizeWidth,sizeHeight = (self.specialTextureImage.get_width() * 80/120,self.specialTextureImage.get_height() * 80/120)
            tempImage = pygame.transform.scale(self.specialTextureImage,(sizeWidth*currentGame.cameraZoom,sizeHeight*currentGame.cameraZoom))
            tempImage = pygame.transform.rotate(tempImage,-(self.rotation-90)%360)
            self.imageCache["specialTextureImage"] = tempImage
        tempImage = self.imageCache["specialTextureImage"]
        tempRect = pygame.Rect(0,0,self.blockSize,self.blockSize)
        
        rotTexOffsets = self.rotateOffsets(self.textureOffsets)
        tempRect.center = (self.x-currentGame.cameraX + rotTexOffsets[0],-self.y+currentGame.cameraY + rotTexOffsets[1])
        tempRect.center = ((tempRect.centerx-640)*currentGame.cameraZoom+640,(tempRect.centery-360)*currentGame.cameraZoom+360)
        tempRect = tempImage.get_rect(center=tempRect.center)

        display.blit(tempImage,tempRect)
    def blitTexture(self):
        if not self.getOnScreen():
            return
        # Make this work with textures not block sized
        # basically just 120 is the base size in the textures, 80 is the base size here. Do the math
        if not self.imageCache.get("tempImage",False):
            sizeWidth,sizeHeight = (self.textureImage.get_width() * 80/120,self.textureImage.get_height() * 80/120) # convert uhd
            #tempImage = pygame.transform.scale(self.textureImage,[self.blockSize,self.textureImage.get_height()*(self.blockSize/self.textureImage.get_width())])
            tempImage = pygame.transform.scale(self.textureImage,(sizeWidth*currentGame.cameraZoom,sizeHeight*currentGame.cameraZoom))
            tempImage = pygame.transform.rotate(tempImage,-(self.rotation-90)%360)
            self.imageCache["tempImage"] = tempImage
        tempImage = self.imageCache["tempImage"]
        tempRect = pygame.Rect(0,0,self.blockSize,self.blockSize)
        #print(self.blockType + ": " + str(self.textureOffsets[0]) + ", " + str(self.textureOffsets[1]))
        rotTexOffsets = self.rotateOffsets(self.textureOffsets)
        tempRect.center = (self.x-currentGame.cameraX + rotTexOffsets[0],-self.y+currentGame.cameraY + rotTexOffsets[1])
        tempRect.center = ((tempRect.centerx-640)*currentGame.cameraZoom+640,(tempRect.centery-360)*currentGame.cameraZoom+360)
        tempRect = tempImage.get_rect(center=tempRect.center)
        #self.sprite.update(rect=tempRect,image=tempImage)
        #print(self.x-player1.x)
        #print("op:")
        #print(player1.x-self.x)
        display.blit(tempImage,tempRect)

# blocksInLevel = sortBlocks()

def lerp(x,y,alpha):
    return x + (y - x)*alpha

fps = 240 # game fps
dMult = 1/fps

blockTypeTexture = {
    "fullBlock": "./resources/blocks/square_01_001.png",
    "fullSpike": "./resources/blocks/spike_01_001.png",
    "smallSpike": "./resources/blocks/spike_02_001.png",
    "blueRing": "./resources/blocks/gravring_01_001.png",
    "yellowRing": "./resources/blocks/ring_01_001.png",
    "pinkRing": "./resources/blocks/ring_03_001.png",
    "greenRing": "./resources/blocks/gravJumpRing_01_001.png",
    "portalFlippedGrav": "./resources/blocks/portals/portal_02_front_001.png",
    "portalNormalGrav": "./resources/blocks/portals/portal_01_front_001.png",
    "portalBall": "./resources/blocks/portals/portal_07_front_001.png",  #"./resources/blocks/spike_02_001.png", #placeholder
    "portalCube": "./resources/blocks/portals/portal_03_front_001.png",
    "portalWave": "./resources/blocks/portals/portal_13_front_001.png", # automatically, in the blitting, should be a special process to auto-blit the under texture
    "portalUfo": "./resources/blocks/portals/portal_10_front_001.png",  # portalUFO ????
    "speed0": "./resources/blocks/portals/boost_01_001.png",
    "speed1": "./resources/blocks/portals/boost_02_001.png",
    "speed2": "./resources/blocks/portals/boost_03_001.png",
    "speed3": "./resources/blocks/portals/boost_04_001.png",
    "bluePad": "./resources/blocks/gravbump_01_001.png",
    "yellowPad": "./resources/blocks/bump_01_001.png",
    "pinkPad": "./resources/blocks/bump_03_001.png"
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
        screenCursorX = (screenCursorX-640)/currentGame.cameraZoom+640
        screenCursorY = (screenCursorY-360)/currentGame.cameraZoom+360
        #zoomX = (currentGame.cameraX-640)/currentGame.cameraZoom+640
        #zoomY = (currentGame.cameraY-360)/currentGame.cameraZoom+360
        zoomX,zoomY = currentGame.cameraX,currentGame.cameraY
        self.x, self.y = (screenCursorX+zoomX,-screenCursorY+zoomY)
        #self.x, self.y = (self.x-640)/currentGame.cameraZoom+640,(self.y-360)/currentGame.cameraZoom+360
    def cycleBlockType(self,back=False):
        self.blockType = list(blockTypeTexture.keys())[(list(blockTypeTexture.keys()).index(self.blockType)+(((not back)*2)-1))%(list(blockTypeTexture.keys()).__len__())]
        self.texture = blockTypeTexture.get(self.blockType)
        self.updateTexture()
    def paint(self):
        #collisionRect = pygame.Rect(self.x-currentGame.cameraX,-self.y+currentGame.cameraY,1,1)
        doX,doY = self.x-currentGame.cameraX,-self.y+currentGame.cameraY
        doX = (doX-640)*currentGame.cameraZoom+640
        doY = (doY-360)*currentGame.cameraZoom+360
        collisionRect = pygame.Rect(doX,doY,1,1)
        for buttonStr in currentGame.editorButtons:
            buttonRect = currentGame.editorButtons[buttonStr]
            if collisionRect.colliderect(buttonRect):
                key = list(currentGame.editorButtons.keys())[list(currentGame.editorButtons.values()).index(buttonRect)]
                #print(key)
                match key:
                    case "buildButtonRect":
                        self.mode = "draw"
                    case "editButtonRect":
                        self.mode = "edit"
                    case "deselect":
                        self.selectedBlockIndex = -1
                    case "save":
                        currentGame.resetLevel()
                        DataSave.save(currentGame.blocksInLevel)
                    case "load":
                        windowsPathList = list(pathlib.Path("./data/").iterdir())
                        for windowsPath in windowsPathList:
                            print(str(windowsPathList.index(windowsPath)+1) + ": " + windowsPath.name)
                        letmego = False
                        while not letmego:
                            try:
                                inputted = input('Select level (Type a number) Type "cancel" to cancel: ')
                                if inputted == "cancel":
                                    letmego = True
                                    break
                                index = int(inputted)-1
                                if index < 0:
                                    int("not a number lmao") # throwing an error on purpose lmao
                                letmego = True
                                currentGame.blocksInLevel = DataSave.load(windowsPathList[index].name.removesuffix(".txt"))
                            except ValueError:
                                print("Invalid Input")
                        #currentGame.blocksInLevel = DataSave.load(windowsPathList[index].name.removesuffix(".txt"))
                    case "song": # clone lmao
                        windowsPathList = list(pathlib.Path("./resources/music/").iterdir())
                        for windowsPath in windowsPathList:
                            print(str(windowsPathList.index(windowsPath)+1) + ": " + windowsPath.name)
                        letmego = False
                        while not letmego:
                            try:
                                inputted = input('Select song (Type a number) Type "cancel" to cancel: ')
                                if inputted == "cancel":
                                    letmego = True
                                    break
                                index = int(inputted)-1
                                if index < 0:
                                    int("not a number lmao") # throwing an error on purpose lmao
                                letmego = True
                                currentGame.songName = windowsPathList[index].name.removesuffix(".ogg")
                                currentGame.reloadSong()
                            except ValueError:
                                print("Invalid Input")
                return
        match self.mode:
            case "draw":
                self.placeBlock()
            case "edit":
                self.selectBlock()
    def selectBlock(self):
        collisionRect = pygame.Rect(self.x-currentGame.cameraX,-self.y+currentGame.cameraY,1,1)
        for block in currentGame.blocksInLevel:
            if currentGame.blocksInLevel.index(block) == currentGame.blocksInLevel[self.selectedBlockIndex]:
                continue
            newRect = pygame.Rect(0,0,80,80)
            newRect.center = (block.x-currentGame.cameraX,-block.y+currentGame.cameraY)
            if collisionRect.colliderect(newRect):
                self.selectedBlockIndex = currentGame.blocksInLevel.index(block)
                break
    def blitSelectedBlock(self):
        if self.selectedBlockIndex == -1:
            return
        if self.selectedBlockIndex > currentGame.blocksInLevel.__len__()-1:
            self.selectedBlockIndex = -1
            return
        selectedBlock = currentGame.blocksInLevel[self.selectedBlockIndex]
        textureWidth,textureHeight = (selectedBlock.textureImage.get_width()*80/120).__int__(),(selectedBlock.textureImage.get_height()*80/120).__int__()
        textureWidth,textureHeight = Block.rotateSize(selectedBlock,textureWidth,textureHeight)[0],Block.rotateSize(selectedBlock,textureWidth,textureHeight)[1]
        textureWidth *= currentGame.cameraZoom
        textureHeight *= currentGame.cameraZoom
        surface = pygame.Surface((textureWidth,textureHeight))
        surface.fill((255,255,255))
        surface.set_alpha(128)
        offsetsX,offsetsY = selectedBlock.rotateOffsets(selectedBlock.getTextureOffsets())
        screenX = selectedBlock.x-currentGame.cameraX+offsetsX
        screenY = -selectedBlock.y+currentGame.cameraY+offsetsY
        screenX = (screenX-640)*currentGame.cameraZoom+640
        screenY = (screenY-360)*currentGame.cameraZoom+360
        display.blit(surface,(screenX-textureWidth/2,screenY-textureHeight/2))
    def placeBlock(self):
        newBlock = Block(round(self.x/80)*80,round((self.y-40)/80)*80+40,self.blockType,self.texture,self.rotation,self.scale)
        currentGame.blocksInLevel.append(newBlock)
        self.selectedBlockIndex = currentGame.blocksInLevel.index(newBlock)
    def editSelectedObject(self,xPos=0,yPos=0,rotation=0,scale=0):
        if self.selectedBlockIndex == -1:
            return
        block = currentGame.blocksInLevel[self.selectedBlockIndex]
        block.x += xPos
        block.y += yPos
        block.rotation += rotation
        block.rotation %= 360
        block.scale += scale
        block.resetHitbox()
        return
    def cloneSelectedObject(self):
        if self.selectedBlockIndex == -1:
            return
        block = currentGame.blocksInLevel[self.selectedBlockIndex]
        clonedBlock = Block(block.x,block.y,block.blockType,block.textureStr,block.rotation,block.scale)
        clonedBlock.resetHitbox()
        currentGame.blocksInLevel.append(clonedBlock)
        self.selectedBlockIndex = currentGame.blocksInLevel.index(clonedBlock)
        return
    def blitBrush(self):
        if self.mode == "edit":
            return
        sizeWidth,sizeHeight = (self.textureImage.get_width() * 80/120,self.textureImage.get_height() * 80/120) # convert uhd
        #tempImage = pygame.transform.scale(self.textureImage,[self.blockSize,self.textureImage.get_height()*(self.blockSize/self.textureImage.get_width())])
        tempImage = pygame.transform.scale(self.textureImage,(sizeWidth*currentGame.cameraZoom,sizeHeight*currentGame.cameraZoom))
        tempImage = pygame.transform.rotate(tempImage,-(self.rotation-90)%360)
        tempRect = pygame.Rect(0,0,self.scale*80,self.scale*80)
        rotTexOffsets = Block.rotateOffsets(self,Block.getTextureOffsets(self,self.texture))
        tempRect.topleft = (self.x-currentGame.cameraX + rotTexOffsets[0],-self.y+currentGame.cameraY + rotTexOffsets[1])
        tempRect.topleft = ((tempRect.left-640)*currentGame.cameraZoom+640,(tempRect.top-360)*currentGame.cameraZoom+360)
        tempRect = tempImage.get_rect(center=tempRect.center)
        display.blit(tempImage,tempRect)
    def erase(self): #no point
        collisionRect = pygame.Rect(self.x-currentGame.cameraX,-self.y+currentGame.cameraY,1,1)
        for block in currentGame.blocksInLevel:
            newRect = pygame.Rect(0,0,80,80)
            newRect.center = (block.x-currentGame.cameraX,-block.y+currentGame.cameraY)
            if collisionRect.colliderect(newRect):
                currentSelectedBlock = "not a block lmao"
                if self.selectedBlockIndex > -1:
                    currentSelectedBlock = currentGame.blocksInLevel[self.selectedBlockIndex]
                currentGame.blocksInLevel.remove(block)
                if block != currentSelectedBlock and self.selectedBlockIndex > -1:
                    self.selectedBlockIndex = currentGame.blocksInLevel.index(currentSelectedBlock)
                else:
                    self.selectedBlockIndex = -1
                break

class DataSave(): # just to organize things cus they have to be here anyway
    #self.x = x
    #self.y = y
    #self.blockType = blocktype
    #self.rotation = rotation
    #self.scale = scale
    seperators = ["#","|","\\"] # first one is the highest level, for seperating blocks. second is for seperating data in blocks, third would be for seperating data in block's custom data
    def __init__(self):
        pass
    def save(blocksInLevel):
        saveString = "" #literally save ts blud
        # first save song
        saveString += "level" + DataSave.seperators[1]
        saveString += currentGame.songName + DataSave.seperators[1] + DataSave.seperators[0]
        for block in blocksInLevel:
            blockString = ""
            # Bro screw python 3.14
            blockString += str(block.x) + DataSave.seperators[1]
            blockString += str(block.y) + DataSave.seperators[1]
            blockString += str(block.blockType) + DataSave.seperators[1]
            blockString += str(block.rotation) + DataSave.seperators[1]
            blockString += str(block.scale) + DataSave.seperators[1]
            saveString += str(blockString) + DataSave.seperators[0]
        filename = str(datetime.datetime.now()).replace(" ","_").replace(":","-").replace(".","_")
        with open("./data/" + filename + ".txt","w") as file:
            file.write(saveString)
            file.close()
        return
    def load(levelName):
        # safety
        if levelName.count(".txt") == 0:
            levelName += ".txt"
        loadString = ""
        with open("./data/" + levelName,"r") as file: #even more safety
            loadString = file.read()
            file.close()
        blocks = loadString.split("#")
        blocks.remove("")
        levelArray = []
        for blockString in blocks:
            blockArray = blockString.split("|")
            if blockArray[0] == "level":
                currentGame.songName = blockArray[0]
                currentGame.reloadSong()
                continue
            #print(blockArray)
            levelArray.append(Block(float(blockArray[0]),float(blockArray[1]),blockArray[2],blockTypeTexture[blockArray[2]],float(blockArray[3]),float(blockArray[4])))
        return levelArray
# get ready bro
# Re-ordered the functions to be aligned with old versions's functions.
class Game(): 
    # static variables
    gridSizeInPixels = 80
    velocityUpdate = "pre"
    def __init__(self): # changable variables
        self.cameraX = 0
        self.cameraY = 0
        self.cameraZoom = 0.85
        self.blocksInLevel = []
        #self.players = [] # player1 = Player()
        self.player1 = Player()
        self.floorY = 0
        self.ceilingY = Game.gridSizeInPixels*500
        self.mouseClick = False
        self.mouseHeld = False

        self.currentBrush = EditorBrush()
        self.showHitboxes = True
        self.editorMode = True
        self.editorButtons = {
            "buildButtonRect": pygame.Rect(0,0,200,50),
            "editButtonRect": pygame.Rect(0,0,200,50),
            "deselect": pygame.Rect(0,0,200,50),
            "save": pygame.Rect(0,0,200,50),
            "load": pygame.Rect(0,0,200,50),
            "song": pygame.Rect(0,0,200,50)
        }
        self.editorButtons["buildButtonRect"].topright = (1280-40,40)
        self.editorButtons["editButtonRect"].topright = (1280-40,40 + self.editorButtons["buildButtonRect"].height*1.1)
        self.editorButtons["deselect"].topright = (1280-40,40 + self.editorButtons["buildButtonRect"].height*1.1*2)
        self.editorButtons["save"].topright = (1280-40,40 + self.editorButtons["buildButtonRect"].height*1.1*3)
        self.editorButtons["load"].topright = (1280-40,40 + self.editorButtons["buildButtonRect"].height*1.1*4)
        self.editorButtons["song"].topright = (1280-40,40 + self.editorButtons["buildButtonRect"].height*1.1*5)

        self.songName = "hero-pump-it-hardtekk" # forcing .ogg
        # it's because mp3s have issues with rewinding and checking their position (read this: https://www.pygame.org/docs/ref/music.html#pygame.mixer.music.set_pos)
        # and I don't want to deal with that. So songs are forced ogg. (Oga -> ogg works as long as it's vorbis)
        self.mixer = pygame.mixer
        self.mixer.init()
        self.song = self.mixer.music
        self.reloadSong()
        return
    def reloadSong(self): # so i can do that
        self.song.unload()
        self.song.load("./resources/music/" + self.songName + ".ogg") #only use ogg files
        self.song.rewind()
    def resetLevel(self):
        self.floorY = 0
        self.ceilingY = Game.gridSizeInPixels*500
        self.song.stop()
        self.song.rewind()
        for block in self.blocksInLevel:
            block.resetHitbox()
        return
    def sortBlocks(self):
        blocksClone = self.blocksInLevel.copy()
        sortedList = []
        
        done = False
        while not done:
            if blocksClone.__len__() == 0:
                done = True
            lowest = False
            for block in blocksClone:
                if not lowest:
                    lowest = block
                    continue
                if block.x < lowest.x:
                    lowest = block
            if lowest:
                sortedList.append(lowest)
                blocksClone.remove(lowest)
        return sortedList
    def perFrameUpdate(self):
        self.player1.physicsTick()
    def updateCamera(self):
        self.cameraX = self.player1.x - 350 # 300
        if not self.editorMode:
            if abs(self.ceilingY - self.floorY) < 1280:
                self.cameraY = lerp(self.cameraY,(self.floorY+self.ceilingY)/2+720/2,0.3*dMult)
                return
            yPosOnScreen = abs(-self.player1.y+self.cameraY)
            if (yPosOnScreen<200):
                target = self.cameraY + ((200-yPosOnScreen))*dMult
                self.cameraY = lerp(self.cameraY,target,0.3*dMult)
            if (-self.player1.y+self.cameraY>720-200):
                target = self.cameraY - ((-self.player1.y+self.cameraY-520))*dMult
                self.cameraY = lerp(self.cameraY,target,0.3*dMult)
            return
        self.cameraY = lerp(self.cameraY,self.player1.y + 720 - 200,0.3*dMult)
        return
    def drawHitboxes(self):
        def drawTransparentRect(rect,color):
            newRect = pygame.Rect(0,0,rect.width*self.cameraZoom,rect.height*self.cameraZoom)
            newRect.center = (rect.center[0]-self.cameraX,rect.center[1]+self.cameraY)
            newRect.center = (newRect.centerx-640)*self.cameraZoom+640,(newRect.centery-360)*self.cameraZoom+360
            surface = pygame.Surface(newRect.size)
            surface.set_alpha(128)
            surface.fill(color)
            display.blit(surface, newRect.topleft)
        for block in self.blocksInLevel:
            if block.blockHitboxRect:
                drawTransparentRect(block.blockHitboxRect,(255,255,0))
            if block.damageHitboxRect:
                drawTransparentRect(block.damageHitboxRect,(255,0,0))
            if block.specialHitboxRect:
                drawTransparentRect(block.specialHitboxRect,(0,255,0))
        drawTransparentRect(self.player1.damageHitboxRect,(255,0,0))
        drawTransparentRect(self.player1.ceilingHitboxRect,(0,255,0))
        drawTransparentRect(self.player1.floorHitboxRect,(0,255,0))
        drawTransparentRect(self.player1.blockHurtHitboxRect,(0,0,255))
        return
    def drawDisplay(self):
        # previous order: blit blocks, blit ground, blit icon, blit ui
        # new order: blit undersideblocks like portals, blit icon, blit blocks, blit ground, blit ui
        
        # Blit deco blocks and underside of blocks
        blocksToBlit = self.blocksInLevel.copy() # Very important to copy

        for block in blocksToBlit:
            block.blitSpecialTexture()
            # TODO: Make up a way to tell if a block is deco. having it in blocktype is weird
            if block.blockType.count("deco") < 1 and not (block.textureStr.lower().count("ring") > 0 or block.textureStr.count("boost") > 0):
                continue # Press start reference
            block.blitTexture()
            blocksToBlit[blocksToBlit.index(block)] = "noBlit"

        # blit icon
        self.player1.blitIcon()

        # finally blit those unblitted blocks
        for block in blocksToBlit:
            if block == "noBlit":
                continue
            block.blitTexture()
            blocksToBlit[blocksToBlit.index(block)] = "noBlit"
        
        if self.showHitboxes:
            self.drawHitboxes()

        #draw ground
        groundRect = pygame.Rect(0,0,1280,400)
        groundRect.topleft = (0,-self.floorY+self.cameraY)
        # (groundRect.left-640)*self.cameraZoom+640
        groundRect.topleft = (groundRect.left,(groundRect.top-360)*self.cameraZoom+360)
        pygame.draw.rect(display,(255,0,0),groundRect)

        # and ceiling
        ceilingRect = pygame.Rect(0,0,1280,400)
        ceilingRect.bottomleft = (0,-self.ceilingY+self.cameraY)
        ceilingRect.bottomleft = (ceilingRect.left,(ceilingRect.bottom-360)*self.cameraZoom+360)
        pygame.draw.rect(display,(255,0,0),ceilingRect)

        # render font n such
        def renderBoldFont(string,x,y,size=28):
            font = pygame.font.Font("./resources/fonts/MSGOTHIC.TTC",size)
            logoStr = string
            surface = font.render(logoStr,True,(255,255,255))
            surface2 = font.render(logoStr,True,(0,0,0))
            """offsetX = -abs(surface.get_width()-surface2.get_width())
            offsetX = -2
            offsetY = -abs(surface.get_height()-surface2.get_height())
            offsetY = 0"""
            offsets = [(-1,-1),(1,1),(-1,1),(1,-1)]
            for offset in offsets:
                display.blit(surface,(x+offset[0],y+offset[1]))
            display.blit(surface2,(x,y))
        
        renderBoldFont("PyDash made by rschoolu",0,0)
        renderBoldFont("FPS: " + str(round(60/dMult)) + "/" + str(fps),0,30)
        #renderBoldFont("Debug",0,30*2)
        #renderBoldFont("playerX: " + str(player1.x) + " playerY: " + str(player1.y),0,30*3)
        
        #pygame.draw.rect(display,(0,255,0),player1.specialHitboxRect)
        #pygame.draw.rect(display,(255,255,0),player1.floorHitboxRect)
        return
    """
    """
    def editorSyncSong(self):
        currentX = -Game.gridSizeInPixels*8
        currentSongTime = 0
        speedGoingAt = (Game.gridSizeInPixels*10.3761348898)/60
        exit = False
        portalsInLevel = []
        for block in self.blocksInLevel:
            if block.blockType.count("speed") > 0:
                portalsInLevel.append(block)
        while not exit:
            currentX+=speedGoingAt/(fps/60) # fps level precision boiii
            collisionRect = pygame.Rect(0,0,1,Game.gridSizeInPixels*500)
            collisionRect.bottomleft = (currentX,0)
            for block in portalsInLevel:
                if block.specialHitboxRect.colliderect(collisionRect):
                    portalsInLevel.remove(block)
                    match block.blockType:
                        case "speed0":
                            speedGoingAt = (Game.gridSizeInPixels*8.36820083682)/60
                        case "speed1":
                            speedGoingAt = (Game.gridSizeInPixels*10.3761348898)/60
                        case "speed2":
                            speedGoingAt = (Game.gridSizeInPixels*12.9032258065)/60
                        case "speed3":
                            speedGoingAt = (Game.gridSizeInPixels*15.5945419103)/60
            currentSongTime+=(1/fps)
            if currentX >= self.player1.x:
                exit = True
        self.song.set_pos(currentSongTime)
    def tickSong(self): #proper syncing w/ speed
        if self.player1.x < -Game.gridSizeInPixels*8:
            return
        #print((player1.x+gridSizeInPixels*8)/(player1.speed*60))
        if self.song.get_pos() <= 0 and not self.song.get_busy():
            self.song.play()
            #self.song.set_pos((self.player1.x+Game.gridSizeInPixels*8)/(self.player1.speed*60))
        if abs(self.song.get_pos()-self.player1.x/(self.player1.speed*60)) > 0.5:
            #song.set_pos(int((player1.x+gridSizeInPixels*8)/(player1.speed*60)))
            pass
        return
    def drawGrid(self):
        for i in range(round(17/self.cameraZoom)): # TODO: Fix this bumfuck thing
            vRect = pygame.Rect(0,0,3,720)
            vRect.centerx = 80*i+round((self.cameraX+300)/80)*80-40-80*round((300/80)/self.cameraZoom)-self.cameraX
            vRect.centerx = (vRect.centerx-640)*self.cameraZoom+640
            #vRect.centerx = -40+80*i+round((player1.x)/80)*80-80*3-cameraX
            pygame.draw.rect(display,(255,255,0),vRect)
        for i in range(round(12/self.cameraZoom)):
            hRect = pygame.Rect(0,0,1280,3)
            hRect.centery = 80*i+round(-(self.cameraY-520)/80)*80-80*round(7/self.cameraZoom)+self.cameraY
            hRect.centery = (hRect.centery-360)*self.cameraZoom+360
            pygame.draw.rect(display,(255,255,0),hRect)
    def editorDrawPre(self):
        #self.drawGrid()
        spawnRect = pygame.Rect(0,0,40*self.cameraZoom,40*self.cameraZoom)
        spawnRect.center = (-Game.gridSizeInPixels*8-self.cameraX,-40+self.cameraY)
        spawnRect.center = (spawnRect.centerx-640)*self.cameraZoom+640,(spawnRect.centery-360)*self.cameraZoom+360
        pygame.draw.rect(display,(0,255,0),spawnRect)
        return
    def editorDrawPost(self):
        self.currentBrush.blitBrush()
        self.currentBrush.blitSelectedBlock()

        #Draw buttons:
        font = pygame.font.Font("./resources/fonts/MSGOTHIC.TTC",30)
        #buildText = font.render("Draw Mode",True,(0,0,0))

        #editText = font.render("Edit Mode",True,(0,0,0))

        drawColor = False
        editColor = False
        if self.currentBrush.mode == "draw":
            drawColor = (0,255,0)
            editColor = (255,255,255)
        else:
            drawColor = (255,255,255)
            editColor = (0,255,0)

        text = font.render("Nadeko Draw",True,(0,0,0))

        pygame.draw.rect(display,drawColor,self.editorButtons["buildButtonRect"])
        display.blit(text,(self.editorButtons["buildButtonRect"].centerx-text.get_width()/2,self.editorButtons["buildButtonRect"].centery-text.get_height()/2))

        text = font.render("Edit Mode",True,(0,0,0))
        pygame.draw.rect(display,editColor,self.editorButtons["editButtonRect"])
        display.blit(text,(self.editorButtons["editButtonRect"].centerx-text.get_width()/2,self.editorButtons["editButtonRect"].centery-text.get_height()/2))

        text = font.render("Deselect",True,(0,0,0))
        pygame.draw.rect(display,(255,255,255),self.editorButtons["deselect"])
        display.blit(text,(self.editorButtons["deselect"].centerx-text.get_width()/2,self.editorButtons["deselect"].centery-text.get_height()/2))

        text = font.render("Save Level",True,(0,0,0))
        pygame.draw.rect(display,(255,255,255),self.editorButtons["save"])
        display.blit(text,(self.editorButtons["save"].centerx-text.get_width()/2,self.editorButtons["save"].centery-text.get_height()/2))

        text = font.render("Load Level",True,(0,0,0))
        pygame.draw.rect(display,(255,255,255),self.editorButtons["load"])
        display.blit(text,(self.editorButtons["load"].centerx-text.get_width()/2,self.editorButtons["load"].centery-text.get_height()/2))

        text = font.render("Change Song",True,(0,0,0))
        pygame.draw.rect(display,(255,255,255),self.editorButtons["song"])
        display.blit(text,(self.editorButtons["song"].centerx-text.get_width()/2,self.editorButtons["song"].centery-text.get_height()/2))

        #renderBoldFont("make sum good for me boaaa",720/2,0,40)
        return
    def editorLoop(self):
        # new thing
        if keys[pygame.K_1] and not prevKeys[pygame.K_1]:
            self.currentBrush.mode = "draw"
        if keys[pygame.K_2] and not prevKeys[pygame.K_2]:
            self.currentBrush.mode = "edit"

        speed = 10
        if (keys[pygame.K_LSHIFT]):
            speed = 1
        if self.currentBrush.mode == "edit":
            speed = 0
        self.player1.y += (speed*dMult)*(keys[pygame.K_w])
        self.player1.y -= (speed*dMult)*(keys[pygame.K_s])
        self.player1.x += (speed*dMult)*(keys[pygame.K_d])
        self.player1.x -= (speed*dMult)*(keys[pygame.K_a])
        
        self.currentBrush.updatePosition()

        if keys[pygame.K_e] and not prevKeys[pygame.K_e]:
            match self.currentBrush.mode:
                case "draw":
                    self.currentBrush.rotation += 90/(keys[pygame.K_LSHIFT]+1)
                    self.currentBrush.rotation %= 360
                case "edit":
                    self.currentBrush.editSelectedObject(rotation=90/(keys[pygame.K_LSHIFT]+1))
        if keys[pygame.K_q] and not prevKeys[pygame.K_q]:
            match self.currentBrush.mode:
                case "draw":
                    self.currentBrush.rotation -= 90/(keys[pygame.K_LSHIFT]+1)
                    self.currentBrush.rotation %= 360
                case "edit":
                    self.currentBrush.editSelectedObject(rotation=-90/(keys[pygame.K_LSHIFT]+1))

        if self.currentBrush.mode == "edit":
            moveMultiplier = 1/((keys[pygame.K_LSHIFT]*9)+1)
            if not keys[pygame.K_LCTRL]:
                if keys[pygame.K_w] and not prevKeys[pygame.K_w]:
                    self.currentBrush.editSelectedObject(yPos=Game.gridSizeInPixels*moveMultiplier)
                if keys[pygame.K_a] and not prevKeys[pygame.K_a]:
                    self.currentBrush.editSelectedObject(xPos=-Game.gridSizeInPixels*moveMultiplier)
                if keys[pygame.K_s] and not prevKeys[pygame.K_s]:
                    self.currentBrush.editSelectedObject(yPos=-Game.gridSizeInPixels*moveMultiplier)
                if keys[pygame.K_d] and not prevKeys[pygame.K_d]:
                    self.currentBrush.editSelectedObject(xPos=Game.gridSizeInPixels*moveMultiplier)
            if keys[pygame.K_LCTRL] and keys[pygame.K_d] and not prevKeys[pygame.K_d]:
                self.currentBrush.cloneSelectedObject()
        
        if mouse[2] and not prevMouse[2]:
            self.currentBrush.erase()

        if keys[pygame.K_f] and not prevKeys[pygame.K_f]:
            self.currentBrush.cycleBlockType()
        if keys[pygame.K_r] and not prevKeys[pygame.K_r]:
            self.currentBrush.cycleBlockType(True)

        if mouse[0] and not prevMouse[0]:
            self.currentBrush.paint()
        return
    def tickGame(self):
        if keys[pygame.K_g] and not prevKeys[pygame.K_g]:
            self.editorMode = not self.editorMode
            if not self.editorMode:
                for block in self.blocksInLevel:
                    block.resetHitbox()
                self.player1.yVelocity = 0
                if self.player1.x >= -Game.gridSizeInPixels*8:
                    self.song.play()
                    self.editorSyncSong()
            else:
                self.song.stop()
                self.song.rewind()
        if keys[pygame.K_h] and not prevKeys[pygame.K_h]:
            self.showHitboxes = not self.showHitboxes
        # poll input before frame update
        inputValue = pygame.mouse.get_pressed()[0]
        if self.mouseHeld != inputValue and inputValue == True:
            self.mouseClick = True
        elif self.mouseHeld == inputValue and inputValue == True:
            self.mouseHeld = True
            self.mouseClick = False
        self.mouseHeld = inputValue
        if not self.editorMode:
            self.perFrameUpdate()
            self.tickSong()
        else:
            self.editorLoop()

        self.updateCamera()

        if self.editorMode:
            self.editorDrawPre()
            self.drawGrid() # optional draw grid feature?!???!?!?!?!?!??
        self.drawDisplay()
        if self.editorMode:
            self.editorDrawPost()

mouse = pygame.mouse.get_pressed()
keys = pygame.key.get_pressed()

currentGame = Game()

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

    display.fill("blue")

    currentGame.tickGame()

    ## pygame.draw.rect(display,(0,255,0),player1.damageHitboxRect)

    # flip() the display to put your work on screen
    pygame.display.flip()
    dMult = (clock.tick(fps)/1000)/(1/60)  # limits FPS to WHATEVER

pygame.quit()
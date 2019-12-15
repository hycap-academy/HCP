import pygame, sys
import time
import math
import importlib
from random import randint

from pygame.locals import *

DISPLAY_WIDTH=800
DISPLAY_HEIGHT=800
TILESIZE = 50
LINEWIDTH = 5
masterTurn=0

maxTurns=100
state = ""
textList = []
textBlob = ""
aryTiles = []
objects=[]
instructions = ""
loseMsg=""
currentLevelFile=""
currentSolnFile=""


BLACK=(0,0,0)
DARK_GRAY = (50,50,50)
WHITE=(255,255,255)
GREEN=(0,200,0)
BRIGHT_GREEN=(150,255,150)
RED=(200,0,0)
BRIGHT_RED=(255,150,150)
BLUE=(0,0,255)

pygame.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
textfont = pygame.font.SysFont("Arial", 20)
instructionFont = pygame.font.SysFont("Arial", 24)
font = pygame.font.Font("freesansbold.ttf",14)
smallfont = pygame.font.Font("freesansbold.ttf",10)
clock = pygame.time.Clock()
intro=True



class object():
    def __init__(self, coordx, coordy, direction, sImg):
        self.initx = coordx
        self.inity = coordy
        self.initdir = direction
        self.x = coordx
        self.y = coordy
        self.direction=direction
        self.OrigSurfImg=sImg
        # direction: 0=north, 1=west, 2=south, 3=east
        self.turn=0  
        self.surfImg = pygame.transform.rotate(self.OrigSurfImg, self.direction*90)
        self.trail=[]
        self.healthHistory = {}
        
        

    def reset(self):
        self.x = self.initx
        self.y = self.inity
        self.direction = self.initdir
        self.turn=0
        self.trail=[]
        self.health=100

    def addTrail(self):
        self.trail.append((self.x, self.y))

    def getRect(self):
        return pygame.Rect(self.x*(TILESIZE+2*LINEWIDTH)+LINEWIDTH, self.y*(TILESIZE+2*LINEWIDTH)+LINEWIDTH, TILESIZE, TILESIZE)

    def turnLeft(self):
        if self.turn < masterTurn:
            if self.direction <3:
                self.direction +=1
            else:
                self.direction=0
            
            self.surfImg = pygame.transform.rotate(self.OrigSurfImg, self.direction*90)
            
            if self.turn==masterTurn-1:
                textScroll(self.turn, "Turning Left")

            self.turn+=1

    def turnRight(self):
        if self.turn < masterTurn:
            if self.direction >0:
                self.direction -=1
            else:
                self.direction=3
                
            self.surfImg = pygame.transform.rotate(self.OrigSurfImg, self.direction*90)
            
            if self.turn==masterTurn-1:
                textScroll(self.turn, "Turning Right")

            self.turn+=1


                            


    def moveForward(self):
        status =""
        if self.turn < masterTurn:
            x, y = self.getFrontSquare(self.x, self.y, self.direction)
            if self.checkForObstacles(x,y)==0:
                self.addTrail()
                if self.direction==0: # north
                    self.y-=1
                    status = "Moved North"
                elif self.direction==1: # west
                    self.x -=1
                    status = "Moved West"
                elif self.direction==2: #south
                    self.y+=1
                    status = "Moved South"
                elif self.direction==3: #east
                    self.x+=1
                    status = "Moved East"
            else:
                status = "Blocked by obstacle"
            
            if self.turn==masterTurn-1:
                textScroll(self.turn, status)
            
            self.turn+=1

    def moveBackward(self):
        if self.turn < masterTurn:
            if self.direction==2: # south
                if self.y > 0:
                    self.addTrail()
                    self.y-=1
            elif self.direction==3: # east
                if self.x > 0:
                    self.addTrail()
                    self.x -=1
            elif self.direction==0: #north
                if self.y <10:
                    self.addTrail()
                    self.y+=1
            elif self.direction==1: # west
                if self.x <10:
                    self.addTrail()
                    self.x+=1
            self.turn+=1
    
    def getInfo(self):
        global objects
        if self.turn < masterTurn:
            
            x, y = self.getFrontSquare(self.x, self.y, self.direction)

            gotSecret=False
            for o in objects:
                if o.type==2:
                    if x==o.x and y==o.y:
                        try:
                            secret = o.ai.getSecret()
                            if self.turn==masterTurn-1:
                                textScroll(self.turn, "Received Secret:" + str(secret))
                            gotSecret=True
                            
                        except:
                            if self.turn==masterTurn-1:
                                textScroll(self.turn, "This base does not have a secret")
            
            if gotSecret==False:
                if self.turn==masterTurn-1:
                    textScroll(self.turn, "Failed to get secret")

            self.turn+=1
            return secret


    def print(self, stuff):
        global objects
        print("printing")
        if self.turn < masterTurn:
            gaveSecret=False
            x, y = self.getFrontSquare(self.x, self.y, self.direction)
            for o in objects:
                if o.type==2:
                    if x==o.x and y==o.y:
                        try:
                            o.ai.validateSecret(stuff)
                            if self.turn==masterTurn-1:
                                textScroll(self.turn, "Printed Secret:" + str(stuff))
                            gaveSecret=True
                        except:
                            if self.turn==masterTurn-1:
                                textScroll(self.turn, "This base does not have a printer")
            if gaveSecret==False:
                if self.turn==masterTurn-1:
                    textScroll(self.turn, "Failed to print at the base")

            self.turn+=1


    def checkTerrainForward(self):
        x, y = self.getFrontSquare(self.x, self.y, self.direction)
        if 0 <=x <=9 and 0<=y<=9:
            return aryTiles[x][y][2]
        else:
            return "edge"

    def checkTerrainLeft(self):
        x, y = self.getLeftSquare(self.x, self.y, self.direction)
        if 0 <=x <=9 and 0<=y<=9:
            return aryTiles[x][y][2]
        else:
            return "edge"

    def checkTerrainRight(self):
        x, y = self.getRightSquare(self.x, self.y, self.direction)
        if 0 <=x <=9 and 0<=y<=9:
            return aryTiles[x][y][2]
        else:
            return "edge"

    def checkObjectForward(self):
        global objects
        x, y = self.getFrontSquare(self.x, self.y, self.direction)
        for o in objects:
            if o.x==x and o.y==y and o.checkAlive(o, self.turn):
                return o
        obj = object(-1,-1,0,pygame.Surface((1,1)))
        obj.type=0
        obj.name=""
        obj.health=0


        return obj

    def checkObjectLeft(self):
        global objects
        x, y = self.getLeftSquare(self.x, self.y, self.direction)
        for o in objects:
            if o.x==x and o.y==y and o.checkAlive(o, self.turn):
                return o.type, o.name
        return 0, ""

    def checkObjectRight(self):
        global objects
        x, y = self.getRightSquare(self.x, self.y, self.direction)
        for o in objects:
            if o.x==x and o.y==y and o.checkAlive(o, self.turn):
                return o.type, o.name
        return 0, ""

    def getFrontSquare(self, x, y, direction):
        newx = x
        newy = y
        if self.direction==0: # north
            newy-=1
        elif self.direction==1: # west
            newx -=1
        elif self.direction==2: #south
            newy+=1
        elif self.direction==3: #east
            newx+=1
        return newx, newy

    def getBackSquare(self, x, y, direction):
        newx = x
        newy = y
        if self.direction==0: # north
            newy+=1
        elif self.direction==1: # west
            newx +=1
        elif self.direction==2: #south
            newy-=1
        elif self.direction==3: #east
            newx-=1
        return newx, newy


    def getLeftSquare(self, x,y, direction):
        newx = x
        newy = y
        if self.direction==0: # north
            newx-=1
        elif self.direction==1: # west
            newy +=1
        elif self.direction==2: #south
            newx+=1
        elif self.direction==3: #east
            newy-=1
        return newx, newy

    def getRightSquare(self,x, y, direction):
        newx = x
        newy = y
        if self.direction==0: # north
            newx +=1
        elif self.direction==1: # west
            newy -=1
        elif self.direction==2: #south
            newx -=1
        elif self.direction==3: #east
            newy +=1
        return newx, newy

    def checkForObstacles(self, x, y):
        global objects
        # returns 0 for no obstacle
        # return 1 for obstacle
        if  y < 0  or x < 0 or y > 10 or x > 10:
            return 1
        else:
            if aryTiles[x][y][1]!=0:
                return 1
            else:
                for o in objects:
                    if (o.x == x and o.y == y and o.checkAlive(o, self.turn)):
                        return 1
                return 0

    def checkAlive(self, obj, currentTurn):
        damage =0
        for i in range(0, currentTurn):
            if i in obj.healthHistory:
                damage += obj.healthHistory[i]
        
        if obj.health+damage > 0:
            return True
        else:
            return False

    def attack(self):
        global objects
        if self.turn < masterTurn:
            x,y = self.getFrontSquare(self.x, self.y, self.direction)
            
            for o in objects:
                if o.x==x and o.y==y and o.type==1 and o.checkAlive(o, self.turn):
                    if self.turn==masterTurn-1:
                        damage = -1 * randint(5,10)
                        if self.turn in o.healthHistory:
                            o.healthHistory[self.turn] += damage
                        else:
                            o.healthHistory[self.turn] = damage
                        
                        for i in o.healthHistory:
                            o.health += o.healthHistory[i]
                        status = "Attacked for " + str(damage) + " points. Health is " + str(o.health)

        if self.turn==masterTurn-1:
            textScroll(self.turn, status)
            
        self.turn+=1

    def locateObject(self, objName):
        global objects
        for o in objects:
            if o.name==objName and o.checkAlive(o, self.turn):
                xdiff = o.x-self.x
                ydiff = o.y-self.y

                reldirection = self.getRelDirection(xdiff, ydiff, self.direction)

                return o.x,o.y, reldirection
        return
                 


    
    def locateAllOpponents(self):
        print("")

    def getRelDirection(self, xdiff, ydiff, direction):
        if xdiff>=0 and ydiff >=0:
            if abs(xdiff) > abs(ydiff):
                if direction==0:
                    return "right"
                elif direction==1:
                    return "back"
                elif direction==2:
                    return "left"
                elif direction==3:
                    return "front"
            else:
                if direction==0:
                    return "back"
                elif direction==1:
                    return "left"
                elif direction==2:
                    return "front"
                elif direction==3:
                    return "right"
        elif xdiff >=0 and ydiff < 0:
            if abs(xdiff) > abs(ydiff):
                if direction==0:
                    return "right"
                elif direction==1:
                    return "back"
                elif direction==2:
                    return "left"
                elif direction==3:
                    return "front"
            else:
                if direction==0:
                    return "front"
                elif direction==1:
                    return "right"
                elif direction==2:
                    return "back"
                elif direction==3:
                    return "left"
        elif xdiff < 0 and ydiff >= 0:
            if abs(xdiff) > abs(ydiff):
                if direction==0:
                    return "left"
                elif direction==1:
                    return "front"
                elif direction==2:
                    return "right"
                elif direction==3:
                    return "back"
            else:
                if direction==0:
                    return "back"
                elif direction==1:
                    return "left"
                elif direction==2:
                    return "front"
                elif direction==3:
                    return "right"
        elif xdiff < 0 and ydiff < 0:
            if abs(xdiff) > abs(ydiff):
                if direction==0:
                    return "left"
                elif direction==1:
                    return "front"
                elif direction==2:
                    return "right"
                elif direction==3:
                    return "back"
            else:
                if direction==0:
                    return "front"
                elif direction==1:
                    return "right"
                elif direction==2:
                    return "back"
                elif direction==3:
                    return "left"

class player(object):
    def __init__(self, coordx, coordy,  ai, direction, sImg, subType, name):
        super().__init__(coordx, coordy,direction, sImg)
        # 0 = main player,  1 = AI opponents
        self.subType = subType
        self.health=100
        self.energy=50
        self.ai = ai
        ai.robot = self
        # 1 = player1, 2=base
        self.type = 1
        self.OrigSurfImg = sImg
        self.surfImg = pygame.transform.rotate(self.OrigSurfImg, self.direction*90)
        self.direction = direction
        self.name=name
            

class base(object):
    def __init__(self, coordx, coordy, ai, direction, sImg, subType, name):
        super().__init__(coordx, coordy, direction, sImg)
        self.subType = subType
        # 1 = player1, 2=base
        self.type = 2
        self.OrigSurfImg = sImg
        self.surfImg = pygame.transform.rotate(self.OrigSurfImg, self.direction*90)
        self.direction = direction
        self.ai = ai
        ai.robot = self
        self.name=name
        self.health=100
    
    def checkTouch(self):
        # Is there a player touching the base?
        for o in objects:
            if o.type==1:
                if (self.x-1 <= o.x <= self.x+1 and self.y==o.y) or (self.x==o.x and self.y-1 <= o.y <= self.y+1):
                    return True
                else:
                    return False



def button(msg,x,y,w,h,ic,ac,action=None, param1=None, param2=None):
    btnText = pygame.font.Font("freesansbold.ttf",14)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x, y, w, h))
        if click[0] == 1 and action != None:
            if param1==None and param2==None:
                action()         
            elif param2==None:
                action(param1)
            else:
                action(param1, param2)
    else:
        pygame.draw.rect(screen, ic,(x,y, w, h))
    
    TextSurf = btnText.render(msg, 1, (200,0,0))
    TextRect = pygame.Rect(0,0,w, h)
    TextRect.center = ((x+w/2,y+h/2))
    screen.blit(TextSurf, TextRect)



def drawIntro(levels):
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
    screen.fill((0,0,0))
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf = largeText.render("HyCap PythonBot", 1, (100,255,100))
    TextRect = pygame.Rect(0,0,DISPLAY_WIDTH/2, DISPLAY_HEIGHT/4)
    TextRect.center = ((DISPLAY_WIDTH/2),(100))
    screen.blit(TextSurf, TextRect)

    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 30
    BUTTON_VERT_SPACING=10
    BUTTON_HORZ_SPACING=20
    FIRST_BUTTON_X = 50
    FIRST_BUTTON_Y=100
    btnNum=0
    col = 0
    row = 0
    for level in levels:
        
        button(level[1],FIRST_BUTTON_X+col*(BUTTON_WIDTH+BUTTON_HORZ_SPACING),FIRST_BUTTON_Y+row*(BUTTON_VERT_SPACING+BUTTON_HEIGHT),BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,action=chooseLevel, param1=level[0])

        btnNum+=1
        col = math.floor(btnNum/10)
        row = btnNum % 10

    pygame.display.update()
    clock.tick(15)

def chooseLevel(levelfile=currentLevelFile):
    global intro, aryTiles, objects, instructions, maxTurns, state, loseMsg, currentLevelFile, currentSolnFile
    global state, masterTurn, maxTurns
    masterTurn=0
    maxTurns=100
    state=""
    
    
    if levelfile !='':
        currentLevelFile = levelfile
    else:
        levelfile = currentLevelFile


    intro=False
    #Dynamically import the robots as modules
    #ai1name=input("What is the name of your bot?").strip()

    importlib.invalidate_caches()


    level = importlib.import_module(levelfile)

    aryTiles.clear()
    m = level.Map(TILESIZE)
    aryTiles=m.loadTiles()

    objects.clear()
    o = level.LevelObjects()
    los = o.loadObjects()
    maxTurns = o.MaxTurns


    i = level.Instructions()
    instructions=i.loadInstructions()

 
        

    for lo in los:
        #x,y,direction, sImg, type, SubType
        #type: 1=player, 2=base
        #subtype: 0 = real player, 1 = AI player
        if lo[4]==1:  #player
            ai1 = importlib.import_module(lo[6])
            importlib.reload(ai1)
            objects.append( player(lo[0],lo[1], ai1.AI(), lo[2], lo[3], lo[5],lo[7])) 
            if lo[5]==0:
                solnfile = lo[6]

        elif lo[4]==2:  #base
            ai = __import__(lo[6])
            try:
                objects.append( base(lo[0],lo[1], ai.AI(lo[8]),lo[2], lo[3], lo[5],lo[7]))
            except IndexError:
                objects.append( base(lo[0],lo[1], ai.AI(),lo[2], lo[3], lo[5],lo[7]))
        
    v = level.Validate()
    strVal = v.validateSoln(solnfile)
    if strVal!="":
        textScroll(strVal)
        loseMsg=strVal
        state="lose"

def GoToIntro():
    global intro

    intro=True



def drawBattlefieldPygame():
    """draws the battlefield with Pygame"""
    global state, redsquares, bluesquares, bot1img, bot2img, namefont, textfont, ai1name, ai2name, uwimg, walls, rbulimg, bbulimg, textBlob

    #Get the display surface
    screen = pygame.display.get_surface()
    

    #Clear the screen
    screen.fill((0,0,0))
    
    #draw grid lines
    for i in range(1,10):
        pygame.draw.line(screen,(50,50,50),(0,i*(TILESIZE+LINEWIDTH*2)),(600,i*(TILESIZE+LINEWIDTH*2)),LINEWIDTH)
        pygame.draw.line(screen,(50,50,50),(i*(TILESIZE+LINEWIDTH*2),0),(i*(TILESIZE+LINEWIDTH*2),600),LINEWIDTH)

    for tileRow in range(0, len(aryTiles)):
        for tile in range(0,len(aryTiles[tileRow])):
            rectground=pygame.Rect(tile*(TILESIZE+2*LINEWIDTH)+LINEWIDTH, tileRow*(TILESIZE+2*LINEWIDTH)+LINEWIDTH, TILESIZE, TILESIZE)
            screen.blit(aryTiles[tile][tileRow][0], rectground)

    #Objects
    numOfPlayers=0
    for o in objects:
        #for players
        if o.type==1:
            #Draw the robot's health bars
            text = font.render(o.name, True, WHITE) 
            if o.checkAlive(o, masterTurn):
                screen.blit(text, pygame.Rect(600,4+ 45*numOfPlayers, 195, 10))
                pygame.draw.rect(screen,(0,255,0),((600,22+ 45*numOfPlayers),(int(o.health*195/100.0),10)))
                screen.blit(o.surfImg, o.getRect())
            if o.energy > 0:
                screen.blit(smallfont.render("Health", True, BLACK), pygame.Rect(600,22+ 45*numOfPlayers, 195, 10))
                pygame.draw.rect(screen,(255,255,0),((600,34+ 45*numOfPlayers),(int(o.energy*195/100.0),10)))
            screen.blit(smallfont.render("Energy", True, BLACK), pygame.Rect(600,34+ 45*numOfPlayers, 195, 10))
            numOfPlayers+=1
        elif o.type==2:
            if o.checkAlive(o, masterTurn):
                screen.blit(o.surfImg, o.getRect())

        
        
        s = pygame.Surface((TILESIZE,TILESIZE))  # the size of your rect
        s.set_alpha(50)                # alpha level
        s.fill((25,25,255))           # this fills the entire surface
        for t in o.trail:

            trailRect = pygame.Rect(t[0]*(TILESIZE+2*LINEWIDTH)+LINEWIDTH, t[1]*(TILESIZE+2*LINEWIDTH)+LINEWIDTH, TILESIZE, TILESIZE)
            screen.blit(s, trailRect)    # (0,0) are the top-left coordinates


    #textScroll
    drawText(screen, textBlob, (255, 255, 255), (603,155,194,600), textfont, aa=True, bkg=(255, 255, 0))

    rectw = 600
    recth = 200
    NOTE_X = 0
    NOTE_Y = 600
    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 30
    BUTTON1_X = 20
    BUTTON1_Y = DISPLAY_HEIGHT - 20 - BUTTON_HEIGHT
    BUTTON2_X = BUTTON1_X + BUTTON_WIDTH + 20
    BUTTON2_Y = BUTTON1_Y
    if masterTurn==0:
        sInstructions = pygame.Surface((rectw, recth))
        sInstructions.fill(DARK_GRAY)
        rectInstructions=pygame.Rect(NOTE_X, NOTE_Y, rectw, recth)
        screen.blit(sInstructions, rectInstructions)
        drawText(screen, instructions, (255,255,255), rectInstructions, instructionFont, aa=True, bkg=(255,255,255))

    if state=="win":
        sInstructions = pygame.Surface((rectw, recth))
        sInstructions.fill(DARK_GRAY)
        rectInstructions=pygame.Rect(NOTE_X, NOTE_Y, rectw, recth)
        screen.blit(sInstructions, rectInstructions)
        drawText(screen, "You did it!", (255,255,255), rectInstructions, instructionFont, aa=True, bkg=(255,255,255))
        button("New Level",BUTTON1_X, BUTTON1_Y,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,action=GoToIntro)
    elif state=="lose":
        sInstructions = pygame.Surface((rectw, recth))
        sInstructions.fill(DARK_GRAY)
        rectInstructions=pygame.Rect(NOTE_X, NOTE_Y, rectw, recth)
        screen.blit(sInstructions, rectInstructions)
        drawText(screen, loseMsg, (255,255,255), rectInstructions, instructionFont, aa=True, bkg=(255,255,255))


        button("Try Again",BUTTON1_X, BUTTON1_Y,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,action=chooseLevel)
        button("Back to Levels",BUTTON2_X,BUTTON2_Y,BUTTON_WIDTH,BUTTON_HEIGHT,GREEN,BRIGHT_GREEN,action=GoToIntro)
    pygame.display.update()

    #add a delay between frames
    if masterTurn==0:
        time.sleep(3)
    elif state!="":
        time.sleep(.05)
    else:
        time.sleep(.5)
    


def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    """
    Takes the parameters of surface, which is where the text is going
    to be displayed,cf.surface for example and the text, which is
    whatever text we want to be displayed, the color, which is
    well, the color (0,0,0) input format, and the font is the location
    of the font you would like to use alternatively. This function
    then calculates the maximum we can fit in the size of our textbox
    and draws it to our surface with whichever parameters we give.
    """
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = 0
    # get the height of the font
    fontHeight = font.size('Tg')[1]
    # Split by newline.
    sp_text = text.split('\n')
    # Loop through text.
    for text in sp_text:
        # Old code to print to screen.
        while text:
            i = 1
            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break
            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1
            temp = text[:i].strip()
            # if we've wrapped the text, then adjust the wrap to the
            # last word
            if i < len(text):
                i = text.rfind(' ', 0, i) + 1
            # render the line and blit it to the surface
            if bkg:
                image = font.render(temp[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(temp[:i], aa, color)
            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing
            # Remove leading and trailing newline and spaces.
            text = text[i:].strip() 

def textScroll(turn, msg):
    global textList, textBlob
    
    textList.insert(0, str(turn) + "-" + msg)

    if len(textList) > 20:
        textList.pop()
    
    textBlob = ""
    for text in textList:
#        print(text)
        if len(textList) == 1:
            textBlob = text
        else:
            textBlob = textBlob + "\n" + text



levels = []
f = open("levels.dat", "r")
strLine = f.readline()
levels.append(strLine.strip().split(":"))
while strLine:
    strLine = f.readline()
    if strLine!="":
        levels.append(strLine.strip().split(":"))




while True:

    if intro:
        drawIntro(levels)

    else:

        if state!="":
            drawBattlefieldPygame()
        else:
            if masterTurn > maxTurns:
                state="lose"
                loseMsg="You must finish this level in less than " + str(maxTurns) + " turns."

            
            #if state=="" and len(textList) > 0:
                #if "This is turn:" not in textList[0]:
                    #textScroll("This is turn:" + str(masterTurn))

            drawBattlefieldPygame()
            
            #player loop
            for o in objects:
                if o.type==1:
                    try: # Prevent PythonBattle from crashing when AI code fails
                        o.reset()
                        o.ai.turn()

                        if state == "win":
                            break
                    except Exception as e:
                        print("failed with error:")
                        print(e)
            
            #base loop
            missionsleft=0
            for o in objects:
                if o.type==2:
                    try:
                        if o.ai.turn()==2:
                            state="win"
                            break
                        elif o.ai.turn()==0:
                            missionsleft+=1
                    except Exception as e:
                        print("failed with error:")
                        print(e)
                #AI
                if o.type==1 and o.subType==1:
                    try:
                        if o.ai.turn()==2:
                            state="win"
                            break
                        elif o.ai.turn()==0:
                            missionsleft+=1
                    except Exception as e:
                        print("failed with error:")
                        print(e) 

            if missionsleft==0:
                state="win"


            masterTurn+=1 
            # Capture all events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # key codes: https://www.pygame.org/docs/ref/key.html
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

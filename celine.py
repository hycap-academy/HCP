# pythonbattle.py
# Copyright Warren & Carter Sande, 2013
# Released under MIT license   http://www.opensource.org/licenses/mit-license.php
# Version $version  ----------------------------

# This is the PythonBattle program that runs the AI's against each other.
# It generates the play grid using Pygame and runs the battle.

import pygame #ASCII/PYGAME
import time
import random
import os
from tkinter import *
pygame.init() #ASCII/PYGAME



class OutOfTurnError(Exception):
    """ A custom exception describing a state in which a robot moves out of turn"""
    def __init__(self,botname):
        self.botname = botname
    def __str__(self):
        return "Robot "+self.botname+" tried to call function when it wasn't his turn"

class RobotIsDefeatedError(Exception):
    """ A custom exception describing a state in which a robot moves while it
is defeated."""
    def __init__(self,botname):
        self.botname = botname
    def __str__(self):
        return "Robot "+self.botname+" tried to call function while defeated"


class Robot:
    """A player in the battle. 
    Rotation values:
    0: Up
    1: Right
    2: Down
    3: Left
    
    Note: All methods starting with _ are PRIVATE. Do not
    call them under any circumstances.  """
    
    def __init__(self,name,ai,position,rotation, mapnum):
        self.name = name
        self.ai = ai
        ai.robot = self
        self.position = position
        self.rotation = rotation
        self.health = 100
        self.energy = 30
        self.mapnum = mapnum
        self._teleports = 5
        self.backfire = 0
    def _spaceInFront(self):
        if self.rotation == 0:
            return (self.position[0],self.position[1]-1)
        elif self.rotation == 1:
            return (self.position[0]+1,self.position[1])
        elif self.rotation == 2:
            return (self.position[0],self.position[1]+1)
        elif self.rotation == 3:
            return (self.position[0]-1,self.position[1])
    def _getSpace(self,space):
        global field
        if space == self.position:
            return "me"
        else:
            for i in field:
                if i.position == space:
                    return "bot"
        if space[0]<1:
            return "wall"
        elif space[1]<1:
            return "wall"
        elif space[0]>10:
            return "wall"
        elif space[1]>10:
            return "wall"
        # Round 2
        elif self.mapnum == 1 and ((space[0] == 3 and space[1] == 3) or (space[0] == 3 and space[1] == 8) or (space[0] == 8 and space[1] == 3) or (space[0] == 8 and space[1] == 8)):
            return "wall"
        elif self.mapnum == 2 and ((space[0] == 2 and space[1] == 2) or (space[0] == 2 and space[1] == 9) or (space[0] == 9 and space[1] == 2) or (space[0] == 9 and space[1] == 9)):
            return "wall"
        elif self.mapnum == 3 and ((space[0] == 3 and space[1] == 5) or (space[0] == 3 and space[1] == 6) or (space[0] == 8 and space[1] == 5) or (space[0] == 8 and space[1] == 6)):
            return "wall"
        else:
            return "clear"
    def _goForth(self):
        if self._getSpace(self._spaceInFront()) == "clear":
            self.position = self._spaceInFront()
            return "success"
        else:
            return self._getSpace(self._spaceInFront())
    def _goBack(self):
        self._turnLeft()
        self._turnLeft()
        if self._getSpace(self._spaceInFront()) == "clear":
            self.position = self._spaceInFront()
            self._turnRight()
            self._turnRight()
            return "success"
        else:
            result = self._getSpace(self._spaceInFront())
            self._turnRight()
            self._turnRight()
            return result
    def _turnLeft(self):
        self.rotation -= 1
        self.rotation %= 4
        return "success"
    def _turnRight(self):
        self.rotation += 1
        self.rotation %= 4
        return "success"
    def _attack(self):
        global field
        for i in field:
            if i.position == self._spaceInFront():
                i.takeDamage(10)
                return self.name + " attacks " + i.name + " for 10 damage."
        return self._getSpace(self._spaceInFront())
    def _beforeMove(self):
        """Check if the robot is moving out of turn or while defeated."""
        global state
        if (state != self.name) and (state != "win"):
            raise OutOfTurnError(self.name)
        elif state == "win":
            raise RobotIsDefeatedError(self.name)

    def _afterMove(self):
        """When a robot has moved, changes the state of the game so it's the
other robot's turn."""
        global field, state
        self._gainEnergy()
        if state == self.name:
            for i in field:
                if i.name != self.name:
                    state = i.name    
                    
    def _gainEnergy(self):
        self.energy += 10
        if self.energy > 100:
            self.energy = 100
    
    def _getRandomOpenSpace(self):    
        rand1 = random.randint(1,10)
        rand2 = random.randint(1,10)
        randtup = (rand1, rand2)
        if self._getSpace(randtup) == "clear":
            return randtup
        else:
            return self._getRandomOpenSpace()
            
    def _telecheck(self):
        if self._teleports > 0:
            self._teleports -= 1
            return True
        else:
            return False
            
    def _toss(self):
        global field
        if self.energy >= 70:
            self.energy -= 80
            for i in field:
                if i.position == self._spaceInFront():
                    randtup = self._getRandomOpenSpace()
                    i.takeDamage(20)
                    i.position = randtup
                    i.rotation = random.randint(0,3)
                    return self.name + " tossed " + i.name + " into the air and caused 20 damage."
                elif i.name != self.name and i.position != self._spaceInFront():
                    return self.name + " used their toss ability and tossed the air because no bot was in front of them."
        else:
            return self.name + " tried to use toss but did not have enough energy."
    
    def _backfireChance(self):
        if self.backfire < 100:
            self.backfire += random.randint(1,20)
        elif self.backfire > 100:
            self.backfire = 100
        return self.backfire
    
    def _luckyshot(self):
        global field
        if self.energy >= 50:
            self.energy -= 60
            backfireroll = random.randint(1,100)
            backfirechance = self._backfireChance() 
            if backfireroll <= (100 - backfirechance):
                for i in field:
                    if i.name != self.name:
                        randdmg = random.randint(5,30)
                        i.takeDamage(randdmg)
                        return self.name + " shot " + i.name + " for " + str(randdmg) + " damage!"
            else:
                randdmg = random.randint(5,15)
                self.takeDamage(randdmg)
                return self.name + " used luckyshot, but the shot backfired and he/she took " + str(randdmg) + " damage!"
        else:
            return self.name + " tried to use luckyshot but did not have enough energy."
        
    def _teleport(self):
        if self.energy >= 80:
            if self._telecheck() == True:
                self.energy -= 90
                enemy_loc = self.locateEnemy()
                enemy_coords = enemy_loc[0]
                enemy_rot = enemy_loc[1]
                if enemy_rot == 0:
                    telecoords = (enemy_coords[0],enemy_coords[1]+1)
                elif enemy_rot == 1:
                    telecoords = (enemy_coords[0]-1,enemy_coords[1])
                elif enemy_rot == 2:
                    telecoords = (enemy_coords[0],enemy_coords[1]-1)
                elif enemy_rot == 3:
                    telecoords = (enemy_coords[0]+1,enemy_coords[1])
                if self._getSpace(telecoords) == "clear":
                    self.position = telecoords
                    self.rotation = enemy_rot
                    return self.name + " teleported behind their opponent."
                else: 
                    self.takeDamage(10)
                    return self.name + " attempted to teleport into a wall and took 10 damage."
            elif self._telecheck() == False:
                return self.name + " tried to use teleport but their teleporter is broken."
        else:
            return self.name + " tried to use teleport but did not have enough energy."
        
    def _repair(self):
        if self.energy >= 20 and self.health <= 90:
            self.health += 10
            self.energy -= 30
            return self.name + " repaired 20 damage successfully."
        elif self.health > 90:
            self.health = 100
            return self.name + " wasted a heal and has 100 health."
        else:
            return self.name + " tried to use repair but did not have enough energy."
        
    def _escape(self):
        if self.energy >= 30:
            if self._telecheck() == True:
                self.energy -= 40
                self.position = self._getRandomOpenSpace()
                self.rotation = random.randint(0,3)
                return self.name + " used escape and teleported away randomly."
            elif self._telecheck() == False:
                return self.name + " tried to use escape but their teleporter is broken."
        else:
            return self.name + " tried to use escape but did not have enough energy."
        
    def _crush(self):
        global field
        if self.energy >= 40:
            self.energy -= 50
            for i in field:
                if i.position == self._spaceInFront():
                    randdmg = random.randint(15,25)
                    i.takeDamage(randdmg)
                    return self.name + " crushes " + i.name + " for " + str(randdmg) + " damage."
                elif i.name != self.name and i.position != self._spaceInFront():
                    return self.name + " crushes the ground in front of them! Too bad no bot was there."
            return self._getSpace(self._spaceInFront())
        else:
            return self.name + " tried to use crush but did not have enough energy."
        
    def calculateCoordinates(self,distance=1,direction=None,position=None):
        """Convenience function for calculating positions.
        Returns the coordinates of the position described."""
        if direction == None:
            directionToCheck = self.rotation
        else:
            directionToCheck = direction
        if position == None:
            locationToReturn = self.position
        else:
            locationToReturn = position
        directionToCheck %= 4
        for i in range(distance):
            if directionToCheck == 0:
                locationToReturn= (locationToReturn[0],locationToReturn[1]-1)
            elif directionToCheck == 1:
                locationToReturn= (locationToReturn[0]+1,locationToReturn[1])
            elif directionToCheck == 2:
                locationToReturn= (locationToReturn[0],locationToReturn[1]+1)
            elif directionToCheck == 3:
                locationToReturn= (locationToReturn[0]-1,locationToReturn[1])
        return locationToReturn
    def lookInFront(self):
        "Looks at the space in front of the robot"
        return self.lookAtSpace(self.calculateCoordinates())
    def lookAtSpace(self,space):
        "Checks a space"
        return self._getSpace(space)
    def takeDamage(self,damage):
        "Don't call. Makes this robot take damage."
        global state, field
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            state = "win"
    def attack(self):
        "Attacks"
        self._beforeMove()
        result = self._attack()
        self._afterMove()
        textScroll(result)
        return result
    def goBack(self):
        "Moves backwards"
        self._beforeMove()
        result = self._goBack()
        self._afterMove()
        return result
    def goForth(self):
        "Moves forwards"
        self._beforeMove()
        result = self._goForth()
        self._afterMove()
        return result
    def turnLeft(self):
        "turns left"
        self._beforeMove()
        result = self._turnLeft()
        self._afterMove()
        return result
    def charge(self):
        "Does nothing, ending the turn"
        self._beforeMove()
        self._gainEnergy()
        result = self.name + " charges."
        textScroll(result)
        self._afterMove()
        return result
    def turnRight(self):
        "Turns right"
        self._beforeMove()
        result = self._turnRight()
        self._afterMove()
        return result
    def locateEnemy(self):
        "Returns the coordinates of an enemy"
        global field
        for i in field:
            if i.name != self.name:
                return i.position, i.rotation
    def teleport(self):
        "_teleports"
        self._beforeMove()
        result = self._teleport()
        textScroll(result)
        self._afterMove()
        return result
    def toss(self):
        "Tosses the opponent and does damage"
        self._beforeMove()
        result = self._toss()
        textScroll(result)
        self._afterMove()
        return result
    def repair(self):
        "Repairs"
        self._beforeMove()
        result = self._repair()
        self._afterMove()
        textScroll(result)
        return result
    def luckyshot(self):
        "Shoots at the enemy. Can backfire"
        self._beforeMove()
        result = self._luckyshot()
        self._afterMove()
        textScroll(result)
        return result
    def escape(self):
        "Randomly _teleports away"
        self._beforeMove()
        result = self._escape()
        self._afterMove()
        textScroll(result)
        return result
    def crush(self):
        "Crushes the enemy for 15-25 damage"
        self._beforeMove()
        result = self._crush()
        textScroll(result)
        self._afterMove()
        return result
    def checkEnergy(self):
        return self.energy

def drawBattlefield(bot1, bot2):
    """draws a battlefield with ASCII.
    Replace all instances of drawBattlefieldPygame with this function
    to draw the battlefield in ASCII art.

    Does not draw red or blue squares."""
    output = ""
    for row in range(12):
        for column in range(12):
            if row in [0,11]:
                #draw wall
                output += "--"
            elif column in [0,11]:
                #draw wall
                output += "||"
            elif (column,row) == bot1.position:
                #draw robot 1
                output += ["^",">","V","<"][bot1.rotation]+"1"
            elif (column,row) == bot2.position:
                #draw robot 2
                output += ["^",">","V","<"][bot2.rotation]+"2"
            else:
                output += "  "
        output += "\n"
    print(output)
    #Display robot health
    print("Bot 1's Health:",bot1.health)
    print("Bot 2's Health:",bot2.health)

def drawBattlefieldPygame(bot1, bot2):
    """draws the battlefield with Pygame"""
    global state, redsquares, bluesquares, bot1img, bot2img, namefont, textfont, ai1name, ai2name, uwimg, walls, rbulimg, bbulimg, textBlob

    #Get the display surface
    screen = pygame.display.get_surface()
    
    #If the Pygame window isn't open, open it.
    if screen == None:
        screen = pygame.display.set_mode((800,600))
    #Clear the screen
    screen.fill((0,0,0))
    #Draw colored squares
    for i in redsquares:
        pygame.draw.rect(screen,(80,0,0),((  (i[0]-1)*60,(i[1]-1)*60  ),(60,60)))
    for i in bluesquares:
        pygame.draw.rect(screen,(0,0,80),(((i[0]-1)*60,(i[1]-1)*60),(60,60)))
    #draw grid lines
    for i in range(1,10):
        pygame.draw.line(screen,(50,50,50),(0,i*60),(600,i*60),5)
        pygame.draw.line(screen,(50,50,50),(i*60,0),(i*60,600),5)    
    for i in walls:
        screen.blit(uwimg, ((((i[0]-1)*60)-1), (((i[1]-1)*60)-1)))
        
    #Get the screen positions of the robots
    bot1pos = ((bot1.position[0]-1)*60,(bot1.position[1]-1)*60)
    bot2pos = ((bot2.position[0]-1)*60,(bot2.position[1]-1)*60)
    #Draw the robots on the screen
    screen.blit(pygame.transform.rotate(bot1img,-90*bot1.rotation),bot1pos)
    screen.blit(pygame.transform.rotate(bot2img,-90*bot2.rotation),bot2pos)
    #Write the names of the robots on the screen
    screen.blit(namefont.render(ai1name,True,(255,0,0),(0,0,0)),(600,0))
    screen.blit(namefont.render(ai2name,True,(0,0,255),(0,0,0)),(600,80))
    #Draw the robot's health bars
    pygame.draw.rect(screen,(0,255,0),((600,22),(int(bot1.health*195/100.0),10)))
    pygame.draw.rect(screen,(255,255,0),((600,34),(int(bot1.energy*195/100.0),10)))
    if bot1._teleports >= 1:
        screen.blit(rbulimg, (605, 50))
    if bot1._teleports >= 2:
        screen.blit(rbulimg, (630, 50))
    if bot1._teleports >= 3:    
        screen.blit(rbulimg, (655, 50))
    if bot1._teleports >= 4:   
        screen.blit(rbulimg, (680, 50))
    if bot1._teleports == 5:       
        screen.blit(rbulimg, (705, 50))
    pygame.draw.rect(screen,(0,255,0),((600,102),(int(bot2.health*195/100.0),10)))
    pygame.draw.rect(screen,(255,255,0),((600,114),(int(bot2.energy*195/100.0),10)))
    if bot2._teleports >= 1:
        screen.blit(bbulimg, (605, 130))
    if bot2._teleports >= 2:
        screen.blit(bbulimg, (630, 130))
    if bot2._teleports >= 3:    
        screen.blit(bbulimg, (655, 130))
    if bot2._teleports >= 4:   
        screen.blit(bbulimg, (680, 130))
    if bot2._teleports == 5:       
        screen.blit(bbulimg, (705, 130))
#    textsurface = textfont.render(textBlob, False, (0, 255, 255))
#    rect = pygame.draw.rect(screen,(255,255,0),(603,155,194,440))
    drawText(screen, textBlob, (255, 255, 255), (603,155,194,440), textfont, aa=True, bkg=(255, 255, 0))
#    screen.blit(textsurface,(601,155))
    pygame.display.update()
    #If the game is over...
    if state == "win":
        running = True
        #wait for the user to close the window
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
    else:
        #Otherwise, add a delay between frames
        time.sleep(.5)


def randomPosition(walls):
    global field, state
    rand1 = random.randint(1,10)
    rand2 = random.randint(1,10)
    randtup = (rand1, rand2)
    for wall in walls:
        if wall[0] == rand1 and wall[1] == rand2:
             randtup = randomPosition(walls)
    return randtup

def textScroll(msg):
    global textList, textBlob
    
    textList.insert(0, msg)

    if len(textList) > 10:
        textList.pop()
    
    textBlob = ""
    for text in textList:
#        print(text)
        if len(textList) == 1:
            textBlob = text
        else:
            textBlob = textBlob + "\n" + text
    

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
    
textList = []
textBlob = ""
mapnum = random.randint(1,3)
#print("Random number: " + str(mapnum))
if mapnum == 1:
    walls = [(3,3), (3,8), (8,3), (8,8)] # Map round 2
if mapnum == 2:
    walls = [(2,2), (2,9), (9,2), (9,9)] # Map round 2
if mapnum == 3:
    walls = [(3,5), (3,6), (8,5), (8,6)] # Map round 2

#Create Font object
namefont = pygame.font.Font(None,25)
#textfont = pygame.font.Font(None, 20)
textfont = pygame.font.SysFont("Arial", 20)
#Get names of competitors

master = Tk()
Label(master, text="AI #1").grid(row=0)
Label(master, text="AI #2").grid(row=1)
e1 = Entry(master)
e2 = Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

ai1name = ""
ai2name = ""
def callback(Event=None):
    global ai1name, ai2name
    ai1name = e1.get()
    ai2name = e2.get()
    master.destroy()

master.bind('<Return>', callback)
b = Button(master, text = "OK", width = 10, command = callback).grid(row=3, column=0, sticky=W, pady=4)
master.mainloop()

#ai1name = input("Enter red AI: ")
#ai2name = input("Enter blue AI: ")
#Dynamically import the robots as modules
ai1 = __import__(ai1name) 
ai2 = __import__(ai2name)
#Create the two Robot objects with the two AI objects
bot1ai = ai1.AI()
bot2ai = ai2.AI()
field = [Robot("red",bot1ai,randomPosition(walls),random.randint(0,3), mapnum),Robot("blue",bot2ai,randomPosition(walls),random.randint(0,3), mapnum)]
redsquares = []
bluesquares = []
state = "red"

pygame.display.set_mode((800,600))
#Load graphics, draw initial battlefield
script_dir = os.path.dirname(__file__)
bot1img = pygame.image.load(script_dir + "\\DozerRed.png").convert_alpha()
bot2img = pygame.image.load(script_dir + "\\DozerBlue.png").convert_alpha()
rbulimg = pygame.image.load(script_dir + "\\red_bullet.png").convert_alpha()
bbulimg = pygame.image.load(script_dir + "\\blue_bullet.png").convert_alpha()
uwimg = pygame.image.load(script_dir + "\\uwlogo.png").convert_alpha()
drawBattlefieldPygame(field[0],field[1]) #ASCII/PYGAME


numberOfTurns = 0

#firsttime = 0

while state != "win":
    #color squares
    if not (field[0].position[0],field[0].position[1]) in redsquares:
        redsquares.append((field[0].position[0],field[0].position[1]))
        while (field[0].position[0],field[0].position[1]) in bluesquares:
            bluesquares.remove((field[0].position[0],field[0].position[1]))
    if not (field[1].position[0],field[1].position[1]) in bluesquares:
        bluesquares.append((field[1].position[0],field[1].position[1]))
        while (field[1].position[0],field[1].position[1]) in redsquares:
            redsquares.remove((field[1].position[0],field[1].position[1]))
#    if firsttime != 1:
    drawBattlefieldPygame(field[0],field[1]) #ASCII/PYGAME
#        firsttime = 1
    for i in field:
        try: # Prevent PythonBattle from crashing when AI code fails
            i.ai.turn()
            if state == "win":
                break
            else:
                drawBattlefieldPygame(field[0],field[1]) #ASCII/PYGAME
        except Exception as e:
            print(i.name,"failed with error:")
            print(e)
    numberOfTurns += 1
    if numberOfTurns == 100:
        #If the battle runs longer than ~1.6 min, pull the plug
        state = "stalemate"
        break
#Color squares one last time
if not (field[0].position[0],field[0].position[1]) in redsquares:
    redsquares.append((field[0].position[0],field[0].position[1]))
    while (field[0].position[0],field[0].position[1]) in bluesquares:
        bluesquares.remove((field[0].position[0],field[0].position[1]))
if not (field[1].position[0],field[1].position[1]) in bluesquares:
    bluesquares.append((field[1].position[0],field[1].position[1]))
    while (field[1].position[0],field[1].position[1]) in redsquares:
        redsquares.remove((field[1].position[0],field[1].position[1]))
if state == "stalemate":
    drawBattlefieldPygame(field[0],field[1])#ASCII/PYGAME
    textScroll("Turn limit reached!")
    #If either robot has higher health, it wins
    if field[0].health > field[1].health:
        textScroll("Red wins!")
    elif field[1].health > field[0].health:
        textScroll("Blue wins!")
    else:
        #Otherwise, whoever has the most squares wins
        textScroll("Stalemate detected!")
        textScroll("Counting colored squares...")
        time.sleep(2) #Pause for dramatic effect...
        if len(redsquares) > len(bluesquares):
            textScroll("The winner is Red with " + str(len(redsquares)) + " squares!")
            textScroll("(Blue had " + str(len(bluesquares)) + " squares)")
        elif len(redsquares) < len(bluesquares):
            textScroll("The winner is Blue with " + str(len(bluesquares)) + " squares!")
            textScroll("(Red had " + str(len(redsquares)) + " squares)")
        else:
            textScroll("Tie! Both opponents had " + str(len(redsquares)) + " squares.")
    drawBattlefieldPygame(field[0],field[1])
    state = "win"
else:
    #print who wins
    if field[0].health > field[1].health:
        textScroll("Red wins with "+ str(field[0].health) + " health!")
    if field[1].health > field[0].health:
        textScroll("Blue wins with " + str(field[1].health) + " health!")
drawBattlefieldPygame(field[0],field[1])     #ASCII/PYGAME
pygame.quit() #ASCII/PYGAME

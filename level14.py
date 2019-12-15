#  if/then 6
import pygame
import random
import maptranslator

class Map():
    def __init__(self, TILESIZE):
        self.TILESIZE = TILESIZE


    def loadTiles(self):
        
        map ="""g1g1g1g1g1g1g1g1g1g1
                g1g1g1g1wvg1g1g1g1g1
                g1g1g1g1wvg1g1g1g1g1
                g1g1g1g1wvg1g1g1g1g1
                g1g1g1g1wvg1g1g1g1g1
                g1g1g1g1wvg1g1g1g1g1
                g1g1g1g1wvg1g1g1g1g1
                g1g1g1g1wvg1g1g1g1g1
                g1g1g1g1wvg1g1g1g1g1
                g1g1g1g1g1g1g1g1g1g1"""



        m = maptranslator.MapMaker()
        mapTiles = m.makeMap(map)

        return mapTiles

class LevelObjects():
    def __init__(self):
        print("loading level objects")
        self.MaxTurns=150

    def loadObjects(self):

        
        levelObjects=[]
        #x,y,direction, imgFile, type, SubType, AI File
        #type: 1=player, 2=base
        # direction: 0=north, 1=west, 2=south, 3=east
        m = maptranslator.MapMaker()
        soln= __name__.replace("level", "soln")
        levelObject=[3,4,3,m.getSurf("dozerblue"),1,0, soln, "player blue"]
        levelObjects.append(levelObject)
        randy = random.randrange(2,8) 
        randx = random.randrange(7,9)
        levelObject=[randx,randy,0, m.getSurf("basered"), 2,1, "baseAIPrintOnly", "base 1", "butterfly"]
        levelObjects.append(levelObject)
        return levelObjects

class Instructions():
    def __init__(self):
        print("loading instructions")

    def loadInstructions(self):
        strInstr = "Move your dozer to the red base, \n" 
        strInstr += "using moveForward() less than 6 times."
        strInstr += "Detect the base by using: \n"
        strInstr += "self.robot.checkObjectForward()"
        strInstr += "then use the self.robot.print(\"butterfly\"), \n"
        return strInstr

class Validate():
    def __init__(self):
        print("loading validation")

    def validateSoln(self, filename):
        filename = filename+".py"
        f = open(filename, "r")

        inCode=False
        hasIf=False
        NumOfMoveForward=0
        line=f.readline()

        while line:
            line = line.strip()
            if inCode==False:
                if line[:3]=="###":
                    inCode=True
            else:
                if line[:2]=="if":
                    hasIf=True
                if line.strip()[:1]!="#":
                    if "moveForward" in line:
                        NumOfMoveForward+=1

            line=f.readline()
        
        if NumOfMoveForward < 6 and hasIf:
            return ""
        else:
            return "You must use an if statement \n and no more than 5 moveForward\n commands."

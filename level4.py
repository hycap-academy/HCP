import pygame
import maptranslator

class Map():
    def __init__(self, TILESIZE):
        self.TILESIZE = TILESIZE


    def loadTiles(self):
        map ="""wqwhweg1g1g1g1g1g1g1
                wvg1wvg1g1g1g1g1g1g1
                wvg1wvg1g1g1g1g1g1g1
                wvg1wzwhwhwhg1g1g1g1
                wvg1g1g1g1g1g1g1g1g1
                wzwhwhwhwhwhg1g1g1g1
                g1g1g1g1g1g1g1g1g1g1
                g1g1g1g1g1g1g1g1g1g1
                g1g1g1g1g1g1g1g1g1g1
                g1g1g1g1g1g1g1g1g1g1"""

        m = maptranslator.MapMaker()
        mapTiles = m.makeMap(map)

        return mapTiles

class LevelObjects():
    def __init__(self):
        print("loading level objects")
        self.MaxTurns=25

    def loadObjects(self):
        levelObjects=[]
        #x,y,direction, imgFile, type, SubType, AI File
        #type: 1=player, 2=base
        # direction: 0=north, 1=west, 2=south, 3=east
        m = maptranslator.MapMaker()
        soln= __name__.replace("level", "soln")
        levelObject=[1,1,3,m.getSurf("dozerblue"),1,0, soln, "player blue"]
        levelObjects.append(levelObject)
        levelObject=[5,4,0, m.getSurf("basered"), 2,1, "baseAITouchbase", "base 1"]
        levelObjects.append(levelObject)
        return levelObjects

class Instructions():
    def __init__(self):
        print("loading instructions")

    def loadInstructions(self):
        return "Move your dozer to the red base \n by using a single self.robot.moveForward() \ncommand and a for loop."


class Validate():
    def __init__(self):
        print("loading validation")

    def validateSoln(self, filename):
        filename = filename+".py"
        f = open(filename, "r")

        inCode=False
        hasForLoop=False
        NumOfMoveForward=0
        line=f.readline()

        while line:
            line = line.strip()
            if inCode==False:
                if line[:3]=="###":
                    inCode=True
            else:
                if line[:3]=="for":
                    hasForLoop=True
                if line.strip()[:1]!="#":
                    if "moveForward" in line:
                        NumOfMoveForward+=1

            line=f.readline()
        
        if NumOfMoveForward < 3 and hasForLoop:
            return ""
        else:
            return "You must use 2 for loops\n and no more than 2 moveForward\n commands."

import pygame
import maptranslator

class Map():
    def __init__(self, TILESIZE):
        self.TILESIZE = TILESIZE


    def loadTiles(self):
        map ="""wqwhwhwhweg1g1g1g1g1
                wvg1g1g1wvg1g1g1g1g1
                wzwhweg1wvg1g1g1g1g1
                g1g1wvg1wvg1g1g1g1g1
                g1g1wvg1wzwhg1g1g1g1
                g1g1wvg1g1g1g1g1g1g1
                g1g1wzwhwhwhg1g1g1g1
                g1g1g1g1g1g1g1g1g1g1
                g1g1g1g1g1g1g1g1g1g1
                g1g1g1g1g1g1g1g1g1g1"""

        m = maptranslator.MapMaker()
        mapTiles = m.makeMap(map)

        return mapTiles

class LevelObjects():
    def __init__(self):
        print("loading level objects")
        self.MaxTurns=15

    def loadObjects(self):
        levelObjects=[]
        #x,y,direction, imgFile, type, SubType, AI File
        #type: 1=player, 2=base
        # direction: 0=north, 1=west, 2=south, 3=east
        m = maptranslator.MapMaker()
        soln= __name__.replace("level", "soln")
        levelObject=[1,1,3,m.getSurf("dozerblue"),1,0, soln, "player blue"]
        levelObjects.append(levelObject)
        levelObject=[5,5,0, m.getSurf("basered"), 2,1, "baseAITouchbase", "base 1"]
        levelObjects.append(levelObject)
        return levelObjects

class Instructions():
    def __init__(self):
        print("loading instructions")

    def loadInstructions(self):
        return "Move your dozer to the red base \n by using the\n self.robot.moveForward()\n self.robot.turnLeft()\n self.robot.turnRight() commands."

class Validate():
    def __init__(self):
        print("loading validation")

    def validateSoln(self, filename):
        return ""

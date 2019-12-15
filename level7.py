import pygame
import maptranslator
import random

class Map():
    def __init__(self, TILESIZE):
        self.TILESIZE = TILESIZE


    def loadTiles(self):
        
        map = """wqwhwhwhwhwhg1g1g1g1
                wvg1g1g1g1g1g1g1g1g1
                wzwhwhwhwhwhg1g1g1g1
                g1g1g1g1g1g1g1g1g1g1
                g1g1g1g1g1g1g1g1g1g1
                g1g1g1g1g1g1g1g1g1g1
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
        secret = random.randrange(1,100) 
        levelObjects=[]
        #x,y,direction, imgFile, type, SubType, AI File
        #type: 1=player, 2=base
        # direction: 0=north, 1=west, 2=south, 3=east
        m = maptranslator.MapMaker()
        soln= __name__.replace("level", "soln")
        levelObject=[1,1,3,m.getSurf("dozerblue"),1,0,soln, "player blue"]
        levelObjects.append(levelObject)
        levelObject=[5,1,0, m.getSurf("basered"), 2,1, "baseAITellSecret", "base 1", secret]
        levelObjects.append(levelObject)
        return levelObjects

class Instructions():
    def __init__(self):
        print("loading instructions")

    def loadInstructions(self):
        return "Move your dozer to the red base, \n get the secret code by using\n self.robot.getInfo(),\n then print using self.robot.print()."

class Validate():
    def __init__(self):
        print("loading validation")

    def validateSoln(self, filename):
        return ""

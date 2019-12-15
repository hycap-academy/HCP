# locate 2
import pygame
import random
import maptranslator

class Map():
    def __init__(self, TILESIZE):
        self.TILESIZE = TILESIZE


    def loadTiles(self):
        
        map ="""g1g1g1g1g1g1g1g1g1g1
                g1g1g1g1g1g1g1g1g1g1
                g1g1g1g1g1g1g1g1g1g1
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
        self.MaxTurns=50

    def loadObjects(self):

        secret = random.randrange(1,100) 
        levelObjects=[]
        #x,y,direction, imgFile, type, SubType, AI File
        #type: 1=player, 2=base
        # direction: 0=north, 1=west, 2=south, 3=east
        m = maptranslator.MapMaker()
        soln= __name__.replace("level", "soln")
        levelObject=[1,1,3,m.getSurf("dozerblue"),1,0, soln, "player blue"]
        levelObjects.append(levelObject)
        randy = random.randrange(2,8)
        levelObject=[8,randy,0, m.getSurf("dozerred"), 1,1, "playerAIDummy", "opponent1"]
        levelObjects.append(levelObject)
        return levelObjects

class Instructions():
    def __init__(self):
        print("loading instructions")

    def loadInstructions(self):
        strInstr = "Move your dozer to the opponent, \n" 
        strInstr += "then use attack to destroy it: \n"
        strInstr += "self.robot.attack() \n"
        return strInstr

class Validate():
    def __init__(self):
        print("loading validation")

    def validateSoln(self, filename):
        return ""


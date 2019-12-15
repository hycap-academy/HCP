import pygame
import random
import maptranslator

class Map():
    def __init__(self, TILESIZE):
        self.TILESIZE = TILESIZE


    def loadTiles(self):
        
        map ="""wqwhwhwhweg1g1g1g1g1
                wvg1g1g1wvg1g1g1g1g1
                wzwhweg1wvg1g1g1g1g1
                g1g1wvg1wvg1g1g1g1g1
                g1g1wvg1wzwhweg1g1g1
                g1g1wvg1g1g1wvg1g1g1
                g1g1wzweg1wqwcg1g1g1
                g1g1g1wvg1wvg1g1g1g1
                g1g1g1wvg1wvg1g1g1g1
                g1g1g1wzwhwcg1g1g1g1"""



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
        levelObject=[1,1,3,m.getSurf("dozerblue"),1,0, soln, "player blue"]
        levelObjects.append(levelObject)
        levelObject=[5,5,0, m.getSurf("basered"), 2,1, "baseAITellOnly", "base 1", secret]
        levelObjects.append(levelObject)
        levelObject=[4,8,0, m.getSurf("baseblack"), 2,1, "baseAIPrintOnly", "base 2", secret]
        levelObjects.append(levelObject)
        return levelObjects

class Instructions():
    def __init__(self):
        print("loading instructions")

    def loadInstructions(self):
        return "Move your dozer to the red base, \n get the secret code by using\n self.robot.getInfo(),\n then print at the black base \nusing self.robot.print()."

class Validate():
    def __init__(self):
        print("loading validation")

    def validateSoln(self, filename):
        return ""

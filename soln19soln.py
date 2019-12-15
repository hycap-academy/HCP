#  Locate 3
#  GOAL:
#  Your goal is to find the opponent, then attack it.
import inspect
if "rungame" not in inspect.getmodule(inspect.stack()[0])._filesbymodname["__main__"]:
    import rungame

class AI:
    def __init__(self):
        print(__name__ + " AI loaded")

    def turn(self):
         #  Your code goes here.
        #  Make sure that you indent properly
        #  The command you want to use are:  
        #  self.robot.moveForward()
        #  self.robot.turnRight()
        #  self.robot.turnLeft()
        #  Use the following command to find the opponent:
        #  x,y,reldir = self.robot.locateObject("opponent1")
        #  x and y are the coordinates of the opponent
        #  reldir is the relative direction of the opponent:
        #       "front" is mostly in front of the player
        #       "back"  is mostly behind the player
        #       "left"  is mostly left of the player
        #       "right" is mostly right of the player

        #  You can check if there is something in front of you:
        #  objType, name = self.robot.checkObjectForward()
        #  objType will return 1 for player and 2 for base.  It will return 0 if there is nothing.
        #  You can also checkObjectRight() and checkObjectLeft()
        #
        #  Use self.robot.attack() to damage a player in front of you for 5-10 points
        #
        #  Start below the line
        ###__________________________________


        for n in range(100):
            obj = self.robot.checkObjectForward()
            if obj.name=="opponent1":
                self.robot.attack()
            else:

                x,y,reldir = self.robot.locateObject("opponent1")
                if reldir=="front":
                    terrain = self.robot.checkTerrainForward()
                    if terrain=="wall":
                        self.robot.turnLeft()
                    else:
                        self.robot.moveForward()
                if reldir=="left":
                    terrain = self.robot.checkTerrainLeft()
                    if terrain=="wall":
                        self.robot.moveForward()
                    else:
                        self.robot.turnLeft()
                if reldir=="right":
                    terrain = self.robot.checkTerrainRight()
                    if terrain=="wall":
                        self.robot.moveForward()
                    else:
                        self.robot.turnRight()
                if reldir=="back":
                    self.robot.turnRight()
            
#  locate 1
#  GOAL:
#  Your goal is to move the dozer to the base, then use the getInfo() command to get the secret number.
#  Then, you must print the number at the base using self.robot.print()

import inspect
if "rungame" not in inspect.getmodule(inspect.stack()[0])._filesbymodname["__main__"]:
    import rungame

class AI:
    def __init__(self):
        print(__name__ + " AI Loaded")

    def turn(self):
         #  Your code goes here.
        #  Make sure that you indent properly
        #  The command you want to use are:  
        #  self.robot.moveForward()
        #  self.robot.turnRight()
        #  self.robot.turnLeft()
        #  Use the following command to find the opponent:
        #  x,y,reldir = self.robot.locateObject("opponent 1")
        #  x and y are the coordinates of the opponent
        #  reldir is the relative direction of the opponent:
        #       "front" is mostly in front of the player
        #       "back"  is mostly behind the player
        #       "left"  is mostly left of the player
        #       "right" is mostly right of the player

        #  You can check if there is something in front of you:
        #  obj = self.robot.checkObjectForward()
        #  obj.type will return 1 for player and 2 for base.  It will return 0 if there is nothing.
        #  You can also checkObjectRight() and checkObjectLeft()
        #
        #  Use self.robot.attack() to damage a player in front of you for 5-10 points
        #
        #  Start below the line
        ###__________________________________

        for n in range(30):
            x,y,reldir = self.robot.locateObject("base 1")
            if reldir=="front":
                self.robot.moveForward()
            else:
                self.robot.turnLeft()

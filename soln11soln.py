#  GOAL:
#  Your goal is to move the dozer to the red base, then print the word "butterfly"

import inspect
if "rungame" not in inspect.getmodule(inspect.stack()[0])._filesbymodname["__main__"]:
    import rungame

class AI:
    def __init__(self):
        print(__name__ + " AI Loaded")

    def turn(self):
        #  Your code goes here.
        #  Make sure that you indent properly
        #  You can only use the moveForward command once.
        #
        #  You can check if there is something in front of you:
        #  obj = self.robot.checkObjectForward()
        #  obj.type will return 1 for player and 2 for base.  It will return 0 if there is nothing.
        #  You can also checkObjectRight() and checkObjectLeft()
        #
        #  then use the self.robot.print("butterfly") at the base.
        #
        #  Start below the line
        ###__________________________________

        for n in range(25):
            obj = self.robot.checkObjectForward()
            if obj.type==2:
                self.robot.print("butterfly")
            else:
                terrain = self.robot.checkTerrainForward() 
                if terrain == "wall":
                    checkL = self.robot.checkTerrainLeft()
                    if checkL=="grass":
                        self.robot.turnLeft()
                    else:
                        self.robot.turnRight()
                else:
                    self.robot.moveForward()

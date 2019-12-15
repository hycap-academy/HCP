#  if/then 4
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
        #  objType, name = self.robot.checkObjectForward()
        #  objType will return 1 for player and 2 for base.  It will return 0 if there is nothing.
        #  You can also checkObjectRight() and checkObjectLeft()
        
        #  Use the following command to see what is in front of you:
        #  terrain = self.robot.checkTerrainForward()
        #  The terrain may be one of the following:
        #  "road", "wall", "grass"
        #  You will also need to detect the edge
        #  "edge" will be returned if you are at the edge.


        #  then use the self.robot.print("butterfly") at the base.
        #
        #  Start below the line
        ###__________________________________

        for n in range(150):
            obj = self.robot.checkObjectForward()
            if obj.type==2:
                print("base is in front of me!")
                self.robot.print("butterfly")
            else:
                print("There is no base in front of me!")
                if self.robot.checkTerrainForward()=="edge":
                    self.robot.turnRight()
                else:
                    self.robot.moveForward()

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
        #  Use the following command to see what is in front of you:
        #  terrain = self.robot.checkTerrainForward()
        #  The terrain may be one of the following:
        #  "road", "wall", "grass"
        #  You can check if there is a wall in front of you by:
        #  terrain = self.robot.checkTerrainForward()
        #  if terrain == "wall":
        #       <do something>
        #  else:
        #       <do something else>
        #
        #  Start below the line
        ###__________________________________

        for x in range(10):
            terrain = self.robot.checkTerrainForward() 
            if terrain == "wall":
                self.robot.turnRight()
            else:
                self.robot.moveForward()

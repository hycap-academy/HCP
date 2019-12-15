#  GOAL:
#  Your goal is to move the dozer to the base using self.robot.moveForward(), self.robot.turnRight()
#  with 2 for loops. You should not use moveForward more than 2 times. 
#  A for loop looks like this:
#  for x in range(0, 2):  OR  for x in range(2):
#  This will loop 2 times.
import inspect
if "rungame" not in inspect.getmodule(inspect.stack()[0])._filesbymodname["__main__"]:
    import rungame

class AI:
    def __init__(self):
        print(__name__ + " AI Loaded")

    def turn(self):
        #  Your code goes here.
        #  Make sure that you indent properly
        #  Please use 2 for loops and a single  
        #   self.robot.moveForward() and self.robot.moveRight()
        #  command.
        #  Start below the line
        ###__________________________________
        
        self.robot.moveForward()

#  GOAL:
#  Your goal is to move the dozer to the base using self.robot.moveForward(), self.robot.turnRight()
#  and 2 for loops.  A for loop looks like this:
#  for x in range(0, 2):  OR  for x in range(2):
#  This will loop 2 times.

#  Remember to indent everything using a tab that you would like to repeat in the loop.
#  Here is an example of a double for loop printing hello 100 times:
#  for x in range(0,10):
#      for y in range(0,10):
#          print("hello")
#          print(x, y)

#  HINT:
#  For this puzzle, notice that the number of moveForward will have to increase with each iteration.
#  Try something like this:
#  for x in range(1,4):
#      for y in range(0, x):  #counts from 0 to whatever is x is.

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

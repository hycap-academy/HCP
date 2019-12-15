#  GOAL:
#  Your goal is to move the dozer to the base using self.robot.moveForward()
#  and a for loop.  A for loop looks like this:
#  for x in range(0, 2):  OR  for x in range(2):
#  This will loop 2 times.
#  Remember to indent everything using a tab that you would like to repeat in the loop.
#  Here is an example of printing hello 10 times:
#  for x in range(0,10):
#      print("hello")

import inspect
if "rungame" not in inspect.getmodule(inspect.stack()[0])._filesbymodname["__main__"]:
    import rungame

class AI:
    def __init__(self):
        print(__name__ + " AI Loaded")

    def turn(self):
        #  Your code goes here.
        #  Make sure that you indent properly
        #  Please use a for loop and a single  
        #   self.robot.moveForward()
        #  command.
        #  Start below the line
        ###__________________________________


        self.robot.moveForward()

#  attack 2
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
        #
        #  Use self.robot.attack() to damage a player in front of you for 5-10 points
        #
        #  Start below the line
        ###__________________________________


        self.robot.moveForward()

        obj = self.robot.checkObjectForward()
        if obj.type==1:
            self.robot.attack()

            
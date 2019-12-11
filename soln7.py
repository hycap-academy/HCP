#  GOAL:
#  Your goal is to move the dozer to the base, then use the getInfo command to get the secret number.
#  Then, you must print the number at the base using self.robot.print


class AI:
    def __init__(self):
        print("soln6 AI loaded")

    def turn(self):
        #  Your code goes here.
        #  Make sure that you indent properly
        #  The command you want to use is:  
        #  self.robot.moveForward()
        #  Use the following command to get the secret from the base
        #  secret = self.robot.getInfo()
        #  Use the following command to print the secret at the base
        #  self.robot.print(secret)
        #  Start below the line
        ###__________________________________

        #self.robot.moveForward()
        #secret = self.robot.getInfo()
        #self.robot.print(secret)

        self.robot.moveForward()
        self.robot.moveForward()
        self.robot.moveForward()
        secret = self.robot.getInfo()
        self.robot.print(secret)
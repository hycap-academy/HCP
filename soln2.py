#  GOAL:
#  Your goal is to move the dozer to the base using self.robot.moveForward() 
#  self.robot.turnRight(), and self.robot.turnLeft()




class AI:
    def __init__(self):
        print("soln2 AI loaded")

    def turn(self):
       #  Your code goes here.
        #  Make sure that you indent properly
        #  The command you want to use are:  
        #   self.robot.moveForward()
        #   self.robot.turnRight()
        #   self.robot.turnLeft()
        #  Start below the line
        ###__________________________________

        self.robot.moveForward()
        self.robot.turnRight()
        self.robot.turnLeft()
        self.robot.moveForward()
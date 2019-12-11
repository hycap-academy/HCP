
class AI:
    def __init__(self):
        print("soln4 AI loaded")

    def turn(self):
        #  Your code goes here.
        #  Make sure that you indent properly
        #  Please use 2 for loops and a single  
        #   self.robot.moveForward() and self.robot.moveRight()
        #  command.
        #  Start below the line
        ###__________________________________

        self.robot.turnRight()
        for x in range(0,3):
            self.robot.moveForward()
        self.robot.turnLeft()
        for y in range(0,3):
            self.robot.moveForward()
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
        #   self.robot.moveForward()
        #   self.robot.turnRight()
        #   self.robot.turnLeft()
        #  Start below the line
        ###__________________________________

        self.robot.moveForward()
        self.robot.moveForward()
        self.robot.turnRight()
        self.robot.moveForward()
        self.robot.moveForward()
        self.robot.moveForward()
        self.robot.moveForward()
        self.robot.turnLeft()
        self.robot.moveForward()
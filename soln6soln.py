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

        for y in range(1,5):
            for x in range(0,y):
                self.robot.moveForward()
            self.robot.turnRight()
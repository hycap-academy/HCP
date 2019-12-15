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

        for x in range(0,4):
            self.robot.moveForward()

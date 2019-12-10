
class AI:
    def __init__(self):
        print("touchabase AI loaded")

    def turn(self):
        # return states:  nothing=0, 1=objective accomplished, 2=level accomplished
        if self.robot.checkTouch()==True:
            return 2
        else:
            return 0

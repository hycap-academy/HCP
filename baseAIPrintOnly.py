import random

class AI:
    def __init__(self, secret=None):
        print("Tell Secret AI loaded")
        self.secret = secret 
        self.missionStatus = 0

    def turn(self):
        # return states:  nothing=0, 1=objective accomplished, 2=level accomplished
        return self.missionStatus

    def validateSecret(self, strGuess):
        if strGuess==self.secret:
            self.missionStatus=2
        else:
            self.missionStatus=0

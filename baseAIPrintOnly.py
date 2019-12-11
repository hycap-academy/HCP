import random

class AI:
    def __init__(self):
        print("Tell Secret AI loaded")
        self.secret = random.randrange(1,100) 
        self.missionStatus = 0

    def turn(self):
        # return states:  nothing=0, 1=objective accomplished, 2=level accomplished
        return self.missionStatus

    def validateSecret(self, strGuess):
        if strGuess=="butterfly":
            self.missionStatus=2
        else:
            self.missionStatus=0

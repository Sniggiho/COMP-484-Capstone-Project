import random

class DissonanceCalculation:
    def __init__(self):
        pass

    def determineDissonance(self, currentString):
        return random.choice(range(10))

    def determineTotalDissonance(self, tune):
        totalDissonance = 0
        for line in tune:
            totalDissonance += self.determineDissonance(line)
        return totalDissonance
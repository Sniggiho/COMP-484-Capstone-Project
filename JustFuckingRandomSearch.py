# Much of the structure for this code (as well as some of the code itself) comes from Susan Fox's Intro to AI HW 2,
# and from the code written by Issaka Van't Hul, Ana Espeleta, and Christian Lentz for that HW assignment

import RuleSet
import TuneGrader
import random
from Synth import Synth
from matplotlib import pyplot as plt

# verbose = True

class RandomSearcher(object):
    """Contains the hill climbing algorithm and some helper methods."""

    def __init__(self, tuneLength, maxRounds=500):
        """Sets up the starting state"""
        self.maxRounds = maxRounds   # Number of rounds of hillclimbing to perform before stopping
        self.tuneLength = tuneLength
        self.synth = Synth()
        
        self.seeds = []
        self.dissonances = []
        
        self.ruleSetGenerator = RuleSet.RuleSetGenerator(len(startSeed))
        self.dissonanceCalculator = TuneGrader.TuneGrader()

        self.bestIdx = 0
        self.count = 0


    def generateCompleteTune(self, child):
        # uses the attatched ruleset to calculate the automata's generation on a give string
        childsTune = []
        childsTune.append(child)
        for x in range(self.tuneLength-1):
            nextString = self.ruleSetGenerator.step(childsTune[x])
            childsTune.append(nextString)
        return childsTune

    def determineSeedDissonance(self, seed):
        # determines the dissonance of a given child by generation its tune, then running it through dissonanceCalculator
        # return self.dissonanceCalculator.determineTotalDissonance(self.generateCompleteTune(child))
        tune = self.generateCompleteTune(seed)
        # print(tune[:3])

        scaleSteps = self.synth.majorPent
        numOcts = 5  # hardcoded for now
        scale = self.synth.getScale("A1", numOcts, scaleSteps)
        notes = self.synth.interpretData1(tune, scale)
        return self.dissonanceCalculator.determineTotalDissonance(notes)
    
    def run(self):
        while self.count < self.maxRounds:
            self.step()

    def step(self):
        seed = generateRandomSeed(75)

        diss = self.determineSeedDissonance(seed)

        self.seeds.append(seed)
        self.dissonances.append(diss)

        if diss < self.dissonances[self.bestIdx]:
            self.bestIdx = int(self.count)
            print("updated best ind")
        print("round", self.count, "dissonance is", diss)

        self.count += 1



    def generateStatistics(self):
        print("----------------------------- Results -----------------------------------")
        print("Average dissonance across all seeds:", sum(self.dissonances)/len(self.dissonances))
        print("Lowest overall dissonance value:", self.dissonances[self.bestIdx])
        print("Lowest dissonance seed: ", end="")
        for i in self.seeds[self.bestIdx]:
            print(i,end="")
        print()



        # plt.plot(self.dissonances)
        # plt.show()


def generateRandomSeed(length):
    seed = []
    for i in range(0,length):
        seed.append(random.randint(0,1))
    return seed

if __name__ == "__main__":
    startSeed = generateRandomSeed(75)
    
    randomSearcher = RandomSearcher(50, maxRounds = 10000)
    randomSearcher.run()
    randomSearcher.generateStatistics()

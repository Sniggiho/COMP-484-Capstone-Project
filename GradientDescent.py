# Much of the structure for this code (as well as some of the code itself) comes from Susan Fox's Intro to AI HW 2,
# and from the code written by Issaka Van't Hul, Ana Espeleta, and Christian Lentz for that HW assignment

import RuleSet
import TuneGrader
import random
from Synth import Synth

# verbose = True

class HillClimber(object):
    """Contains the hill climbing algorithm and some helper methods."""

    def __init__(self, startSeed, tuneLength, maxRounds=500, maxNeighTries=30):
        """Sets up the starting state"""
        self.startSeed = startSeed
        self.maxRounds = maxRounds   # Number of rounds of hillclimbing to perform before stopping
        self.maxNeighborAttempts = maxNeighTries
        self.minValue = 0   # Minimum possible score
        self.currSeed = startSeed
        self.tuneLength = tuneLength
        self.synth = Synth()
        
        
        self.ruleSetGenerator = RuleSet.RuleSetGenerator(len(startSeed))
        self.dissonanceCalculator = TuneGrader.TuneGrader()

        self.bestSoFarSeed = startSeed
        self.count = 0
        # if verbose:
        #     print("============= START ==============")


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
    
    # def determineDissonanceFromTune(self, tune):
    #     scaleSteps = self.synth.majorPent
    #     numOcts = 5  # hardcoded for now
    #     scale = self.synth.getScale("A1", numOcts, scaleSteps)
    #     notes = self.synth.interpretData1(tune, scale)
    #     return self.dissonanceCalculator.determineTotalDissonance(notes)
    
    def getCurrValue(self):
        """Returns the dissonance of the current seed"""
        return self.determineSeedDissonance(self.currSeed)

    def resetCount(self):
        """Resets the count to zero for the next set of rounds"""
        self.count = 0

    def getCurrSeed(self):
        """Returns the current state."""
        return self.currSeed

    def getBestState(self):
        """Returns the best state ever found"""
        return self.bestSoFarSeed
        

    def run(self):
        """Perform the hill-climbing algorithm, starting with the given start state and going until a local maxima is
        found or the maximum rounds is reached updating the current seed at each iteration."""
        # status = None

        while self.getCurrValue() > self.minValue and self.count < self.maxRounds:
            self.currSeed = self.step() # used to be status instead of self.currSeed

        
        return self.getCurrValue(), self.count

    def step(self):
        """Runs one step of hill-climbing, generates children and picks the best one, returning it as its value.
        Also returns a second value that tells if the best child is optimal or not."""
        self.count += 1

        # use this for hill climbing
        result = self.getBestAllNeighs()
        
        
        return result

    def getBestAllNeighs(self):
        """Looks at all neighbors, and returns the best (or the original state if all neighbors have a worse dissonance)"""
        neighbors = []
        for i in range(len(self.currSeed)):
            neighbor = list(self.currSeed)
            if neighbor[i]:
                neighbor[i]=0
            else:
                neighbor[i]=1
            neighbors.append(neighbor)
        #i=0
        # for char in self.currSeed:
        #     if i == 0:
        #         if char == "1":
        #             newSeed = "0" + self.currSeed[1:]
        #         else:
        #             newSeed = "1" + self.currSeed[1:]
                    
        #     elif i == len(self.currSeed) - 1:
        #         if char == "1":
        #             newSeed = self.currSeed[0:i] + "0"
        #         else:
        #             newSeed = self.currSeed[0:i] + "1"
        #     else:
        #         if char == "1":
        #             newSeed = self.currSeed[0:i] + "0" + self.currSeed[i+1:]
        #         else:
        #             newSeed = self.currSeed[0:i] + "1" + self.currSeed[i+1:]    
        #     neighbors.append(newSeed)
        #     i+=1
        
        bestNeigh = self.findBestNeighbor(neighbors)
        
        if bestNeigh == self.currSeed:
            print("local maximum reached with dissonance:", self.determineSeedDissonance(bestNeigh))
            print(bestNeigh)
            return bestNeigh
        else:
            print("better neighbor found")
            return bestNeigh
    
    def findBestNeighbor(self, neighbors):
        """Given a list of neighbors and values, find and return a neighbor with
        the best value (or the original state if all neighbors have a worse dissonance). If there are multiple neighbors with the same best value,
        the first one found is chosen"""
        bestNeigh = self.currSeed
        bestDissonance = self.determineSeedDissonance(self.currSeed)
        
        for neigh in neighbors:
            dissonance = self.determineSeedDissonance(neigh)
            if dissonance < bestDissonance:
                bestNeigh = neigh
                bestDissonance = dissonance
        
        return bestNeigh

def main():
    startSeed = []
    for i in range(0,75):
        startSeed.append(random.randint(0,1))
    
    hillClimber = HillClimber(startSeed, 50, maxRounds = 15)
    hillClimber.run()
    
if __name__ == "__main__":
    main()

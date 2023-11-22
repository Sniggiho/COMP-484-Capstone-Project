# Much of the structure for this code (as well as some of the code itself) comes from Susan Fox's Intro to AI HW 2,
# and from the code written by Issaka Van't Hul, Ana Espeleta, and Christian Lentz for that HW assignment

import RuleSet
import TuneGrader
import random
from Synth import Synth
from matplotlib import pyplot as plt

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
        
        self.localMinima = []
        self.allDissonanceVals = []
        
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
            self.allDissonanceVals.append(self.determineSeedDissonance(self.currSeed))

        
        return self.getCurrValue(), self.count

    def step(self):
        """Runs one step of hill-climbing, generates children and picks the best one, returning it as its value.
        Also returns a second value that tells if the best child is optimal or not."""
        self.count += 1

        # use this for hill climbing
        result = self.getBestAllNeighsBigSteps()
        
        if result == self.currSeed:
            print("Doing random restart")
            self.localMinima.append(self.currSeed)
            result = generateRandomSeed(len(self.currSeed))
        
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
        
        bestNeigh = self.findBestNeighborNonStop(neighbors)
        
        if bestNeigh == self.currSeed:
            print("local minimum reached with dissonance:", self.determineSeedDissonance(bestNeigh), "Round:", self.count)
            print("The local minimum is:", end="")
            for i in self.currSeed:
                print(i,end="")
            print()
            return bestNeigh
        else:
            print("better neighbor found; round:", self.count)
            return bestNeigh

    def getBestAllNeighsBigSteps(self):
        """Looks at all neighbors, and returns the best (or the original state if all neighbors have a worse dissonance)"""
        neighbors = []
        for i in range(0,len(self.currSeed),3):
            neighbor = list(self.currSeed)
            for j in range(0,3):
                if neighbor[i+j]:
                    neighbor[i+j]=0
                else:
                    neighbor[i+j]=1
            neighbors.append(neighbor)
        
        bestNeigh = self.findBestNeighbor(neighbors)
        
        if bestNeigh == self.currSeed:
            print("local minimum reached with dissonance:", self.determineSeedDissonance(bestNeigh), "Round:", self.count)
            print("The local minimum is:", end="")
            for i in self.currSeed:
                print(i,end="")
            print()
            return bestNeigh
        else:
            print("better neighbor found; round:", self.count)
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

    def findBestNeighborStochastic(self, neighbors):
        """Given a list of neighbors and values, find and return a neighbor with
        the best value. If there are multiple neighbors with the same best value,
        the first one found is chosen. If the best value is equal to the current value,
        a neighbor is selected half the time (allowing the search to continue) and the
        original string is selected half the time (triggering a random restart)"""
        bestNeigh = self.currSeed
        bestDissonance = self.determineSeedDissonance(self.currSeed)
        
        for neigh in neighbors:
            dissonance = self.determineSeedDissonance(neigh)
            if dissonance < bestDissonance:
                bestNeigh = neigh
                bestDissonance = dissonance
            elif dissonance == bestDissonance and random.random() > 0.5:
                bestNeigh = neigh
                print("lateral move selected")
        return bestNeigh

    def findBestNeighborNonStop(self, neighbors):
        """Given a list of neighbors, returns the neighbor with the lowest dissonance"""
        # THIS DOESN'T WORK BECAUSE IT JUST BOUNCES BACK AND FORTH
        dissonances = []
        for neigh in neighbors:
            dissonances.append(self.determineSeedDissonance(neigh))
        
        bestIdx = dissonances.index(min(dissonances))
        print(dissonances[bestIdx])
        return neighbors[bestIdx]
    
    def generateStatistics(self):
        print("----------------------------- Results -----------------------------------")
        print("Number of rounds completed:", self.count)
        print("Number of local minimum discovered:", len(self.localMinima))
        localMinDissonanceVals = []
        for minimum in self.localMinima:
            localMinDissonanceVals.append(self.determineSeedDissonance(minimum))
        
        globalMinIdx = localMinDissonanceVals.index(min(localMinDissonanceVals))
        print("Lowest overall dissonance value:", localMinDissonanceVals[globalMinIdx])
        print("Lowest dissonance seed: ", end="")
        for i in self.localMinima[globalMinIdx]:
            print(i,end="")
        print()

        plt.plot(self.allDissonanceVals)
        plt.show()


def generateRandomSeed(length):
    seed = []
    for i in range(0,length):
        seed.append(random.randint(0,1))
    return seed

if __name__ == "__main__":
    startSeed = generateRandomSeed(75)
    
    hillClimber = HillClimber(startSeed, 50, maxRounds = 500)
    hillClimber.run()
    hillClimber.generateStatistics()

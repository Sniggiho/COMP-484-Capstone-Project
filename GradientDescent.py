# Much of the structure for this code (as well as some of the code itself) comes from Susan Fox's Intro to AI HW 2,
# and from the code written by Issaka Van't Hul, Ana Espeleta, and Christian Lentz for that HW assignment

import RuleSet
import TuneGrader
import random
from Synth import Synth

# verbose = True

class HillClimber(object):
    """Contains the hill climbing algorithm and some helper methods."""

    def __init__(self, startSeed, tuneLength, stringLength, maxRounds=500, maxNeighTries=30):
        """Sets up the starting state"""
        self.startSeed = startSeed
        self.maxRounds = maxRounds   # Number of rounds of hillclimbing to perform before stopping
        self.maxNeighborAttempts = maxNeighTries
        self.minValue = 0   # Minimum possible score
        self.currSeed = startSeed
        self.tuneLength = tuneLength
        self.stringLength = stringLength
        self.synth = Synth()
        
        
        self.ruleSetGenerator = RuleSet.RuleSetGenerator(self.childrenLength)
        self.dissonanceCalculator = TuneGrader.DissonanceCalculation()

        self.bestSoFarSeed = startSeed
        self.count = 0
        # if verbose:
        #     print("============= START ==============")


    def generateCompleteTune(self, child):
        # uses the attatched ruleset to calculate the automata's generation on a give string
        childsTune = [[]]
        childsTune.append(child)
        for x in range(self.tuneLength-1):
            nextString = self.ruleSetGenerator.step(child)
            childsTune.append(nextString)
        return childsTune

    def determineChildDissonance(self, child):
        # determines the dissonance of a given child by generation its tune, then running it through dsc
        # return self.dissonanceCalculator.determineTotalDissonance(self.generateCompleteTune(child))
        childsTune = self.generateCompleteTune(child)

        scaleSteps = self.synth.majorPent
        numOcts = 5  # hardcoded for now
        scale = self.synth.getScale("A1", numOcts, scaleSteps)
        childsNotes = self.synth.interpretData1(childsTune, scale)
        return self.dissonanceCalculator.determineTotalDissonance(childsNotes)



    def getCount(self):
        """Returns the current count."""
        return self.count

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

            # if status == 'optimal' or status == 'local minimum':
            #     break

        # if verbose:
        #     print("============== FINAL STATE ==============")
        #     print(self.currSeed)
        #     print("   Number of steps =", self.count)
        #     if status == 'optimal':
        #         print("  FOUND PERFECT SOLUTION")
        return self.getCurrValue(), self.minValue, self.count

    def step(self):
        """Runs one step of hill-climbing, generates children and picks the best one, returning it as its value.
        Also returns a second value that tells if the best child is optimal or not."""
        self.count += 1
        # if verbose:
        #     print()
        #     print("--------- Count =", self.count, "---------")
        #     print("Current state and score:", self.currSeed, self.getCurrValue())
        #     print() 
        #     print("Best state so far and score", self.bestSoFarSeed, self.bestSoFarSeed.getValue())

        # use this for hill climbing
        result = self.getBestAllNeighs()

        # use this for stochasitc, random-restart hill climbing (doesn't work yet)
        # result = self.stochRandRestartStep() 
        return result

    def getBestAllNeighs(self):
        """Looks at all neighbors, and returns the best (or the original state if all neighbors have a worse dissonance)"""
        neighbors = []
        i=0
        for char in self.currSeed:
            if i == 0:
                if char == "1":
                    newSeed = "0" + self.currSeed[1:]
                else:
                    newSeed = "1" + self.currSeed[1:]
                    
            elif i == len(self.currSeed) - 1:
                if char == "1":
                    newSeed = self.currSeed[0:i] + "0"
                else:
                    newSeed = self.currSeed[0:i] + "1"
            else:
                if char == "1":
                    newSeed = self.currSeed[0:i] + "0" + self.currSeed[i+1:]
                else:
                    newSeed = self.currSeed[0:i] + "1" + self.currSeed[i+1:]    
            neighbors.append(newSeed)
            i+=1
        
        bestNeigh = self.findBestNeighbor(neighbors)
        
        if bestNeigh == self.currSeed:
            print("local maximum reached")
            print(bestNeigh)
            return bestNeigh
        else:
            print("better neighbor found")
            return bestNeigh
    
    def findBestNeighbor(self, neighbors):
        """Given a list of neighbors and values, find and return a neighbor with
        the best value (or the original state if all neighbors have a worse dissonance). If there are multiple neighbors with the same best value,
        the first one found is chosen"""
        bestNeigh = self.currState
        bestDissonance = self.dissonanceCalculator.determineTotalDissonance(self.generateCompleteTune(self.currState))
        
        for neigh in neighbors:
            dissonance = self.dissonanceCalculator.determineTotalDissonance(self.generateCompleteTune(neigh))
            if dissonance < bestDissonance:
                bestNeigh = neigh
                bestDissonance = dissonance
        
        return bestNeigh

    # def stochRandRestartStep(self):
    #     """Performs stochastic hill-climbing with random restart. The algorithm is:
    #         1. Repeat up to self.maxNeighborAttempts times
    #            a. Generate a random neighbor of the current state (self.currState)
    #            b. If the neighbor is better than self.currState, then update self.currState and its
    #            value, and return "keep going" or "optimal", depending on whether the solution is optimal
    #         2. If the loop runs without finding a better neighbor, then use random-restart to generate
    #         a new, completely random starting point for the search."""
    #     neigh_attempts = 0
    #     while neigh_attempts < self.maxNeighborAttempts: 
    #         neigh_attempts+=1
    #         # generate a random neighbor
    #         random_neigh = self.currSeed.randomNeighbors(1)[0] 
    #         random_neigh_val = random_neigh.getValue()
    #         # see if random_neigh is better than the current 
    #         if random_neigh_val > self.currSeed.getValue(): 
    #             # see if random_neigh is the best so far 
    #             if self.bestSoFarSeed.getValue() < random_neigh_val: 
    #                 self.bestSoFarSeed = random_neigh
    #                 self.currSeed = random_neigh
    #                 # return optimal soln if found 
    #                 if random_neigh_val == self.minValue: 
    #                     return "optimal"
    #                 # else, keep searching 
    #                 else: 
    #                     return "keep going" 
    #     # if we hit self.maxNeighborAttempts, return a random restart state 
    #     self.currSeed = self.currSeed.getRandomState() 
    #     return "random restart"

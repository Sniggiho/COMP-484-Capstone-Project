import RuleSet
import TuneGrader
import random
from Synth import Synth
from matplotlib import pyplot as plt

class RockstarGA:
    # run the Genetic Algorithm with set specifications

    def __init__(self, children, totalGenerations, childrenLength, tuneLength, ruleSet):
        # initialization variables
        self.children = children
        self.totalGenerations = totalGenerations
        self.childrenLength = childrenLength
        self.tuneLength = tuneLength
        self.currentGeneration = 0
        self.ruleSet = ruleSet

        self.allBestDissonances =[]
        self.allAvgDissonances= []

        # external calls setup
        self.rsg = RuleSet.RuleSetGenerator(self.childrenLength)
        self.dsc = TuneGrader.TuneGrader()
        self.synth = Synth()

        # datastructures
        self.allGenerations = []

    def generateStartingChildren(self):
        # randomly generates a random set of starting seeds of size equal to childrenLength
        nextGeneration = []
        newChild = []
        for x in range(self.children):
            for y in range(self.childrenLength):
                newChild.append(random.choice(range(2)))
            nextGeneration.append(newChild.copy())
            # print(newChild)
            newChild.clear()
        # print(nextGeneration)
        self.allGenerations.append(nextGeneration)

    def generateCompleteTune(self, child):
        # uses the attatched ruleset to calculate the automata's generation on a give string
        # childsTune = [[], child]
        # for x in range(self.tuneLength - 1):
        #     nextString = self.rsg.step(child)
        #     childsTune.append(nextString)
        # # print(childsTune)
        # return childsTune[1:]
        tune  = []
        tune.append(child)
        for i in range(self.tuneLength-1):
            # nextChord = self.rsg.step(tune[i])
            nextChord = self.rsg.stepSpecific(tune[i],self.ruleSet)
            tune.append(nextChord)
        return tune

    def determineChildDissonance(self, child):
        # determines the dissonance of a given child by generation its tune, then running it through dsc
        childsTune = self.generateCompleteTune(child)

        # print(child)

        scaleSteps = self.synth.majorPent
        numOcts = 5  # hardcoded for now
        scale = self.synth.getScale("A1", numOcts, scaleSteps)

        childsNotes = self.synth.interpretData1(childsTune, scale)

        return self.dsc.determineTotalDissonance(childsNotes)

    def generateRoulette(self, generation):
        # given a generation of children, calculates their dissonance and forms a roulette based set to breed
        breedingSet = []
        workSet = []

        mostDissonance = 0

        leastDissonance = 1000
        secondLeastDissonance = 1000
        leastDissonantChild = 0
        secondLeastDissonantChild = 0
        

        for i in range(len(generation)):
            workSet.append(self.determineChildDissonance(generation[i]))
            if(self.determineChildDissonance(generation[i]) > mostDissonance):
                mostDissonance = self.determineChildDissonance(generation[i])
            if(self.determineChildDissonance(generation[i]) < leastDissonance):
                leastDissonance = self.determineChildDissonance(generation[i])
                leastDissonantChild = i
            elif(self.determineChildDissonance(generation[i]) < secondLeastDissonance):
                secondLeastDissonance = self.determineChildDissonance(generation[i])
                secondLeastDissonantChild = i

        for i in range(len(generation)):
            workSet[i] = mostDissonance - workSet[i]

        totalDissonance = sum(workSet)

        while len(breedingSet) < self.children - 2:
            randomInt = random.randint(0, totalDissonance)
            i = 0
            while randomInt > 0:
                randomInt -= workSet[i]
                i += 1
            breedingSet.append(generation[i - 1])
        
        breedingSet.append(generation[leastDissonantChild])
        breedingSet.append(generation[secondLeastDissonantChild])
        return breedingSet

    def generateNewChildren(self, breedingSet):
        # given a breeding set, generate a new generation of children.
        nextGeneration = []
        i = 0
        halfway = int(len(breedingSet[0]) / 2)
        while len(nextGeneration) != len(breedingSet)-2:
            newString1 = breedingSet[i][: halfway] + breedingSet[i + 1][halfway:]
            newString2 = breedingSet[i + 1][: halfway] + breedingSet[i][halfway:]
            newString1 = self.mutate(newString1)
            newString2 = self.mutate(newString2)
            nextGeneration.append(newString1)
            nextGeneration.append(newString2)
            i+=2
        

        nextGeneration.append(breedingSet[len(breedingSet)-1])
        nextGeneration.append(breedingSet[len(breedingSet)-2])

        return nextGeneration

    def mutate(self, child):
        for i in range(len(child)-1):
            if random.randint(0, 100) < 2:
                if child[i] == 0:
                    child[i] = 1
                else:
                    child[i] = 0
        return child

    def calculateDissapointment(self, generation):
        bestChildDissonance = 1000
        totalGenerationDissonance = 0
        for i in range(len(generation)):
            childDissonance = self.determineChildDissonance(generation[i])
            # print(childDissonance)
            totalGenerationDissonance += childDissonance
            if childDissonance <= bestChildDissonance:
                bestChildDissonance = childDissonance
        print("Best Child Dissonance:"+ str(bestChildDissonance))
        self.allBestDissonances.append(bestChildDissonance)
        print("Generation's average dissonance:"+ str(totalGenerationDissonance/self.children))
        self.allAvgDissonances.append(totalGenerationDissonance/self.children)

    def conclusion(self):
        generation = self.allGenerations[self.currentGeneration]
        
        leastDissonance = 1000
        secondLeastDissonance = 1000
        leastDissonantChild = 0
        secondLeastDissonantChild = 0
        

        for i in range(len(generation)):
            if(self.determineChildDissonance(generation[i]) < leastDissonance):
                leastDissonance = self.determineChildDissonance(generation[i])
                leastDissonantChild = i
            elif(self.determineChildDissonance(generation[i]) < secondLeastDissonance):
                secondLeastDissonance = self.determineChildDissonance(generation[i])
                secondLeastDissonantChild = i
        
        print("Best Child:")
        for i in generation[leastDissonantChild]:
            print(i, end="")

        print("\nSecond Best Child:")
        for i in generation[secondLeastDissonantChild]:
            print(i, end="")

        plt.plot(self.allBestDissonances)
        plt.plot(self.allAvgDissonances)
        plt.show()

            

    def runGenerations(self):
        while self.currentGeneration < self.totalGenerations:
            breedingSet = self.generateRoulette(self.allGenerations[self.currentGeneration])
            self.allGenerations.append(self.generateNewChildren(breedingSet))
            print("Generation " + str(self.currentGeneration) + " done!")
            self.currentGeneration += 1
            self.calculateDissapointment((self.allGenerations[self.currentGeneration]))
        self.conclusion()
        

    def start(self):
        # begins the GA generation
        self.generateStartingChildren()
        self.runGenerations()
        # print(self.allGenerations)
        # print(self.determineChildDissonance(self.allGenerations[0][0]))


def RunGA(children=40, totalGenerations=25, childrenLength=75, tuneLength=50, ruleSet=None):
    if ruleSet is None:
        ruleSet = [0, 1, 1, 1, 0, 0, 0, 1]
    ga = RockstarGA(children, totalGenerations, childrenLength, tuneLength, ruleSet)
    ga.start()


if __name__ == "__main__":
    RunGA()

import RuleSet
import TuneGrader
import random


class RockstarGA:
    # run the Genetic Algorithm with set specifications

    def __init__(self, children, totalGenerations, childrenLength, tuneLength):
        # initialization variables
        self.children = children
        self.totalGenerations = totalGenerations
        self.childrenLength = childrenLength
        self.tuneLength = tuneLength
        self.currentGeneration = 0

        # external calls setup
        self.rsg = RuleSet.RuleSetGenerator(self.childrenLength)
        self.dsc = TuneGrader.TuneGrader()

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
        childsTune = [[], child]
        for x in range(self.tuneLength - 1):
            nextString = self.rsg.step(child)
            childsTune.append(nextString)
        # print(childsTune)
        return childsTune

    def determineChildDissonance(self, child):
        # determines the dissonance of a given child by generation its tune, then running it through dsc
        return self.dsc.determineTotalDissonance(self.generateCompleteTune(child))

    def generateRoulette(self, generation):
        # given a generation of children, calculates their dissonance and forms a roulette based set to breed
        breedingSet = []
        workSet = []

        for i in range(len(generation)):
            workSet.append(self.determineChildDissonance(generation[i]))

        totalDissonance = sum(workSet)
        print("Total Dissonance for generation " + str(self.currentGeneration)+" is " + str(totalDissonance))
        while len(breedingSet) < self.children:
            randomInt = random.randint(0, totalDissonance)
            i = 0
            while randomInt > 0:
                randomInt -= workSet[i]
                i += 1
            breedingSet.append(generation[i - 1])
        return breedingSet

    def generateNewChildren(self, breedingSet):
        # given a breeding set, generate a new generation of children.
        nextGeneration = []
        i = 0
        halfway = int(len(breedingSet[0]) / 2)
        while len(nextGeneration) != len(breedingSet):
            newString1 = breedingSet[i][0: halfway - 1] + breedingSet[i + 1][halfway: len(breedingSet[0] - 1)]
            newString2 = breedingSet[i + 1][0: halfway - 1] + breedingSet[i][halfway: len(breedingSet[0] - 1)]
            newString1 = self.mutate(newString1)
            newString2 = self.mutate(newString2)
            nextGeneration.append(newString1)
            nextGeneration.append(newString2)
            if len(nextGeneration) == len(breedingSet) - 1:
                nextGeneration.append(breedingSet[random.randint(0, len(breedingSet) - 1)])
        return nextGeneration

    def mutate(self, child):
        for i in range(len(child)-1):
            if random.randint(0,100) < 2:
                if child[i] == 0:
                    child[i] = 1
                else:
                    child[i] = 0
        return child

    def runGenerations(self):
        while self.currentGeneration < self.totalGenerations:
            breedingSet = self.generateRoulette(self.allGenerations[self.currentGeneration])
            self.allGenerations.append(self.generateNewChildren(breedingSet))
            print("Generation " + str(self.currentGeneration) + " done!")
            self.currentGeneration += 1

    def start(self):
        # begins the GA generation
        self.generateStartingChildren()
        self.runGenerations()
        print(self.allGenerations)
        # print(self.determineChildDissonance(self.allGenerations[0][0]))


def RunGA(children=20, totalGenerations=50, childrenLength=75, tuneLength=50):
    ga = RockstarGA(children, totalGenerations, childrenLength, tuneLength)
    ga.start()


if __name__ == "__main__":
    RunGA()

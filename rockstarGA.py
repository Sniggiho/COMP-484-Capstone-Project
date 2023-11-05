import RuleSet
import DissonanceCalculator
import random


class RockstarGA:
    # run the Genetic Algorithm with set specifications

    def __init__(self, children, totalGenerations, childrenLength, tuneLength):
        # initialization variables
        self.children = children
        self.totalGenerations = totalGenerations
        self.childrenLength = childrenLength
        self.tuneLength = tuneLength

        # external calls setup
        self.rsg = RuleSet.RuleSetGenerator(self.childrenLength)
        self.dsc = DissonanceCalculator.DissonanceCalculation()

        #datastructures
        self.allGenerations = [[[]]]



    def generateStartingChildren(self):
        # randomly generates a random set of starting seeds of size equal to childrenLength
        nextGeneration = [[]]
        newChild = []
        for x in range(self.children):
            for y in range(self.childrenLength):
                newChild.append(random.choice(range(2)))
            nextGeneration.append(newChild)
            # print(newChild)
            newChild.clear()
        self.allGenerations.append(nextGeneration)

    def generateCompleteTune(self, child):
        # uses the attatched ruleset to calculate the automata's generation on a give string
        childsTune = [[], child]
        for x in range(self.tuneLength-1):
            nextString = self.rsg.step(child)
            childsTune.append(nextString)
        print(childsTune)
        return childsTune

    def determineChildDissonance(self, child):
        # determines the dissonance of a given child by generation its tune, then running it through dsc
        return self.dsc.determineTotalDissonance(self.generateCompleteTune(child))

    def start(self):
        # begins the GA generation
        self.generateStartingChildren()
        print(self.allGenerations)
        # print(self.determineChildDissonance(self.allGenerations[0][0]))


def RunGA(children=20, totalGenerations=50, childrenLength =75, tuneLength=50):
    ga = RockstarGA(children,totalGenerations,childrenLength, tuneLength)
    ga.start()

if __name__ == "__main__":
    RunGA()
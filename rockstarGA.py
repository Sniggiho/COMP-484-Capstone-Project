import RuleSet
import DissonanceCalculator
import random


class RockstarGA:
    # run the Genetic Algorithm with set specifications

    def __init__(self, children, totalGenerations, childrenLength):
        # initialization variables
        self.children = children
        self.totalGenerations = totalGenerations
        self.childrenLength = childrenLength

        # external calls setup
        self.rsg = RuleSet.RuleSetGenerator(self.childrenLength)
        self.dsc = DissonanceCalculator.DissonanceCalculation()

        #datastructures
        self.allGenerations = [[[]]]



    def generateStartingChildren(self):
        #randomly generates a random set of starting seeds of size equal to childrenLength
        nextGeneration = [[]]
        newChild = []
        for x in range(self.children):
            for y in range(self.childrenLength):
                newChild.append(random.choice(range(2)))
            nextGeneration.append(newChild)
            print(newChild)
            newChild.clear()
        self.allGenerations.append(nextGeneration)


    def start(self):
        self.generateStartingChildren()


def RunGA(children=20, totalGenerations=50, childrenLength =75):
    ga = RockstarGA(children,totalGenerations,childrenLength)
    ga.start()

if __name__ == "__main__":
    RunGA()
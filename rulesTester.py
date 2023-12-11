import RuleSet
import TuneGrader
import rockstarGA
import itertools

class RuleTester:
    # run the Genetic Algorithm with set specifications

    def __init__(self, children, totalGenerations, childrenLength, tuneLength, startPoint):
        # initialization variables
        self.children = children
        self.totalGenerations = totalGenerations
        self.childrenLength = childrenLength
        self.tuneLength = tuneLength
        self.startPoint = startPoint

        self.allRuleStrings = self.getAllRules()
        # print(self.allRuleStrings)


    def getAllRules(self):
        allRuleStrings = [[] for _ in range(256)]
        currentHalfway=128
        currentCount=0
        currentSymbol=0
        for j in range(8):
            for i in range(len(allRuleStrings)):
                allRuleStrings[i].append(currentSymbol)
                currentCount+=1
                if(currentCount == currentHalfway):
                    currentCount=0
                    if(currentSymbol == 0):
                        currentSymbol = 1
                    else:
                        currentSymbol = 0
            currentHalfway=currentHalfway/2
            currentCount=0
            currentSymbol=0
        index = allRuleStrings.index(self.startPoint)
        newAllRuleStrings = allRuleStrings[index:]
        
        return newAllRuleStrings

    def start(self):
        for ruleSet in self.allRuleStrings:
            newGA = rockstarGA.RockstarGA(self.children, self.totalGenerations, self.childrenLength, self.tuneLength, ruleSet)
            leastDissonance, secondLeastDissonance, leastDissonantChild, secondLeastDissonantChild = newGA.start()
            print("\nRuleSet: ",ruleSet)
            # print("Least Dissonant: ",leastDissonantChild)
            # print("Dissonance: ",leastDissonance)
            # print("Second Least Dissonant: ",secondLeastDissonantChild)
            # print("Dissonance: ",secondLeastDissonance)

            converted_list = map(str, ruleSet)
            resultRuleSet = ''.join(converted_list)
            converted_list = map(str, leastDissonantChild)
            resultLeastDissonantChild = ''.join(converted_list)
            converted_list = map(str, secondLeastDissonantChild)
            resultSecondLeastDissonantChild = ''.join(converted_list)

            f = open("testfile.txt", "a")
            f.write("\nRuleSet: " + resultRuleSet)
            f.write("\nLeast Dissonant: " + resultLeastDissonantChild)
            f.write("\nDissonance: " + str(leastDissonance))
            f.write("\nSecond Least Dissonant: " + resultSecondLeastDissonantChild)
            f.write("\nDissonance: " + str(secondLeastDissonance))
            f.close()

def runTester(children=40, totalGenerations=1000, childrenLength=75, tuneLength=50, startPoint = [0,0,0,0,0,0,0,0]):
    rt = RuleTester(children, totalGenerations, childrenLength, tuneLength, startPoint)
    rt.start()



if __name__ == "__main__":
    runTester()
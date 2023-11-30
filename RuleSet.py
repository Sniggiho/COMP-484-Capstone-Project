class RuleSetGenerator:
    def __init__(self, xDimension):
        """Initializes the Ruleset Generator"""
        self.numCols = xDimension

    def step(self, currentString):
        """Takes a string of 1s and 0s and generates a new string
        of 1s and 0s using the encoded ruleset."""
        newString = [0] * len(currentString)
        cpyCurrString = list(currentString)
        # print(newString)
        length = len(currentString)
        # print(length)
        cpyCurrString.append(currentString[0])

        for x in range(length):
            # print(x)
            # 0,0,0 = 0
            if(cpyCurrString[x-1] == 0) and (cpyCurrString[x] == 0) and (cpyCurrString[x+1] == 0):
                newString[x] = 0
            # 1,0,0 = 1
            elif(cpyCurrString[x-1] == 1) and (cpyCurrString[x] == 0) and (cpyCurrString[x+1] == 0):
                newString[x] = 1
            # 0,1,0 = 1
            elif (cpyCurrString[x - 1] == 0) and (cpyCurrString[x] == 1) and (cpyCurrString[x + 1] == 0):
                newString[x] = 1
            # 0,0,1 = 1
            elif (cpyCurrString[x - 1] == 0) and (cpyCurrString[x] == 0) and (cpyCurrString[x + 1] == 1):
                newString[x] = 1
            # 0,1,1 = 0
            elif (cpyCurrString[x - 1] == 0) and (cpyCurrString[x] == 1) and (cpyCurrString[x + 1] == 1):
                newString[x] = 0
            # 1,0,1 = 0
            elif (cpyCurrString[x - 1] == 1) and (cpyCurrString[x] == 0) and (cpyCurrString[x + 1] == 1):
                newString[x] = 0
            # 1,1,0 = 0
            elif (cpyCurrString[x - 1] == 1) and (cpyCurrString[x] == 1) and (cpyCurrString[x + 1] == 0):
                newString[x] = 0
            # 1,1,1 = 1
            elif (cpyCurrString[x - 1] == 1) and (cpyCurrString[x] == 1) and (cpyCurrString[x + 1] == 1):
                newString[x] = 1
        return newString

    def stepSpecific(self, currentString, ruleString):
        """Takes a string of 1s and 0s and generates a new string
        of 1s and 0s using the encoded ruleset given the ruleString."""
        newString = [0] * len(currentString)
        cpyCurrString = list(currentString)
        # print(newString)
        length = len(currentString)
        # print(length)
        cpyCurrString.append(currentString[0])

        for x in range(length):
            if (cpyCurrString[x - 1] == 0) and (cpyCurrString[x] == 0) and (cpyCurrString[x + 1] == 0):
                if ruleString[0]==0:
                    newString[x] = 0
                else:
                    newString[x] = 1
                # 1,0,0 = 1
            elif (cpyCurrString[x - 1] == 1) and (cpyCurrString[x] == 0) and (cpyCurrString[x + 1] == 0):
                if (ruleString[1] == 0):
                    newString[x] = 0
                else:
                    newString[x] = 1
                # 0,1,0 = 1
            elif (cpyCurrString[x - 1] == 0) and (cpyCurrString[x] == 1) and (cpyCurrString[x + 1] == 0):
                if (ruleString[2] == 0):
                    newString[x] = 0
                else:
                    newString[x] = 1
                # 0,0,1 = 1
            elif (cpyCurrString[x - 1] == 0) and (cpyCurrString[x] == 0) and (cpyCurrString[x + 1] == 1):
                if (ruleString[3] == 0):
                    newString[x] = 0
                else:
                    newString[x] = 1
                # 0,1,1 = 0
            elif (cpyCurrString[x - 1] == 0) and (cpyCurrString[x] == 1) and (cpyCurrString[x + 1] == 1):
                if (ruleString[4] == 0):
                    newString[x] = 0
                else:
                    newString[x] = 1
                # 1,0,1 = 0
            elif (cpyCurrString[x - 1] == 1) and (cpyCurrString[x] == 0) and (cpyCurrString[x + 1] == 1):
                if (ruleString[5] == 0):
                    newString[x] = 0
                else:
                    newString[x] = 1
                # 1,1,0 = 0
            elif (cpyCurrString[x - 1] == 1) and (cpyCurrString[x] == 1) and (cpyCurrString[x + 1] == 0):
                if (ruleString[6] == 0):
                    newString[x] = 0
                else:
                    newString[x] = 1
                # 1,1,1 = 1
            elif (cpyCurrString[x - 1] == 1) and (cpyCurrString[x] == 1) and (cpyCurrString[x + 1] == 1):
                if (ruleString[7] == 0):
                    newString[x] = 0
                else:
                    newString[x] = 1
            return newString

class RuleSetGenerator:
    def __init__(self, xDimension):
        """Initializes the Ruleset Generator"""
        self.numCols = xDimension

    def step(self, currentString):
        """Takes a string of 1s and 0s and generates a new string
        of 1s and 0s using the encoded ruleset."""
        newString = [0] * len(currentString)
        # print(newString)
        length = len(currentString)
        currentString.append(currentString[0])
        for x in range(length):
            # print(x)
            # 0,0,0 = 0
            if(currentString[x-1] == 0) and (currentString[x] == 0) and (currentString[x+1] == 0):
                newString[x] = 0
            # 1,0,0 = 1
            elif(currentString[x-1] == 1) and (currentString[x] == 0) and (currentString[x+1] == 0):
                newString[x] = 1
            # 0,1,0 = 1
            elif (currentString[x - 1] == 0) and (currentString[x] == 1) and (currentString[x + 1] == 0):
                newString[x] = 1
            # 0,0,1 = 1
            elif (currentString[x - 1] == 0) and (currentString[x] == 0) and (currentString[x + 1] == 1):
                newString[x] = 1
            # 0,1,1 = 0
            elif (currentString[x - 1] == 0) and (currentString[x] == 1) and (currentString[x + 1] == 1):
                newString[x] = 0
            # 1,0,1 = 0
            elif (currentString[x - 1] == 1) and (currentString[x] == 0) and (currentString[x + 1] == 1):
                newString[x] = 0
            # 1,1,0 = 0
            elif (currentString[x - 1] == 1) and (currentString[x] == 1) and (currentString[x + 1] == 0):
                newString[x] = 0
            # 1,1,1 = 1
            elif (currentString[x - 1] == 1) and (currentString[x] == 1) and (currentString[x + 1] == 1):
                newString[x] = 1
        return newString

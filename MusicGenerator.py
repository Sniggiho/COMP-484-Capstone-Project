# A lot of the GUI code -- at least the parts of it that are connected to visual components -- come from Susan Fox's MazePlanner code.

import tkinter as tk
import tkinter.filedialog as tkFileDialog
import RuleSet
from Synth import Synth
from TuneGrader import *


class MusicGeneratorGUI:
    #set up and manage all variables and GUI elements
    
    def __init__(self, xDimension, yDimension):
        """Given the dimensions of the cellular automata game, set up a new Tk object of the right size"""
        self.root = tk.Tk()
        self.root.title("Music Generator")
        self.numRows = yDimension
        self.numCols = xDimension
        self.blockBPM = 0.0

        # declarations for external calls
        self.rsg = RuleSet.RuleSetGenerator(self.numCols)
        self.stepsTaken = 0
        self.allGenerations = [[]]

        # Set up the GUI
        self.setupWidgets()
        
        # Set up synth
        self.synth = Synth()

        # TODO: just for testing purposes
        self.tuneGrader =  TuneGrader()
        
    def setupWidgets(self):
        self._initGrid()
        self._initEditTools()
        
    def _initEditTools(self):
        """Sets up the edit tools frame and its parts, including buttons for clearing the grid, changing
        its numRows/numCols, BPM, and key"""
        self.editEnabled = True
        editFrame = tk.Frame(self.root, bd=7, padx=5, pady=5, relief=tk.GROOVE)
        editFrame.grid(row=3, column=1, rowspan=7, padx=5, pady=5, sticky=tk.N)
        editTitle = tk.Label(editFrame, text="Edit Generator Options", font="Arial 16 bold", anchor=tk.CENTER)
        editTitle.grid(row=0, column=1, padx=5, pady=5)

        # Make a new Grid subframe
        makerFrame = tk.Frame(editFrame, bd=2, relief=tk.GROOVE, padx=5, pady=5)
        makerFrame.grid(row=1, column=1, padx=5, pady=5)
        makerLabel = tk.Label(makerFrame, text="Create New Grid", font="Arial 14 bold", anchor=tk.CENTER)

        BPMLabel = tk.Label(makerFrame, text="BPM")
        rowLabel = tk.Label(makerFrame, text="# of Rows")
        colLabel = tk.Label(makerFrame, text="# of Cols")
        seedLabel = tk.Label(makerFrame, text="input seed")
        self.userBPM = tk.StringVar()
        self.userKey = tk.StringVar()
        self.userRows = tk.StringVar()
        self.userCols = tk.StringVar()
        self.userSeed = tk.StringVar()
        self.userBPM.set(str(60))
        self.userRows.set(str(self.numRows))
        self.userCols.set(str(self.numCols))
        self.userSeed.set(str(0))
        self.BPMEntry = tk.Entry(makerFrame, textvariable=self.userBPM, width=4, justify=tk.CENTER)
        self.rowsEntry = tk.Entry(makerFrame, textvariable=self.userRows, width=4, justify=tk.CENTER)
        self.colsEntry = tk.Entry(makerFrame, textvariable=self.userCols, width=4, justify=tk.CENTER)
        self.seedEntry = tk.Entry(makerFrame, textvariable=self.userSeed, width=16, justify=tk.CENTER)

        

        # place the basic buttons for editing frames
        makerLabel.grid(row=0, column=1, columnspan=4, padx=5)
        BPMLabel.grid(row=1, column=1)
        rowLabel.grid(row=1, column=3)
        colLabel.grid(row=2, column=3)
        seedLabel.grid(row=3, column=1)
        self.BPMEntry.grid(row=2, column=1)
        self.rowsEntry.grid(row=1, column=4)
        self.colsEntry.grid(row=2, column=4)
        self.seedEntry.grid(row=3, column=2)

        # Edit existing maze subframe
        editSubFrame = tk.Frame(editFrame, bd=2, relief=tk.GROOVE, padx=5, pady=5)
        editSubFrame.grid(row=2, column=1, padx=5, pady=5)

        editSubTitle = tk.Label(editSubFrame, text="Choose key", font="Arial 14 bold", anchor=tk.CENTER)
        editSubTitle.grid(row=0, column=1)  # , columnspan=2)
        
        self.keyEntry = tk.Entry(editSubFrame, textvariable=self.userKey, width=4, justify=tk.CENTER)
        self.keyEntry.grid(row=1, column=1)
        
        
        # Variables related to action settings
        self.editChoice = tk.StringVar()
        self.editChoice.set("start")

        # # Create and place the radio buttons for key editing
        # self.AMinor = tk.Radiobutton(editSubFrame, variable=self.editChoice, text="A Major",
        #                                    value="addDelBlock", width=15, justify=tk.LEFT)
        # self.placeStart = tk.Radiobutton(editSubFrame, variable=self.editChoice, text="Move Start",
        #                                  value="start", width=15, justify=tk.LEFT)
        # self.placeGoal = tk.Radiobutton(editSubFrame, variable=self.editChoice, text="Move Goal",
        #                                 value="goal", width=15, justify=tk.LEFT)
        # self.incrWeight = tk.Radiobutton(editSubFrame, variable=self.editChoice, text="Increase Cost",
        #                                  value="increase", width=15, justify=tk.LEFT)
        # self.decrWeight = tk.Radiobutton(editSubFrame, variable=self.editChoice, text="Decrease Cost",
        #                                  value="decrease", width=15, justify=tk.LEFT)
        # self.AMinor.grid(row=1, column=1)
        # self.placeStart.grid(row=3, column=1)
        # self.placeGoal.grid(row=4, column=1)
        # self.incrWeight.grid(row=5, column=1)
        # self.decrWeight.grid(row=6, column=1)

        # Load and save step subframe
        stepFrame = tk.Frame(editFrame, bd=2, relief=tk.GROOVE, padx=5, pady=5)
        stepFrame.grid(row=3, column=1, padx=5, pady=5)
        stepRunTitle = tk.Label(stepFrame, text="step/run", font="Arial 14 bold", anchor=tk.CENTER)
        stepRunTitle.grid(row=0, column=1)  # , columnspan = 2)

        self.stepButton = tk.Button(stepFrame, text="Step", command=self.step)
        self.runButton = tk.Button(stepFrame, text="Run", command=self.run)
        self.stepButton.grid(row=1, column=1, pady=5)
        self.runButton.grid(row=2, column=1, pady=5)
        self.playButton = tk.Button(stepFrame, text="play", command=self.playMusic)
        self.playButton.grid(row=3, column=1, pady=5)


    def _initGrid(self):
        """sets up the grid with given dimensions, done as a helper because it may need to be done over later"""
        self.canvas = None
        self.canvasSize = 500
        self.canvasPadding = 10
        canvasFrame = tk.Frame(self.root, bd=5, padx=10, pady=10, relief=tk.RAISED, bg="lemon chiffon")
        canvasFrame.grid(row=3, column=2, rowspan=2, padx=5, pady=5)
        self.canvas = tk.Canvas(canvasFrame,
                                width=self.canvasSize + self.canvasPadding,
                                height=self.canvasSize + self.canvasPadding)
        self.canvas.grid(row=1, column=1)
       # self.canvas.bind("<Button-1>", self.leftClickCallback)
       # self.canvas.bind("<B1-Motion>", self.motionCallback)

        self._createAutomataGrid()
    
    
    def _createAutomataGrid(self):
        """This sets up the display of the grid."""
        self.idToPos = {}
        self.posToId = {}

        numRows = self.numRows
        numCols = self.numCols
        bigDim = max(numRows, numCols)
        if bigDim * 50 < self.canvasSize:
            self.cellSize = 50
        else:
            self.cellSize = self.canvasSize / bigDim

        for row in range(numRows):
            for col in range(numCols):
                (x1, y1, x2, y2) = self._posToCoords(row, col)
                currId = self.canvas.create_rectangle(x1, y1, x2, y2)
                self.idToPos[currId] = (row, col)
                self.posToId[row, col] = currId
        self._displayGrid()
        
        
    def _setCellColor(self, cellId, color):
        """Sets the grid cell with cellId, and at row and column position, to have the
        right color.  Note that in addition to the visible color, there is also a colors
        matrix that mirrors the displayed colors"""
        self.canvas.itemconfig(cellId, fill=color)
    
    def _setOutlineColor(self, cellId, color):
        """Sets the outline of the grid cell with cellID, and at row and column position, to
        have the right color."""
        self.canvas.itemconfig(cellId, outline=color)
        
    def _displayGrid(self):
        numRows = self.numRows
        numCols = self.numCols
        for row in range(numRows):
            for col in range(numCols):
                currId = self._posToId(row, col)
                (outlineColor, cellColor) = ("green","white")
                self._setOutlineColor(currId, outlineColor)
                self._setCellColor(currId, cellColor)
                
    def _posToId(self, row, col):
        """Given row and column indices, it looks up and returns the GUI id of the cell at that location"""
        return self.posToId[row, col]
        
        
    def _posToCoords(self, row, col):
        """Given a row and column position, this converts that into a position on the frame"""
        x1 = col * self.cellSize + 5
        y1 = row * self.cellSize + 5
        x2 = x1 + (self.cellSize - 2)
        y2 = y1 + (self.cellSize - 2)
        return x1, y1, x2, y2

    def getSeed(self):
        """Converts the current string seed into a list of ints and returns it"""
        currentSeed = []
        print(self.userSeed.get())
        for character in str(self.userSeed.get()):
            currentSeed.append(int(character))
        while (len(currentSeed) < self.numCols):
            currentSeed.append(0)
        return currentSeed

    def updateGrid(self):
        count = 0
        for cell in self.allGenerations[self.stepsTaken]:
            if(cell == 1) and (count < 75):
                self._setCellColor(self._posToId(self.stepsTaken, count), "red2")
            count+=1



    def goProgram(self):
        """This starts the whole GUI going"""
        self.root.mainloop()
# -------------------------------------------------------------------------------------------------------------------------
    #below here are methods for communicating with the other classes and for stepping/running the code

    def step(self):
        print("stepped")
        if(self.stepsTaken < (int(self.numRows) -1)):
            if(self.stepsTaken == 0):
                currentString = self.getSeed()
                self.allGenerations[0] = (currentString)
                self.updateGrid()
            else:
                currentString = self.allGenerations[self.stepsTaken]
            print(currentString)
            self.stepsTaken+=1
            self.allGenerations.append(self.rsg.step(currentString))
            print(self.allGenerations[self.stepsTaken])
            self.updateGrid()

    def run(self):
        print("ran")
        while(self.stepsTaken < (int(self.numRows) -1)):
            self.step()
          
    def getKey(self):
        return self.userKey.get()
      
    def playMusic(self):
        key = self.getKey()
        
        scaleSteps = []
        if "m" in key:
            scaleSteps = self.synth.minorPent
            keyName = key[0:-1]+"1"
        else:
            scaleSteps = self.synth.majorPent
            keyName = key + "1"
        
        numOcts = 5 # hardcoded for now
        
        scale = self.synth.getScale(keyName,numOcts,scaleSteps)
        
        print(scale)
        tune = self.synth.interpretData1(self.allGenerations, scale)
        
        print(tune)
        print("dissonance =", self.tuneGrader.determineTotalDissonance(tune))
               
        
        self.synth.playTune(tune, int(self.userBPM.get()))
        

def RunMusicGenerator(xDimension=75, yDimension = 50):
    """This starts it all up.  Sets up the GUI, and its widgets, and makes it go"""
    s = MusicGeneratorGUI(xDimension, yDimension)
    s.goProgram()


# The lines below cause the program to run 
if __name__ == "__main__":
    RunMusicGenerator()
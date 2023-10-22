from pyo import*

class Synth:

    audioServer = Server() # the audio server this synth will use

    allNoteFreqs = {} # once initialized, this holds note names as keys and their freqeuncies as values.
    # Each entry will look like these examples: {"A4" : 440}, {"D#5" : 622.25},  {"Eb5" : 622.25}
    # NOTE: Enharmonically equivalent notes are given seperate entries with identical values
    # All frequencies are given in equal temperment.

    allNoteNames = [] # once initialized, this holds a list of all note names. 
    # NOTE: the enharmonically equivalent notes are listed as *one* entry with a slash, e.g. "D#5/Eb5"

    # Below are step patterns for some different types of keys and modes
    # They're given as integer number of semitones above the previous frequency, starting at the tonic
    minorPent = [3,2,2,3,2]
    majorPent = [2,2,3,2,3]

    def __init__(self, noteFreqFile = "NoteFreqsCleaned.txt", noteNameFile = "NoteNames.txt"):
        """ Sets up the class allNoteFreqs dictionary and the allNoteNames list, and boots the audio server
        """
        with open(noteFreqFile,'r') as f:
            for line in f:
                tokens = line.split()
                self.allNoteFreqs[tokens[0]] = float(tokens[1])

        with open(noteNameFile,'r') as f:
            for line in f:
                self.allNoteNames.append(line.strip())
        
        self.audioServer.boot()



    def playTune(self,chords,bpm):
        self.audioServer.start()
        for chord in chords:
            self.playNotes(chord, 60/bpm)
        self.audioServer.stop()

    
    def playNotes(self,noteFreqs, duration):
        chord = SuperSaw(noteFreqs).out()
        time.sleep(duration)


    def getNotesForKey(self, lowestTonic, numOctaves, scaleSteps):
        """ 
        Generates a list of all notes in a particular key given a particular tonic and number of octaves
        
        For example getNotesForKey("A4", 2, [3,2,2,3,2]) returns ['A4', 'C5', 'D5', 'E5', 'G5', 'A5', 'C6', 'D6', 'E6', 'G6']

        Param: 
        ------
        lowestTonic : String
            The lowest note (and tonic) to be included in the key. For example "A4", "Eb3", "C#2"

        numOctaves : int
            The number of octaves of the key that should be included

        scaleSteps : List of ints
            A list containing integer number of semitones above the previous frequency, starting at the tonic

        Return:
        -------
            A list of Strings representing the notes in a given key
        """
        startIdx = self.allNoteNames.index(lowestTonic.capitalize().strip())
        currIdx = startIdx
        notesInKey = []

        for oct in range(numOctaves):
            for step in scaleSteps:
                notesInKey.append(self.allNoteNames[currIdx])
                currIdx+=step
        
        return notesInKey
        
    def getFreqsForKey(self, noteNames):
        """ Given a list of note names, returns a list holding the frequncies for each note

        Param:
        ------
        noteNames : list of strings
            The notes for which to retrieve frequencies
        
        Return:
        -------
            List of floats representing note frequencies
        """
        freqs = []

        for n in noteNames:
            freqs.append(self.allNoteFreqs[n])

        return freqs

    def getAllNoteFreqs(self):
        """ Returns internal dictionary between note names and their equal tempered frequency"""
        return self.allNoteFreqs
    
    def stopAudioLoop(self):
        self.audioServer.stop()

if __name__ == "__main__":
    synth = Synth()
    amPent = synth.getFreqsForKey(synth.getNotesForKey("A4",2,synth.minorPent))


    exampleTune = [[amPent[i] for i in [0,1,3]],
                   [amPent[i] for i in [1,3,4]],
                   [amPent[i] for i in [2,5,7]],
                   [amPent[i] for i in [3,4,8]],
                   [amPent[i] for i in [0,1,3]]]
    
    synth.playTune(exampleTune,60)


    # notes = [440, 659.25]

    # while notes[-1] < 1000:
    #     chord = SuperSaw(notes).out()
    #     newNotes = []
    #     for n in notes:
    #         newNotes.append(1.05946*n)
    #     notes = newNotes
    #     time.sleep(1)

    # 


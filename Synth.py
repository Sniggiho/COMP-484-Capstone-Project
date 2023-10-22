from pyo import*

class Synth:

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
        """ Sets up the class allNoteFreqs dictionary and the allNoteNames list
        """
        with open(noteFreqFile,'r') as f:
            for line in f:
                tokens = line.split()
                self.allNoteFreqs[tokens[0]] = float(tokens[1])

        with open(noteNameFile,'r') as f:
            for line in f:
                self.allNoteNames.append(line.strip())
            
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
    

if __name__ == "__main__":
    synth = Synth()
    print(synth.getFreqsForKey(synth.getNotesForKey("A4",1,synth.minorPent)))
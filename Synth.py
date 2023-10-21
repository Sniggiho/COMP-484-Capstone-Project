from pyo import*

class Synth:

    allNoteFreqs = {}

    amPent = ["a", "c", "d", "e", "g"]

    def __init__(self, noteFreqFile = "NoteFreqsCleaned.txt"):
        with open("NoteFreqsCleaned.txt",'r') as f:
            for line in f:
                tokens = line.split()
                self.allNoteFreqs[tokens[0]] = tokens[1]
            

    #TODO: this doesn't work!
    def getFreqsForKey(self, noteNames):
        """ Given a list of note name strings, returns a list of the frequencies corresponding to each of those notes
        """
        freqs = []
        for name in noteNames:
            for key in self.allNoteFreqs.keys():
                print(name, key)
                if name in key:
                    freqs.append(self.allNoteFreqs[key])
        return freqs

    def getAllNoteFreqs(self):
        return self.allNoteFreqs
    

if __name__ == "__main__":
    synth = Synth()
    print(synth.getFreqsForKey(["a", "c", "d", "e", "g"]))
    # s = Server()
    # s.boot()
    # s.start()

    # notes = [440, 659.25]

    # while notes[-1] < 1000:
    #     chord = SuperSaw(notes).out()
    #     newNotes = []
    #     for n in notes:
    #         newNotes.append(1.05946*n)
    #     notes = newNotes
    #     time.sleep(1)

    # s.stop()


class TuneGrader:
    triads = []
    triadFileName = "Triads.txt"

    def __init__(self):
        with open(self.triadFileName,'r') as f:
            for line in f:
                self.triads.append(line.split())

    def determineDissonance(self, chord : list):
        """ Implements an incredibly simple measure of chordal dissonance. Each possible diatonic triad is considered, 
        and for each the number of non-chord tones are tallied. The triad with the smallest number of non-chord tones is
        selected, and the number of non-chord tones is considered the dissonance score of the chord.

        Areas for growth:
            - Weight lowest note more heavily (preference for root position triads)
            - Count 7ths as less dissonant that other extensions (generally considered the case)
            - Weight adjacent dischord more heavily and "spread out" extensions less heavily (they are typically perceived as less "crunchy")

        Param:
        ------
        Chord : list of strings
            The chord to score - a list of note names

        Return:
        -------
        DissonanceScore : int
            Measure of dissonance for the given chord

        """
        editedChord = []
        for note in chord: # remove octave numbering
            editedChord.append(note[:-1])

        lowestDissonance = 1000000 # far higher than we'll ever achieve

        for triad in self.triads: # TODO: this is highly inneficient, can almost half the work being done with a little more careful code should the need arise
            dissonanceScore = 0
            for note in editedChord:
                if not note in triad:
                    dissonanceScore +=1
            if dissonanceScore < lowestDissonance:
                lowestDissonance = dissonanceScore        

        return lowestDissonance

    def determineTotalDissonance(self, tune):
        """ Sums the dissonance across all chords in a tune.

        Param:
        ------
        Tune : list of list of strings
            The tune to score - a list of lists of note names

        Return:
        -------
        DissonanceScore : int
            Measure of dissonance for tune

        """
        totalDissonance = 0
        for chord in tune:
            totalDissonance += self.determineDissonance(chord)
        return totalDissonance
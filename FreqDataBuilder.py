out = open("NoteFreqsCleaned.txt", "w")

with open("NoteFreqs.txt",'r') as f:
    for line in f:
        tokens = line.split()
        cleanedLine = tokens[0] + " " + tokens[1]
        out.write(cleanedLine.strip()+ "\n")
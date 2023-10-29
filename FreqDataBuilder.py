out = open("NoteFreqsCleaned.txt", "w")

with open("NoteFreqs.txt",'r') as f:
    for line in f:
        tokens = line.split()
        # if len(tokens[0].split("/"))>1:
        #     tokens2 = tokens[0].split("/")
        #     cleanedLine = tokens2[0] + " " + tokens[1]
        #     out.write(cleanedLine.strip()+ "\n")
        #     cleanedLine = tokens2[1] + " " + tokens[1]
        #     out.write(cleanedLine.strip()+ "\n")
        # else:
        cleanedLine = tokens[0] + " " + tokens[1]
        out.write(cleanedLine.strip()+ "\n") 

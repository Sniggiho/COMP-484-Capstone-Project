allNoteNames = []

with open("NoteNames.txt",'r') as f:
    for line in f:
        allNoteNames.append(line.strip())

out = open("Triads.txt", "w")

with open("NoteNames.txt",'r') as f:
    for i in range(12):
        maj = allNoteNames[i][:-1] + " " + allNoteNames[i+4][:-1] + " " +allNoteNames[i+7][:-1] + "\n"
        out.write(maj)
        minor = allNoteNames[i][:-1] + " " + allNoteNames[i+3][:-1] + " " +allNoteNames[i+7][:-1] + "\n"
        out.write(minor)

from pyo import*

s = Server()
s.boot()
s.start()

notes = [440, 659.25]

while notes[-1] < 1000:
    chord = SuperSaw(notes).out()
    newNotes = []
    for n in notes:
        newNotes.append(1.05946*n)
    notes = newNotes
    time.sleep(1)

s.stop()
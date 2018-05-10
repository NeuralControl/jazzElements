import pandas as pd
from jazzTheory.jazzTheory.base import Note, Chord, Mode, Scale, Progression

Chord('Co').plot()
Scale('C dorian').plot()


self = Progression('Misty')
self.label()
self.plot(plotScale=True, plotChord=True)


Note('Cb')

Chord('Cm7b5').print()
Chord(['C', 'G', 'Eb']).print()

Chord('Eb').print()
Scale('Eb').print()

Scale('Eb', 'Ionian').chords()

Scale('Eb', 'Ionian').hasChord(Chord('Cm7'))

for ch in Chord('F7').listScales():
    print('{} {:12} {}'.format(ch[0], ch[1], ch[2]))

## print all chords from C scales

key = 'A#'
lst = {}
for mode in Mode.modesLst:
    if mode is not 'Chromatic':
        C = Scale(key, mode).chords()
        lst[key + ' ' + mode] = [str(C[c].root) + C[c].type for c in C]
print(pd.DataFrame(lst, index=Scale.chordsDegrees).T)

Scale('D', 'Ionian').relativeMinor()

Chord('Dm7').guideTones()

Chord('Cm7').avoidNotes(Scale('C', 'Ionian'))

satinDoll = '|Dm7,G7|Dm7,G7|Em7,A7|Em7,A7|Am7,D7|Abm7,Db7|CM7|CM7|'
misty = '|B7b9|EbM7|Bbm7,Eb7|AbM7|Abm7,Db7|EbM7,Cm7|Fm7,Bb7|Gm7,C7|Fm7,Bb7|'

# Plot all chords in a given key
s = Scale('C minor')
s.plotChords()

# Plot Xm7 in all keys
fig = figure(figsize=(12, 5))
grid = gridspec.GridSpec(4, 3, wspace=0.2, hspace=0.2)
for i, n in enumerate(Note.chrSharp):
    ax = fig.add_subplot(grid[i])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    plotNotes(Chord(str(n) + 'm7').notes(), pos=[0, 0, 100, 60], name=str(n) + 'm7')
    axis('off')
suptitle('Xm7 in all keys')

# Plot every implemented chord types in from a given root
root = 'C'
fig = figure(figsize=(12, 5))
grid = gridspec.GridSpec(5, 5, wspace=0.2, hspace=0.2)
for i, n in enumerate(Chord.typesLst):
    ax = fig.add_subplot(grid[i])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    plotNotes(Chord(root + n).notes(), pos=[0, 0, 100, 60], name=root + str(n))
    axis('off')
suptitle('Implemented chord types in ' + root)

self = Progression(misty)
self.label()
self.print()
self.printChords()
self.printScales()

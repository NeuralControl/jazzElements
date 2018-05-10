from jazzTheory.jazzTheory.base import Note, Chord, Mode, Scale, Progression
import pandas as pd

Note('Cb')

Chord('Cm7b5').print()
Chord(['C', 'G', 'Eb']).print()

Chord('Eb').print()
Scale('Eb').print()

Scale('Eb', 'Ionian').chords()

Scale('Eb', 'Ionian').hasChord(Chord('Cm7'))

for ch in Chord('F7').listKeys():
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


## SATIN DOLL
prg = '|Dm7,G7|Dm7,G7|Em7,A7|Em7,A7|Am7,D7|Abm7,Db7|CM7|CM7|'
self = Progression(prg)
self.label()
self.print()

## Misty
prg='|B7b9|EbM7|Bbm7,Eb7|AbM7|Abm7,Db7|EbM7,Cm7|Fm7,Bb7|Gm7,C7|Fm7,Bb7|'
self = Progression(prg)
self.label()
self.print()

Chord('B7b9')






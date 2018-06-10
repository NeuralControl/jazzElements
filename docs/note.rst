.. automodule:: jazzElements.note

Notes
======
Notes are the most basic element, they can be defined as Note('E♯'),Note('Cb'),
and perform simplification (e.g. Note('Gb♭#♯')) or alteration (e.g. Note('C',-2) in semitones).

Applications:

- Note('C')+2 gives D♯
- Note('A')-Note('F#') gives 3
- Note('F##')==Note('Abb') gives True

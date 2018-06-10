.. automodule:: jazzElements.chord

Chords
======
Chords are built on notes, and can be instantiated from a string (e.g. c = Chord('Em7') ) or
from a list of notes strings (e.g. c = Chord(['C','E','G']) ) or Notes

Chords have the following attributes:
    - Chord('Cdim').notes = [C, E♭, G♭] -> The notes in the chord
    - Chord('Cdim').intArr = [0, 3, 6] -> The distances from root in semitones
    - Chord('Cdim').intStr = ['1', '♭3', '♭5'] -> chord intervals
    - Chord('Cdim').quality = 'dim' -> chord quality

and the following members (e.g. C ):
    - Chord('Cm7').guideTones() -> [E♭, B♭]
      Guide Tones are the 3rd and the 7th of a chord. They are the most harmonically important as they
      determine its quality.
    - Chord('C').relativeMinor() -> returns Chord('Am') or 'Am' if asStr=True
    - Chord('Cm').relativeMajor() -> returns Chord('D♯M') or 'D♯M' if asStr=True
    - Chord('Cm7') == Chord('EbM6') -> Returns True as the two chords contain the same notes
    - Chord('Cm').plot() -> plots the chord
    .. image:: img/Cm.png
        :width: 150pt

.. automodule:: jazzElements.chord

Chords
======
Chords are built on notes, and can be instantiated from a string (e.g. c = Chord('Em7') ) or
from a list of notes strings (e.g. c = Chord(['C','E','G']) ) or Notes


Basic attributes
-----------------
.. list-table::
    :header-rows: 1
    :stub-columns: 1

    * -
      - code
      - output
    * - Chord notes
      - Chord('Cdim').notes
      - [C, E♭, G♭]
    * - Distances from root in semitones
      - Chord('Cdim').intArr
      - [0, 3, 6]
    * - Chord intervals
      - Chord('Cdim').intStr
      - ['1', '♭3', '♭5']
    * - Chord quality
      - Chord('Cdim').quality
      - 'dim'


Basic members
-------------
.. list-table::
    :header-rows: 1
    :stub-columns: 1

    * -
      - code
      - output
    * - Guide Tones (3rd,7th)
      - Chord('Cm7').guideTones()
      - [E♭, B♭]
    * -  Relative minor chord
      - Chord('C').relativeMinor()
      - Chord('Am') or 'Am' if asStr=True
    * - Relative major chord
      - Chord('Cm').relativeMajor()
      - Chord('D♯M') or 'D♯M' if asStr=True
    * -  Plot a chord
      - Chord('Cm').plot()
      - .. image:: img/Cm.png
           :width: 150pt
    * -  Chord comparison
      - Chord('Cm7') == Chord('EbM6')
      - True as they have the same notes


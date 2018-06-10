.. automodule:: jazzElements.note

Notes
======
Notes are the most basic element, they can be defined as Note('E♯'),Note('Cb'),
and perform simplification (e.g. Note('Gb♭#♯')) or alteration (e.g. Note('C',-2) in semitones).

Uses
-----

.. list-table::
    :header-rows: 1
    :stub-columns: 1

    * -
      - code
      - output
    * - Transposition
      - Note('C')+2
      - D♯
    * - Note difference
      - Note('A')-Note('F#')
      - 3
    * - Comparison
      - Note('F##')==Note('Abb')
      - True


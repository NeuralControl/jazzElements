Examples
===========

.. WARNING::
    Dev in progress, more coming soon


Scale
------

Printing the chords built from the modes of the C key::

>>> import pandas as pd
>>> key = 'C'
>>> lst = {}
>>> for mode in Scale.modesLst:
>>>     if mode is not 'Chr':
>>>         C = Scale(key, mode).chords()
>>>         lst[key + ' ' + mode] = [str(c.root) + c.type for c in C]
>>> print(pd.DataFrame(lst,index=range(1,len(lst)+1)).T)

Returns:

>>>            1     2     3    4     5     6     7
>>>   C Aeo  Cm7    Dø  D♯M7  Fm7   Gm7  G♯M7   A♯7
>>>   C Dor  Cm7   Dm7  D♯M7   F7   Gm7    Aø  A♯M7
>>>   C Ion  CM7   Dm7   Em7  FM7    G7   Am7    Bø
>>>   C Loc   Cø  C♯M7  D♯m7  Fm7  F♯M7   G♯7  A♯m7
>>>   C Lyd  CM7    D7   Em7  F♯ø   GM7   Am7   Bm7
>>>   C Mix   C7   Dm7    Eø  FM7   Gm7   Am7  A♯M7
>>>   C Phr  Cm7  C♯M7   D♯7  Fm7    Gø  G♯M7  A♯m7

Progressions
------------

Training on major 2-5-1s
^^^^^^^^^^^^^^^^^^^^^^^^
To train on 2-5-1 cadences, one can generate the progression then plot the analysis and the associated keyboards.
We can then use the keyboard view to play the chords (upper keyboard) with the left hand, and the associated scale
(lower keyboard) with the right hand.

>>> # Generating the 4 notes 2-5-1s for every root:
>>> seq=''.join(['|{},{}|{}'.format(
>>>     Scale(key,'ion').getDegree(2,nbNotes=4),
>>>     Scale(key,'ion').getDegree(5,nbNotes=4),
>>>     Scale(key,'ion').getDegree(1,nbNotes=4) ) for key in Note.chrFlat])

>>> prg=Progression(chr,name='Maj 2-5-1s')
>>> prg.annotate()
>>> prg.plot('fn') # Plot the analysis view
>>> prg.plot('kbd') # Plot the keyboard view

.. image:: img/maj251sFn.png
    :width: 500pt

.. image:: img/maj251sKbd.png
    :width: 500pt


Training on minor 2-5-1s
^^^^^^^^^^^^^^^^^^^^^^^^

Likewise, we can train on 4 notes chords in the harmonic minor 2-5-1s

>>> # Generating the 4 notes 2-5-1s for every root:
>>> seq=''.join(['|{},{}|{}'.format(
>>>     Scale(key,'hMin').getDegree(2,nbNotes=4),
>>>     Scale(key,'hMin').getDegree(5,nbNotes=4),
>>>     Scale(key,'hMin').getDegree(1,nbNotes=4) ) for key in Note.chrFlat])

>>> prg=Progression(chr,name='Min 2-5-1s')
>>> prg.annotate()
>>> prg.plot('fn') # Plot the analysis view
>>> prg.plot('kbd') # Plot the keyboard view

.. image:: img/min251sFn.png
    :width: 500pt

.. image:: img/min251sKbd.png
    :width: 500pt

Annotation
----------

Implemented cadence Graphs
^^^^^^^^^^^^^^^^^^^^^^^^^^
Following are examples of detected cadences.
They can be obtained using CadenceGraph().plot()

Kostka transitions (C Major):

.. image:: img/kostkaMaj.png
    :width: 300pt

Kostka transitions (C Harmonic minor):

.. image:: img/kostkaMin.png
    :width: 300pt

Allow all transitions (C Major):

.. image:: img/allTransMaj.png
    :width: 300pt

Allow all transitions (C Harmonic Major):

.. image:: img/allTransMin.png
    :width: 300pt

Only allow main cadences (C Major):

.. image:: img/mainCadMaj.png
    :width: 300pt

Only allow main cadences (C Harmonic minor):

.. image:: img/mainCadMin.png
    :width: 300pt



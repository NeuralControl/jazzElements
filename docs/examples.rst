Examples
===========

Coming soon


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


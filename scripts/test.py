# import warnings
# import pandas as pd
# from jazzElements.chord import Chord
# from jazzElements.note import Note
# from jazzElements.scale import Scale
# from jazzElements.progression import Progression
# from jazzElements.annotate import annGraph

"""
todo: fix bar separation
todo: some cadPos arent right e.g. My romance chord 3
"""
"""
Harmonic Analysis of the chord progression
Args:
    key: force a given key (str)

Following WalkThatBass:
http://www.thejazzpianosite.com/jazz-piano-lessons/jazz-chord-progressions/how-to-analyse-a-chord-progression-harmonic-analysis/

Level 1:
- Find the most represented key
- Annotate chords using this key
Level 2:
- Annotate Function: (PD,D,T)
- Annotate Second Level Chords
    Everything before PD-D-T is a Tonic Prolongation (prolongs the tonic without a cadence)
    They can be Substitutions, or Quick Passing Chords
- Look for non-diatonic chords:
    Long period (>1bar): Modulation
    Short Period (.5-1 bar): Passing Chord | Borrowed Chord | Secondary Dominant

Improvisation:
- first level: We can use the relevant mode under each chord, but we change scale all the time
- or in the second level: We use the functionally important chords
then we can go into crazy stuff i.e. side slipping, cycled patterns, chromatic runs etc...
"""


self=Progression('Misty')
self.annotate(reduce=False)
self.plot('kbd')



ann=annGraph(self.chords)
ann.annotate(reduce=False)
ann.plot()



# todo: Not all chords quality can be resolved:
# for c in Chord.chrLst:
#     print(Chord('C' + c).name + '  ' + Chord('C' + c).quality)

# prg=Progression('My Romance')
# prg.annotate(method='graph',model='majKostka',reduce=False)
#
# self=annGraph(prg.chords)
# self.annotate(reduce=False)
# self.plot()






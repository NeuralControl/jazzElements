# import warnings
# import pandas as pd
# from jazzElements.chord import Chord
# from jazzElements.note import Note
# from jazzElements.scale import Scale
# from jazzElements.progression import Progression
# from jazzElements.annotate import annGraph

"""
todo:
ok - dont color single chords
ok - lighten scales etc
- fix bar separation
- some cadPos arent right e.g. My romance chord 3
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






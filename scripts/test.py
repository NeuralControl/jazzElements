import warnings
import pandas as pd
from jazzElements.chord import Chord
from jazzElements.note import Note
from jazzElements.scale import Scale



for x in Chord.chrFamilies:
    print(x + ' ----------------------')
    for y in Chord.chrFamilies[x]:
        print('   {} {}'.format(y,'-'.join([_ for _ in Chord('C'+y).intStr])))

for d in range(7):
    print(Scale('C min').getFamily(d+1))


    print(Scale('C min').getFamilies())



TODO:
#todo: REPLACE degree by getFamily?
#todo: USE getFamily in progression analysis...

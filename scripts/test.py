import warnings
import pandas as pd
from jazzElements.chord import Chord
from jazzElements.note import Note
from jazzElements.scale import Scale
from jazzElements.progression import Progression
from jazzElements.annotate import annGraph

prg = Progression('My Romance')

for model in ['kostka','allTrans','mainCad']:
    prg.annotate(model=model)
    prg.plot()


from matplotlib.pyplot import *
from jazzElements.progression import Progression,progressions

def plotKnownProgressions(plotType='fn',tgt='d:\\Code\\jazzElements\\img\\'):
    """
        Analyze known progressions and store to disk
    Args:
        plotType: 'fn' | 'kbd'
    """
    for song in progressions:
        for model in ['kostka','wtb']:
            try:
                print('== '+song+' == ('+model+')')
                prg = Progression(song)
                prg.annotate(model=model)
                prg.plot(plotType)
                savefig(tgt + plotType+'\\' + song.replace(' ','')+' '+model)
                close('all')
            except:
                raise ValueError('Error on '+song+' '+model)
                warnings.warn('Error on '+song+' '+model)

plotKnownProgressions('fn')

# plotKnownProgressions('kbd')


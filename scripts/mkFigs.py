from matplotlib.pyplot import *
from jazzElements.progression import Progression,progressions

def plotKnownProgressions(plotType='fn',reduce=False,tgt='d:\\Code\\jazzElements\\img\\'):
    """
        Analyze known progressions and store to disk
    Args:
        plotType: 'fn' | 'kbd'
    """
    for song in progressions:
        for method in ['graph']:
            print('== '+song+' == ('+method+')')
            prg = Progression(song)
            prg.annotate(method=method,reduce=reduce)
            prg.plot(plotType)
            savefig(tgt + plotType+'\\' + song.replace(' ','')+' '+method)
            close('all')

plotKnownProgressions('fn')
plotKnownProgressions('kbd')







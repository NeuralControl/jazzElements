from jazzElements.base import *

def plotKnownProgressions(plotType='fn',tgt='d:\\Code\\jazzElements\\img\\'):
    """
        Analyze known progressions and store to disk
    Args:
        plotType: 'fn' | 'kbd'
    """
    for song in progressions:
        print('== '+song+' ==')
        prg = Progression(song)
        prg.analyze()
        prg.plot(plotType)
        savefig(tgt + plotType+'\\' + song.replace(' ',''))
        close('all')

# plotKnownProgressions('kbd')
# plotKnownProgressions('fn')

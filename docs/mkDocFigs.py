from matplotlib import gridspec
from matplotlib.pyplot import *

from jazzElements.annotate import CadenceGraph
from jazzElements.chord import Chord
from jazzElements.note import Note
from jazzElements.progression import Progression
from jazzElements.scale import Scale
from jazzElements.viz import plotNotes

def mkMisty():
    prg = Progression('Misty')
    prg.annotate()
    prg.plot('fn')
    savefig('./img/MistyFn.png')
    close('all')

    prg = Progression('Misty')
    prg.annotate()
    prg.plot('kbd')
    savefig('./img/MistyKbd.png')
    close('all')


def mkAllChords():
    Scale('C minor').plotChords()
    savefig('./img/allChords.png')
    close('all')


def mkImplementedChords():
    root = 'C'
    fig = figure(figsize=(15, 5))
    nCols = 10
    nRows = int(np.ceil(len(Chord.chrLst) / nCols))
    grid = gridspec.GridSpec(nRows, nCols, wspace=0.4, hspace=0.4)
    for i, n in enumerate(Chord.chrLst):
        ax = fig.add_subplot(grid[i])
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 60)
        plotNotes(Chord(root + n).notes, pos=[0, 0, 100, 60], name=root + str(n), ax=ax)
        axis('off')
    suptitle('Implemented chord types in ' + root)
    savefig('./img/implementedChords.png')
    close('all')


def mkAllKeys():
    fig = figure(figsize=(12, 5))
    grid = gridspec.GridSpec(4, 3, wspace=0.2, hspace=0.2)
    for i, n in enumerate(Note.chrSharp):
        ax = fig.add_subplot(grid[i])
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 60)
        plotNotes(Chord(str(n) + 'm7').notes, pos=[0, 0, 100, 60], name=str(n) + 'm7', ax=ax)
        axis('off')
    suptitle('Xm7 in all keys')
    savefig('./img/allKeys.png')
    close('all')


def mkCadenceGraphs():
    for k in CadenceGraph.cadGraphs:
        CadenceGraph('C', k).plot(tgt='./img/' + k, showChords=True)
    close('all')


def mk251():
    for name, mode in zip(['maj251s', 'min251s'], ['ion', 'hm']):
        seq = ''.join(['|{},{}|{}'.format(
            Scale(key, mode).getDegree(2, nbNotes=4),
            Scale(key, mode).getDegree(5, nbNotes=4),
            Scale(key, mode).getDegree(1, nbNotes=4)) for key in Note.chrFlat])
        prg = Progression(seq, name=name)
        prg.annotate()
        prg.plot('kbd')
        savefig('./img/{}Kbd.png'.format(name))
        prg.plot('fn')
        savefig('./img/{}Fn.png'.format(name))
        close('all')
    close('all')


def plotDocFigs():
    mkMisty()
    mkAllChords()
    mkImplementedChords()
    mkAllKeys()
    mkCadenceGraphs()
    mk251()

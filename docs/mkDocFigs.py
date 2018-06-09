from matplotlib.pyplot import *
from jazzElements.progression import Progression
from jazzElements.scale import Scale
from jazzElements.chord import Chord
from jazzElements.note import Note
from jazzElements.viz import plotNotes
from matplotlib import gridspec
from jazzElements.annotate import CadenceGraph

#todo: automatize mkDocFigs on sphynx build

prg = Progression('My Romance')
prg.annotate(method='graph',model='majKostka', reduce=False)
prg.plot('fn')
savefig('./img/MyRomanceFn.png')
close('all')

prg = Progression('My Romance')
prg.annotate(method='graph',model='majKostka', reduce=False)
prg.plot('kbd')
savefig('./img/MyRomanceKbd.png')
close('all')

Scale('C minor').plotChords()
savefig('./img/allChords.png')
close('all')


root = 'C'
fig = figure(figsize=(15, 5))
nCols = 10
nRows = int(np.ceil(len(Chord.chrLst) / nCols))
grid = gridspec.GridSpec(nRows, nCols, wspace=0.4, hspace=0.4)
for i, n in enumerate(Chord.chrLst):
    ax = fig.add_subplot(grid[i])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    plotNotes(Chord(root + n).notes, pos=[0, 0, 100, 60], name=root + str(n),ax=ax)
    axis('off')
suptitle('Implemented chord types in ' + root)
savefig('./img/implementedChords.png')
close('all')

fig = figure(figsize=(12, 5))
grid = gridspec.GridSpec(4, 3, wspace=0.2, hspace=0.2)
for i, n in enumerate(Note.chrSharp):
    ax = fig.add_subplot(grid[i])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    plotNotes(Chord(str(n) + 'm7').notes, pos=[0, 0, 100, 60], name=str(n) + 'm7',ax=ax)
    axis('off')
suptitle('Xm7 in all keys');
savefig('./img/allKeys.png')
close('all')


CadenceGraph('C').plot(tgt='./img/majKostka', showChords=True)
CadenceGraph('C','minKostka').plot(tgt='./img/minKostka', showChords=True)


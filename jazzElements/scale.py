import re

import numpy as np
from matplotlib import gridspec
from matplotlib.pyplot import figure, axis, suptitle

from jazzElements.chord import Chord
from jazzElements.note import Note
from jazzElements.viz import plotNotes


class Scale():
    modesLst = ['Ion', 'Dor', 'Phr', 'Lyd', 'Mix', 'Aeo', 'Loc']
    modesIntervals = {
        'Ion': [2, 2, 1, 2, 2, 2, 1],
        'Dor': [2, 1, 2, 2, 2, 1, 2],
        'Phr': [1, 2, 2, 2, 1, 2, 2],
        'Lyd': [2, 2, 2, 1, 2, 2, 1],
        'Mix': [2, 2, 1, 2, 2, 1, 2],
        'Aeo': [2, 1, 2, 2, 1, 2, 2],
        'Loc': [1, 2, 2, 1, 2, 2, 2],
        'Chr': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'Hmin': [2, 1, 2, 2, 1, 3, 1], # Harmonic Minor
        'Mmin+': [2, 1, 2, 2, 2, 2, 1], # melodic Minor up
        'Mmin-': [2, 1, 2, 2, 1, 2, 2], # melodic Minor down
    }
    chrDegLst = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
    chrSubLst = \
        [  # List of chord substitutions,  Format ['<old>-><new>','name']
            ['IM7->iiim7', '3sub1'],  # I -> iii common on I-vi-ii-V
            ['im7->IIIM7', '3sub1'],

            ['IM7->vim7', '6sub1'],
            ['im7->VIM7', '6sub1'],

            ['V7->iim7,V7', '2-5sub5'],
            ['V7->II7,V7', '2-5sub5'],

            ['V7->iiim7,VI7,iim7,V7', '3-6-2-5sub5'],
            ['V7->III7,VI7,II7,V7', '3-6-2-5sub5'],

            ['V7->#Vdim7', '#5sub5'],
            ['V7->bii7', 'trisub5'],
        ]
    """
        - Tritone substitution: we can replace a dom7 by a dom7 that is 6halfSteps above the root   
        - Tritone substitution is good on II-V-I because it provides a chromatic root movement   
          e.g. Dm7–G7–CM7 -> Dm7–D♭7–CM gives a downward walking bass   
    """

    regexRoman = re.compile(r"([#b♭♯]*)([iIvV]+)(.*)")  # Regular expression to understand Roman Notation

    def __init__(self, root='C', mode='Ion'):
        if isinstance(root, Note):
            root = root.name
        if ' ' in root:
            root, mode = root.split(' ')
        # todo: be able to instanciate Scale('Cmin') or Scale('C#maj')

        mode = mode[0].upper() + mode[1:].lower()

        if mode in ['Major', 'Maj']: mode = 'Ion'
        if mode in ['Minor', 'Min', 'Nmin']: mode = 'Aeo'
        if mode not in self.modesIntervals: raise ValueError('mode {} not implemented'.format(mode))

        self.root = Note(root)
        self.mode = mode
        self.name = self.root.name + ' ' + self.mode

    def __str__(self):
        return '{} {:4} | {}'.format(str(self.root), str(self.mode), ' '.join([str(n) for n in self.notes()]))

    def __repr__(self):
        return self.__str__()

    def __add__(self, steps):
        return Scale(self.root + steps, self.mode)

    def __sub__(self, steps):
        return Scale(self.root - steps, self.mode)

    def __eq__(self, scale):
        x = scale.notes()
        y = self.notes()
        return all([xi in y for xi in x]) and all([yi in x for yi in y])

    def intervals(self, asStr=False):
        stepsNames = {2: 'w', 1: 'h'}
        if asStr:
            return '-'.join([stepsNames[s] for s in self.modesIntervals[self.mode]])
        else:
            return self.modesIntervals[self.mode]

    def plot(self, ax=0, pos=None, nbOctaves=2, showName=True):
        if pos is None:
            pos = [0, 0, 200, 40]
        plotNotes(self.notes(), pos=pos, ax=ax, nbOctaves=nbOctaves,
                  name=showName * (self.root.name + ' ' + self.mode))

    def plotChords(self, nbNotes=4):
        fig = figure(figsize=(7, 4))
        grid = gridspec.GridSpec(4, 2, wspace=0.2, hspace=0.2)
        i = 0
        for c, d in zip(self.chords(), self.chordsRoman(nbNotes=nbNotes)):
            ax = fig.add_subplot(grid[i])
            ax.set_xlim(0, 100)
            ax.set_ylim(0, 60)
            plotNotes(c.notes, pos=[0, 0, 100, 60], name=c.name + '  ' + d, ax=ax)
            axis('off')
            i += 1
        suptitle('Chords built from ' + self.root.name + ' ' + self.mode);

    def parallelModes(self, asStr=False):
        """
        Parallel modes are the modes built from the same tonic
        Returns:
            list of parallel modes
        """
        if asStr:
            return [m for m in self.modesLst if m != self.mode]
        else:
            return [Scale(self.root, m) for m in self.modesLst if m != self.mode]

    def relativeModes(self, asStr=False):
        """
        Relative modes are the scales with the same key signature
        Returns:
            list of relative modes
        """
        modesLst = self.modesLst.index(self.mode)
        if asStr:
            return [n + ' ' + m for n, m in
                    zip(Scale(self.root, self.mode).notes(asStr=True), np.roll(self.modesLst, -modesLst)) if
                    m != self.mode]
        else:
            return [Scale(n + ' ' + m) for n, m in
                    zip(Scale(self.root, self.mode).notes(asStr=True), np.roll(self.modesLst, -modesLst))
                    if m != self.mode]

    def relativeMinor(self, asStr=False):
        if self.mode == 'Ion':  # Relative Major is 1.5 tone below key
            return Scale(Note(self.root) - 3, 'Aeo').name if asStr else Scale(Note(self.root) - 3, 'Aeo')
        else:
            raise ValueError('Cannot calculate relative Minor')

    def relativeMajor(self, asStr=False):
        if self.mode == 'Aeo':  # Relative Minor is 1.5 tone above key
            return Scale(Note(self.root) + 3, 'Ion').name if asStr else Scale(Note(self.root) + 3, 'Ion')
        else:
            raise ValueError('Cannot calculate relative Major')

    def parallelMinor(self, asStr=False):
        if self.mode == 'Ion':
            return Scale(Note(self.root), 'Aeo').name if asStr else Scale(Note(self.root), 'Aeo')
        else:
            raise ValueError('Cannot calculate parallel Minor')

    def chordFromRoman(self, item, asStr=False):
        alt, deg, chrType = re.search(self.regexRoman, item).groups()
        chr = Chord(self.notes(asStr=True)[self.chrDegLst.index(deg.upper())] + alt + chrType)
        return chr.name if asStr else chr

    def possibleSubstitutions(self, asStr=False):
        S = []
        for s in self.chrSubLst:
            From, To = s[0].split('->')
            From = [self.chordFromRoman(c, asStr=asStr) for c in From.split(',')]
            To = [self.chordFromRoman(c, asStr=asStr) for c in To.split(',')]
            S.append([From, To, s[1]])
        return S

    def getDegree(self, d, nbNotes=4, asStr=False):
        if isinstance(d, str):
            d = self.chrDegLst.index(d) + 1
        return self.chords(nbNotes=nbNotes)[d - 1].name if asStr else self.chords(nbNotes=nbNotes)[d - 1]

    def getDegreeFamily(self,d,asStr=False):
        if asStr:
            return [Chord(self.chords()[d-1].root.name+chrType).name for chrType in Chord.chrFamilies[self.degreesQuality(4)[d-1]]]
        else:
            return [Chord(self.chords()[d-1].root.name+chrType) for chrType in Chord.chrFamilies[self.degreesQuality(4)[d-1]]]


    def degreesQuality(self, nbNotes=4):
        return [chr.quality for chr in self.chords(nbNotes)]

    def degrees(self):
        return \
            [
                (self.chrDegLst[d].lower() if q in ['min', 'dim'] else self.chrDegLst[d].upper())
                + ('o' if q == 'dim' else '')
                for d, q in enumerate(self.degreesQuality())
            ]


    def notes(self, asStr=False):
        if asStr:
            return [str(self.root + i) for i in np.insert(np.cumsum(self.intervals()[:-1]), 0, 0)]
        else:
            return [self.root + i for i in np.insert(np.cumsum(self.intervals()[:-1]), 0, 0)]

    def chords(self, nbNotes=4, asStr=False):
        N = self.notes() * 3
        C = [Chord([N[n + 2 * i] for i in range(nbNotes)], checkInv=False) for n in range(len(self.notes()))]

        if asStr:
            return [c.name for c in C]
        return C

    def chordsRoman(self, nbNotes=4):
        return [(self.chrDegLst[d].lower() + c.type
                 if 3 in c.intArr else self.chrDegLst[d] + c.type).strip()
                for d, c in enumerate(self.chords(nbNotes=nbNotes, asStr=False))]

    def hasChord(self, chord):
        """
        Checks if a given chord can be built from a scale
        Args:
            chord: Chord name or Chord instance

        Returns:
            boolean
        """
        if isinstance(chord, str): chord = Chord(chord)
        if chord.notes == []: return False

        if all([n in self.notes() for n in chord.notes]):
            if chord in self.chords(nbNotes=len(chord.notes)):
                return self.chordsRoman(nbNotes=len(chord.notes))[
                    self.chords(nbNotes=len(chord.notes)).index(chord)]
            else:
                print('Found {} in {} but cannot calculate it'.format(chord.name, self.name))

        return False

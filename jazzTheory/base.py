"""
"""
from itertools import permutations
from matplotlib import gridspec
from matplotlib.patches import FancyBboxPatch
from matplotlib.pyplot import *

def printNotes(notes, fmt='shade'):
    if isinstance(notes[0], str):
        notes = [Note(n) for n in notes]
    if fmt == 'square':
        b, w, spc = [u"\u25A1", u"\u25A0", u"\u2005"]
    elif fmt == 'shade':
        b, w, spc = [u"\u2591", u"\u2588", u"\u2005"]
    else:
        b, w, spc = [u"\u2591", u"\u2588", u"\u2005"]

    N = [b] * 12
    for ni, n in enumerate(Scale('C', 'Chromatic').notes()):
        if n in notes: N[ni] = w

    print(3 * spc + N[1] + 2 * spc + N[3] + 9 * spc + N[6] + 2 * spc + N[8] + 2 * spc + N[10] + 7 * spc +
          3 * spc + N[1] + 2 * spc + N[3] + 9 * spc + N[6] + 2 * spc + N[8] + 2 * spc + N[10] + '\n' +
          N[0] + 2 * spc + N[2] + 2 * spc + N[4] + 4 * spc + N[5] + 2 * spc + N[7] + 2 * spc + N[9] + 2 * spc + N[
              11] + 3 * spc +
          N[0] + 2 * spc + N[2] + 2 * spc + N[4] + 4 * spc + N[5] + 2 * spc + N[7] + 2 * spc + N[9] + 2 * spc + N[
              11])

def plotNotes(notes, pos=[0, 0, 100, 40], cNote='#63B4D1', name='', ax=0, nbOctaves=1):
    def plotKey(ax, x, y, w, h, faceColor='w', edgeColor='k', pad=2, z=0):
        ax.add_patch(FancyBboxPatch((x + pad, y + pad),
                                    abs(w) - 2 * pad, abs(h) - 2 * pad,
                                    boxstyle="round,pad=" + str(pad),
                                    fc=faceColor, ec=edgeColor, zorder=z, lw=2))

    nb = int(np.ceil(len(notes) / (nbOctaves * 12)) * (nbOctaves * 12))
    start = 'C' if notes[0] - Note('C') < notes[0] - Note('F') else 'F'
    chromatic = Note.chrSharp * 4
    chromatic = chromatic[chromatic.index(Note(start)):]
    chromatic = chromatic[:nb]
    whites = [n for n in chromatic if n in Scale('C major').notes()]
    whiteWidth = pos[2] / len(whites)
    blackWidth = whiteWidth / 2

    if ax == 0:
        figure(figsize=(3, 1))
        ax = gca()
    axis('off')

    nWhites = 0
    for i, n in enumerate(chromatic):
        if n in whites:
            plotKey(ax, pos[0] + (nWhites) * whiteWidth, pos[1], whiteWidth, pos[3],
                    pad=2 * whiteWidth / nb, faceColor=cNote if n in notes else 'w', z=0)

            nWhites += 1
        else:
            plotKey(ax, pos[0] + (nWhites) * whiteWidth - blackWidth / 2, pos[1] + pos[3] / 3, blackWidth,
                    2 * pos[3] / 3,
                    pad=2 * blackWidth / nb, faceColor=cNote if n in notes else 'k', z=1)
    plot(0, 0, '.w', zorder=-1)
    if name:
        text(pos[0], pos[1] + pos[3] / 2, name, ha='right', va='center', rotation=90)

progressions = \
    {
        'SatinDoll': '|Dm7,G7|%|Em7,A7|%|Am7,D7|Abm7,Db7|CM7|%|',
        'Misty': '|B7b9|EbM7|Bbm7,Eb7|AbM7|Abm7,Db7|EbM7,Cm7|Fm7,Bb7|Gm7,C7|Fm7,Bb7|',
    }

class Note:
    """
    Create a new note with format verification and simplification
    Args:
        note: note string format (can use unicode b,♭,#,♯ )
        alt: additional alteration
    Examples:
        n=Note('Db')
        n=Note('D♭')
        n=Note('D♭♭♭♭♭♭♭')
        n=Note('D♭',+3)
    """

    chrSharp = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B']
    chrFlat = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']

    sharp = '#'
    Sharp = u"\u266f"
    flat = 'b'
    Flat = u"\u266d"
    natural = 'n'
    Natural = u"\u266e"
    altLst = {sharp: 1, Sharp: 1, flat: -1, Flat: -1, natural: 0, Natural: 0, '?': 0}

    def __init__(self, note, alt=0):
        if isinstance(note, Note):
            self.name = note.name
        else:
            if note[0].upper() in self.chrSharp:
                self.name = note[0].upper()
            else:
                raise ValueError('Note unknown')

            for alti in note[1:]:
                if alti in self.altLst:
                    alt += self.altLst[alti]
                else:
                    raise ValueError('Alteration unknown')
        alt = alt % 12 if alt > 0 else alt
        if alt == 0:
            return
        elif alt < 0:
            chrScale = self.chrFlat[::-1] * 2 + self.chrSharp[::-1] * 2
        else:
            chrScale = self.chrSharp * 2 + self.chrFlat * 2

        self.name = chrScale[(chrScale.index(self.name)) + abs(alt) % 12]

    def __str__(self):
        return self.name

    def __add__(self, alt):
        """
        Adds alt half steps to a given note
        Args:
            alt: number of half steps to add
        Returns:
            Altered Note
        Examples:
            Note('C')+2 returns Note('D')
        """
        return Note(self, alt)

    def __sub__(self, altOrNote):
        """
        Returns the steps from another note, OR transpose down alt halfSteps

        Args:
            altOrNote: <int>: number of halfSteps to substract
                       <Note>:  the note to compare to

        Returns:
            number of halfSteps or altered Note

        Examples:
            Note('D')-Note('C') returns 2
            Note('D')-2 returns Note('C')
        """

        if isinstance(altOrNote, Note):
            n1 = ((self.chrFlat + self.chrSharp).index(self.name)) % 12
            n2 = ((self.chrFlat + self.chrSharp).index(altOrNote.name)) % 12
            return n1 - n2 if n1 - n2 >= 0 else 12 + n1 - n2
        else:
            return Note(self, -altOrNote)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, note):
        """
        Tests if self is equivalent to another Note
        Args:
            note: Note to compare to
        Returns:
            bool
        """
        if isinstance(note, str):
            note = Note(note)
        return (self - note) == 0

class Chord:
    """

    """
    # todo: for a minor chord, the 3 should be b, no #
    # todo: implement + and -

    intervalsLst = ['1', 'b2', '2', 'b3', '3', '4', 'b5', '5', '#5', '6', 'b7', '7', '8',
                    'b9', '9', '#9', '10', '11', '#11', '12', '#12', '13', 'b14', '14', '15']
    typesLst = {
        # Major
        '': '1-3-5',
        'M6': '1-3-5-6',
        'M7': '1-3-5-7',
        'M9': '1-3-5-7-9',
        # Minor
        'm': '1-b3-5',
        'm6': '1-b3-5-6',
        'm7': '1-b3-5-b7',
        'm9': '1-b3-5-b7-9',
        'm7b5': '1-b3-b5-b7',
        # Dominant
        '7': '1-3-5-b7',
        '9': '1-3-5-b7-9',
        '7b9': '1-3-5-b7-b9',
        '11': '1-3-5-b7-9-11',
        '13': '1-3-5-b7-9-11-13',
        # diminished
        'o': '1-b3-b5',
        'o7': '1-b3-b5-6',  # bb7->6
        u'\u00F8': '1-b3-b5-b7',
        # augmented
        'aug': '1-3-#5',
        # sus
        'sus4': '1-4-5',
        'sus2': '1-2-5',
        '7sus4': '1-4-5-b7',
        '7sus2': '1-2-5-b7'
    }

    def __init__(self, nameOrNotes, checkInv=True):
        """
        Create a chord from chord name or list of notes
        Args:
            nameOrNotes: chord names or notes within chord
        Examples:
            c=Chord('Em7')
            c=Chord(['C','E','G'])
        """
        if isinstance(nameOrNotes, str):
            self.type = ''
            if len(nameOrNotes) == 1:
                self.root = Note(nameOrNotes)
            elif nameOrNotes[1] in Note.altLst:
                self.root = Note(nameOrNotes[:2])
                if len(nameOrNotes) > 2:
                    self.type = nameOrNotes[2:]
            else:
                self.root = Note(nameOrNotes[0])
                self.type = nameOrNotes[1:]

        elif isinstance(nameOrNotes, Chord):
            self.root = nameOrNotes.root
            self.type = nameOrNotes.type
        else:
            nameOrNotes = [str(n) for n in nameOrNotes]
            chrdType = []
            if checkInv:
                seq = list(permutations(nameOrNotes, len(nameOrNotes)))
            else:
                seq = [nameOrNotes]
            for lst in seq:
                intervals = [n if n >= 0 else n + 12 for n in [Note(n) - Note(lst[0]) for n in lst]]
                intervals = '-'.join([Chord.intervalsLst[i] for i in intervals])
                chrdType.extend([lst[0] + k for k, v in self.typesLst.items() if v == intervals])

            if len(chrdType) == 0:
                raise ValueError('Cannot find a chord from ' + ','.join(nameOrNotes))

            if len(chrdType) > 1:
                chrdType.sort(key=len)  # todo: Best match shouldnt be done this way
                #print('Found {} choosing {}'.format(','.join(chrdType), chrdType[0]))

            self.root = Chord(chrdType[0]).root
            self.type = Chord(chrdType[0]).type

        self.name = str(self.root) + self.type

    def intervals(self, asStr=False):
        """
        Return intervals of the chord
        Args:
            asStr: if True, returns as strings list, otherwise as list of steps
        """
        if asStr:
            return self.typesLst[self.type].split('-')
        else:
            return [self.intervalsLst.index(i) for i in self.typesLst[self.type].split('-')]

    def print(self, set='shade'):
        print(self.__str__())
        printNotes(self.notes(), fmt=set)

    def plot(self,ax=0,pos=[0, 0, 100, 40],nbOctaves=1,showName=True):
        plotNotes(self.notes(), ax=ax,pos=pos,nbOctaves=nbOctaves,name=showName*self.name)

    def notes(self, asStr=False):
        I = [i - 12 * ('b' in iName) for i, iName in zip(self.intervals(), self.intervals(asStr=True))]
        # hack to keep flat intervals flat
        if asStr:
            return [str(Note(self.root) + i) for i in I]
        else:
            return [Note(self.root) + i for i in I]

    def guideTones(self, asStr=False):
        """
        Guide Tones are the 3rd and the 7th of a chord. They are the most harmonically important as they
        determine its quality, so we want to focus on them.
        Args:
            asStr: return a string list

        Returns:
            list of guide tones
        """
        guideTonesLst = ['b3', '3', 'b7', '7']
        guideTones = [gt for i, gt in zip(self.intervals(asStr=True), self.notes()) if i in guideTonesLst]
        return [str(gt) for gt in guideTones] if asStr else guideTones

    def avoidNotes(self, notesOrScale, asStr=False):
        """
        Avoid notes are notes one step above a chord note, use sparingly and while passing
        """
        if isinstance(notesOrScale, Scale):
            notesOrScale = notesOrScale.notes()
        if isinstance(notesOrScale,str):
            if ' ' in notesOrScale:
                notesOrScale = Scale(notesOrScale).notes()

        avoid = [n + 1 for n in self.notes()]
        avoidNotes = [an for an in notesOrScale if an in avoid]
        return [str(gt) for gt in avoidNotes] if asStr else avoidNotes

    def __str__(self):
        return '{}{} {} | {}'.format(self.root.name, self.type,
                                     '-'.join(self.intervals(asStr=True)),
                                     ' '.join([str(n) for n in self.notes()]))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, chordOrStr):
        x = Chord(chordOrStr).notes()
        y = self.notes()
        return all([xi in y for xi in x]) and all([yi in x for yi in y])

    def listScales(self):
        """
        Lists the keys on which we have this chord
        """
        lst = []
        for key in Scale('C', 'Chromatic').notes():
            for mode in Mode.modesLst:
                chr = Scale(key, mode).hasChord(self)
                if len(chr):
                    for c in chr:
                        lst.append([key, mode, c])
        return lst

class Mode:
    modesLst = ['Ionian', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Aeolian', 'Locrian', 'Chromatic']
    modesIntervals = {
        'Ionian': [2, 2, 1, 2, 2, 2, 1],
        'Dorian': [2, 1, 2, 2, 2, 1, 2],
        'Phrygian': [1, 2, 2, 2, 1, 2, 2],
        'Lydian': [2, 2, 2, 1, 2, 2, 1],
        'Mixolydian': [2, 2, 1, 2, 2, 1, 2],
        'Aeolian': [2, 1, 2, 2, 1, 2, 2],
        'Locrian': [1, 2, 2, 1, 2, 2, 2],
        'Chromatic': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }

    def __init__(self, mode):
        if isinstance(mode, Mode):
            self.name = mode.name
        else:
            mode = mode[0].upper() + mode[1:].lower()

            if mode == 'Major': mode = 'Ionian'
            if mode == 'Minor': mode = 'Aeolian'

            if mode in self.modesLst:
                self.name = mode
            else:
                raise ValueError('mode {} not implemented'.format(mode))

    def intervals(self, str=False):
        stepsNames = {2: 'w', 1: 'h'}
        if str:
            return '-'.join([stepsNames[s] for s in self.modesIntervals[self.name]])
        else:
            return self.modesIntervals[self.name]

    def __str__(self):
        return self.name + ': ' + self.intervals(str=True)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, mode):
        if isinstance(mode, str):
            return self.name.lower() == mode.lower()
        else:
            return self.name.lower() == mode.name.lower()

class Scale:
    chordsDegrees = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']

    def __init__(self, root='C', mode='ionian'):
        if isinstance(root,Note): root=root.name
        if ' ' in root:
            self.root = Note(root.split(' ')[0])
            self.mode = Mode(root.split(' ')[1])
        else:
            self.root = Note(root)
            self.mode = Mode(mode)

    def __str__(self):
        return '{} {:10} | {}'.format(str(self.root), str(self.mode), ' '.join([str(n) for n in self.notes()]))

    def __repr__(self):
        return self.__str__()

    def __add__(self, steps):
        return Scale(self.root + steps, self.mode.name)

    def __sub__(self, steps):
        return Scale(self.root - steps, self.mode.name)

    def __eq__(self, scale):
        x = scale.notes()
        y = self.notes()
        return all([xi in y for xi in x]) and all([yi in x for yi in y])

    def __getitem__(self, item, asStr=False):
        """
        Get chord or note from a scale
        Args:
            item: int-> nth note | str: chord by degree
        Returns:
            note or chord
        """
        if isinstance(item, str):
            return self.chords(asStr)[item]
        else:
            return self.notes(asStr)[item]

    def print(self, set='shade'):
        print(self.__str__())
        printNotes(self.notes(), fmt=set)

    def plot(self,ax=0,pos=[0, 0, 200, 40],nbOctaves=2,showName=True):
        plotNotes(self.notes(),pos=pos, ax=ax, nbOctaves=nbOctaves,name=showName*(self.root.name+' '+self.mode.name))

    def notes(self, asStr=False):
        if asStr:
            return [str(self.root + i) for i in np.insert(np.cumsum(self.mode.intervals()[:-1]), 0, 0)]
        else:
            return [self.root + i for i in np.insert(np.cumsum(self.mode.intervals()[:-1]), 0, 0)]

    def chords(self, asStr=False):
        if len(self.notes()) == 7:
            N = self.notes() * 2
            if asStr:
                return {self.chordsDegrees[n]: Chord([N[n], N[n + 2], N[n + 4], N[n + 6]], checkInv=False).name for n in
                        range(7)}
            else:
                return {self.chordsDegrees[n]: Chord([N[n], N[n + 2], N[n + 4], N[n + 6]], checkInv=False) for n in
                        range(7)}
        else:
            return {}

    def plotChords(self):
        fig = figure(figsize=(7, 4))
        grid = gridspec.GridSpec(4, 2, wspace=0.2, hspace=0.2)
        for i, degree in enumerate(self.chordsDegrees):
            ax = fig.add_subplot(grid[i])
            ax.set_xlim(0, 100)
            ax.set_ylim(0, 60)
            plotNotes(self[degree].notes(), pos=[0, 0, 100, 60], name=self[degree].name + ' (' + degree + ')',ax=ax)
            axis('off')
        suptitle('Chords built from ' + self.root.name + ' ' + self.mode.name)

    def hasChord(self, chord):
        if isinstance(chord, str): chord = Chord(chord)
        return [k for k, v in self.chords().items() if v == chord]

    def relativeMinor(self):
        if self.mode == 'Ionian':  # Relative Major is 1.5 tone below key
            return Scale(Note(self.root) - 3, 'Aeolian')
        else:
            raise ValueError('Cannot calculate relative Minor')

    def relativeMajor(self):
        if self.mode == 'Aeolian':  # Relative Minor is 1.5 tone above key
            return Scale(Note(self.root) + 3, 'Ionian')
        else:
            raise ValueError('Cannot calculate relative Major')

class Progression:
    def __init__(self, prg,name=''):
        self.beatsPerBar = 4
        self.chords = []
        self.name=name

        if '|' not in prg:
            self.name = prg
            prg = progressions[prg]

        for bi, bar in enumerate(prg.strip('|').split('|')):
            if len(bar):
                chords = [Chord(c) for c in bar.split(',')]
                for c in chords:
                    chr = {}
                    chr['chord'] = c
                    chr['beats'] = self.beatsPerBar / len(chords)
                    chr['bar'] = bi
                    self.chords.append(chr)

    def findScale(self, chr, degree='V'):
        # todo: There must be a better way
        # todo: Only looking for major keys
        # todo: Taking now the first one found
        mode = 'Ionian'
        return [Scale(k, mode) for k in Note.chrSharp if chr == Scale(k, mode)[degree]][0]

    def analyze(self):
        for c in range(len(self.chords)):
            if self.chords[c]['chord'].type in ['', '7']:
                # we found a dominant
                self.chords[c]['degree'] = 'V'
                self.chords[c]['scale'] = self.findScale(self.chords[c]['chord'], 'V')

                if c > 0:
                    if self.chords[c]['scale']['II'] == self.chords[c - 1]['chord']:
                        # we found a predominant
                        self.chords[c - 1]['degree'] = 'II'
                        self.chords[c - 1]['scale'] = self.chords[c]['scale']

                if c < len(self.chords) - 1:
                    if self.chords[c]['scale']['I'] == self.chords[c + 1]['chord']:
                        # we found the tonic
                        self.chords[c + 1]['degree'] = 'I'
                        self.chords[c + 1]['scale'] = self.chords[c]['scale']

    def asArray(self):
        P = []
        for c in self.chords:
            C = {}
            if 'chord' in c: C['chord'] = c['chord'].name
            if 'bar' in c: C['bar'] = c['bar']
            if 'beats' in c: C['beats'] = c['beats']
            if 'degree' in c: C['degree'] = c['degree']
            if 'scale' in c: C['scale'] = c['scale'].root.name + ' ' + c['scale'].mode.name
            P.append(C)
        return P

    def print(self):
        lastBar = -1
        for c in self.asArray():
            if c['bar'] > lastBar:
                lastBar += 1
                print(u"\u2588" * 2 + ' bar ' + str(lastBar) + ' ' + u"\u2588" * 27)

            if 'scale' in c:
                scaleStr = Scale(c['scale']).root.name + ' ' + Scale(c['scale']).mode.name[:3] + ': ' + ','.join(
                    (Scale(c['scale']).notes(asStr=True)))
            else:
                scaleStr = ''
            print('  {:2} {:4} x{} | {:10} | {}'.format(
                c.get('degree', ''),
                c.get('chord', ''),
                int(c.get('beats', -1)),
                ','.join(Chord(c['chord']).notes(asStr=True)) if 'chord' in c else '', scaleStr))

    def printChords(self):
        for chr in set([s.get('chord') for s in self.asArray() if 'chord' in s]):
            Chord(chr).print()

    def printScales(self):
        for sca in set([s.get('scale') for s in self.asArray() if 'scale' in s]):
            Scale(sca).print()

    def plot(self, plotScale=True, plotChord=True):
        from matplotlib import patches, gridspec
        from matplotlib.pyplot import Subplot
        lastBar = -1
        fig = figure(figsize=(12,6))
        axis('off')
        # gridspec inside gridspec
        grid = gridspec.GridSpec(4, 4, wspace=0.01, hspace=0.1)
        for i, c in enumerate(self.asArray()):
            ax = Subplot(fig, grid[i])
            fig.add_subplot(ax)
            bgd = patches.Rectangle((0, 0), 100, 100, fill=True, clip_on=False, alpha=.1)
            ax.add_patch(bgd)
            ax.set_xlim(0, 100)
            ax.set_ylim(0, 100)

            ax.text(5, 80, c['chord'], ha='left', fontSize=15, fontWeight='bold')
            if 'degree' in c: ax.text(95, 80, '$\\bf{' + c['degree'] + '}_{' + c['scale'].replace(' ', '-') + '}$',
                                      ha='right', fontSize=15)

            if c['bar'] != lastBar:
                lastBar = c['bar']
                ax.plot([0,0], [0, 100], 'k', lw=10)
            if 'chord' in c:
                if plotChord:
                    Chord(c['chord']).plot(ax=ax,pos=[10, 42, 80, 30], nbOctaves=1,showName=False)
                else:
                    ax.text(50,55,'Chord: '+','.join(Chord(c['chord']).notes(asStr=True)),ha='center',va='center')

            if 'scale' in c:
                if plotScale:
                    Scale(c['scale']).plot(ax=ax,pos=[10, 2, 80, 30], nbOctaves=2,showName=False)
                else:
                    ax.text(50,15,'Scale: '+','.join(Scale(c['scale']).notes(asStr=True)),ha='center',va='center')

            ax.axis('off')
            ax.set_xticks([])
            ax.set_yticks([])
        suptitle(self.name,size=30,weight='bold')




##

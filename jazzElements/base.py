"""
"""
import re
from itertools import permutations

from matplotlib import gridspec, patches
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
    for ni, n in enumerate(Scale('C', 'Chr').notes()):
        if n in notes: N[ni] = w

    print(3 * spc + N[1] + 2 * spc + N[3] + 9 * spc + N[6] + 2 * spc + N[8] + 2 * spc + N[10] + 7 * spc +
          3 * spc + N[1] + 2 * spc + N[3] + 9 * spc + N[6] + 2 * spc + N[8] + 2 * spc + N[10] + '\n' +
          N[0] + 2 * spc + N[2] + 2 * spc + N[4] + 4 * spc + N[5] + 2 * spc + N[7] + 2 * spc + N[9] + 2 * spc + N[
              11] + 3 * spc +
          N[0] + 2 * spc + N[2] + 2 * spc + N[4] + 4 * spc + N[5] + 2 * spc + N[7] + 2 * spc + N[9] + 2 * spc + N[
              11])


def plotNotes(notes, pos=None, name='', ax=0, nbOctaves=1):
    if pos is None:
        pos = [0, 0, 100, 40]

    def plotKey(ax, x, y, w, h, keyType, status):
        lw = .5
        pad = 0.5
        # edgeColor = 'w'
        # parms = dict(
        #     black=dict(color=['skyblue', 'steelblue'], z=1),
        #     white=dict(color=['skyblue', 'steelblue'], z=0)
        # )

        edgeColor = 'k'
        parms = dict(
            black=dict(color=['k', 'skyblue'], z=1),
            white=dict(color=['w', 'skyblue'], z=0)
        )

        ax.add_patch(FancyBboxPatch((x + pad, y + pad),
                                    abs(w) - 2 * pad, abs(h) - 2 * pad,
                                    boxstyle="round,pad=" + str(pad),
                                    fc=parms[keyType]['color'][status], ec=edgeColor, zorder=parms[keyType]['z'],
                                    lw=lw))

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
            plotKey(ax, pos[0] + (nWhites) * whiteWidth, pos[1], whiteWidth, pos[3], keyType='white', status=n in notes)
            nWhites += 1
        else:
            plotKey(ax, pos[0] + (nWhites) * whiteWidth - blackWidth / 2, pos[1] + pos[3] / 3, blackWidth,
                    2 * pos[3] / 3, keyType='black', status=n in notes)
    plot(0, 0, '.w', zorder=-1)
    if name:
        text(pos[0], pos[1] + pos[3] / 2, name, ha='right', va='center', rotation=90)


progressions = \
    {
        'Satin Doll': '|Dm7,G7|%|Em7,A7|%|Am7,D7|Abm7,Db7|CM7|%|',

        'Misty': '|B7b9|EbM7|Bbm7,Eb7|AbM7|Abm7,Db7|EbM7,Cm7|Fm7,Bb7|Gm7,C7|Fm7,Bb7|',

        'Major 251s': '|Dm7,G7|CM7|E♭m7,A♭7|D♭M7|Em7,A7|DM7|Fm7,B♭7|E♭M7|F♯m7,B7|EM7|'
                      'Gm7,C7|FM7|A♭m7,D♭7|G♭M7|Am7,D7|GM7|B♭m7,E♭7|A♭M7|Bm7,E7|AM7|Cm7,F7|B♭M7|C♯m7,F♯7|BM7|',

        'Minor 251s': '|Dø,Gm7|Cm7|E♭ø,A♭m7|D♭m7|Eø,Am7|Dm7|Fø,B♭m7|E♭m7|F♯ø,Bm7|Em7|'
                      'Gø,Cm7|Fm7|A♭ø,D♭m7|G♭m7|Aø,Dm7|Gm7|B♭ø,E♭m7|A♭m7|Bø,Em7|Am7|Cø,Fm7|B♭m7|C♯ø,F♯m7|Bm7|',

        'All Of Me': '|CM7|%|E7|%|A7|%|Dm|%|E7|%|Am|%|D7|%|Dm7|G7|'
                     'CM7|%|E7|%|A7|%|Dm|%|F|Fm|CM7,Em7|A7|Dm7|G7|C6,Ebdim|Dm7,G7|',

        'My Romance': '|CM7,FM7|Em7,Am7|Dm7,G7|CM7,E7#5|Am7,E7#5|Am7,A7#5|Dm7,G7|CM7,C7|'
                      'FM7,Bb7|CM7,C7|FM7,Bb7|CM7|F#m7b5,B7|Em7,Bb7|Am7,D7|Dm7,G7|',  # INCOMPLETE

        'All The Things You Are':
            '|Fm7|Bbm7|Eb7|AbM7|DbM7|Dm7,G7|CM7|%'
            '|Cm7|Fm7|Bb7|EbM7|AbM7|Am7,D7|GM7|%'
            '|Am7|D7|GM7|%|Am7|D7|GM7|%'
            '|F#m7|B7|EM7|C7#5|Fm7|Bbm7|Eb7|AbM7'
            '|DbM7|Dbm7|Cm7|Bo7|Bbm7|Eb7|AbM7|G7,C7|',

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
    altLst = {sharp: 1, Sharp: 1, flat: -1, Flat: -1, natural: 0, Natural: 0, '?': 0, '-': -1, '+': 1}

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
                    raise ValueError('Alteration unknown: {}'.format(alti))
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

    intervalsLst = ['1', 'b2', '2', 'b3', '3', '4', 'b5', '5', '#5', '6', 'b7', '7', '8',
                    'b9', '9', '#9', '10', '11', '#11', '12', '#12', '13', 'b14', '14', '15']

    typesLst = {
        # Major
        '': '1-3-5',
        'M6': '1-3-5-6',
        '6': '1-3-5-6',
        '6/9': '1-3-5-6-4',
        'M7': '1-3-5-7',
        'M9': '1-3-5-7-2',
        'M9(no7)': '1-3-5-2',
        'M(add9)': '1-3-5-2',
        'M11': '1-3-5-7-2-4',

        # Minor
        'm': '1-b3-5',
        'm6': '1-b3-5-6',
        'm7': '1-b3-5-b7',
        'm9': '1-b3-5-b7-2',
        'm9(no7)': '1-b3-5-2',
        'm7b9': '1-b3-5-b7-b2',
        'm7b5b9': '1-b3-b5-b7-b2',
        'm11': '1-b3-5-b7-2-4',

        # Dominant
        '7': '1-3-5-b7',
        '7+5': '1-3-#5-b7',
        '7#5': '1-3-#5-b7',
        '9': '1-3-5-b7-2',
        '7b9': '1-3-5-b7-b2',
        '11': '1-3-5-b7-2-4',
        '11(no7)': '1-3-5-2-4',
        '11(no7,no9)': '1-3-5-4',
        '11(no9)': '1-3-5-b7-4',
        '13': '1-3-5-b7-2-4-6',
        '13(no7)': '1-3-5-2-4-6',  # todo ugly
        '13(no9)': '1-3-5-b7-4-6',
        '13(no11)': '1-3-5-b7-2-6',
        '13(no7no9)': '1-3-5-4-6',
        '13(no7no11)': '1-3-5-2-6',
        '13(no9no11)': '1-3-5-b7-2-4-6',

        # diminished
        'o': '1-b3-b5',
        'o7': '1-b3-b5-6',  # bb7->6
        'dim': '1-b3-b5',
        'dim7': '1-b3-b5-6',  # bb7->6
        u'\u00F8': '1-b3-b5-b7',
        'hdim': '1-b3-b5-b7',
        'm7b5': '1-b3-b5-b7',
        # augmented
        'aug': '1-3-#5',
        '+': '1-3-#5',
        # sus
        'sus4': '1-4-5',
        'sus2': '1-2-5',
        '7sus4': '1-4-5-b7',
        '7sus2': '1-2-5-b7',
        '9sus4': '1-4-5-b7-2',
        '9sus2': '1-2-5-b7-2',
        # misc:
        '5': '1-3',

    }
    regexChord = re.compile(r"([a-zA-Z]{1})([#b♭♯]*)(.*)")  # Regular expression to understand Chord Notation

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
            root, alt, chrType = re.search(self.regexChord, nameOrNotes).groups()
            self.root = Note(root + alt)
            self.type = chrType

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

            if len(chrdType) > 1:
                chrdType.sort(key=len)  # todo: Best match shouldnt be done this way
                # print('Found {} choosing {}'.format(','.join(chrdType), chrdType[0]))

            if len(chrdType):
                self.root = Chord(chrdType[0]).root
                self.type = Chord(chrdType[0]).type
            else:
                print('Cannot find a chord from ' + ','.join(nameOrNotes))
                self.root = Note(nameOrNotes[0])
                self.type = '?'
        self.name = str(self.root) + self.type

    def intervals(self, asStr=False):
        """
        Return intervals of the chord
        Args:
            asStr: if True, returns as strings list, otherwise as list of steps
        """
        if self.type == '?':
            return ''

        if asStr:
            return self.typesLst[self.type].split('-')
        else:
            return [self.intervalsLst.index(i) for i in self.typesLst[self.type].split('-')]

    def plot(self, ax=0, pos=None, nbOctaves=1, showName=True):
        if pos is None:
            pos = [0, 0, 100, 40]
        plotNotes(self.notes(), ax=ax, pos=pos, nbOctaves=nbOctaves, name=showName * self.name)

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
        if isinstance(notesOrScale, str):
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
        for key in Scale('C', 'Chr').notes():
            for mode in Scale.modesLst:
                if mode is not 'Chr':
                    chr = Scale(key, mode).hasChord(self)
                    if chr:
                        lst.append([key.name + ' ' + mode, chr])
        return lst


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
        'Chr': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
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

        mode = mode[0].upper() + mode[1:].lower()

        if mode in ['Major', 'Maj']: mode = 'Ion'
        if mode in ['Minor', 'Min']: mode = 'Aeo'
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
            plotNotes(c.notes(), pos=[0, 0, 100, 60], name=c.name + '  ' + d.replace(' ', ' $^{') + '}$', ax=ax)
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
                 if 3 in c.intervals() else self.chrDegLst[d] + c.type).strip()
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

        if all([n in self.notes() for n in chord.notes()]):
            if chord in self.chords(nbNotes=len(chord.notes())):

                return self.chordsRoman(nbNotes=len(chord.notes()))[
                    self.chords(nbNotes=len(chord.notes())).index(chord)]
            else:
                print('Found {} in {} but cannot calculate it'.format(chord.name, self.name))

        return False


class Progression:
    def __init__(self, prg, name=''):
        # todo: chords are now of equal duration within a bar.
        self.beatsPerBar = 4
        self.chords = []
        self.name = name

        if '|' not in prg:
            self.name = prg
            prg = progressions[prg]
        for bi, bar in enumerate(prg.strip('|').split('|')):
            if len(bar):
                for c in bar.split(','):
                    if c == '%':
                        chr = dict(
                            chord=self.chords[-1]['chord'],
                            beats=self.beatsPerBar / len(bar.split(',')),
                            bar=bi)
                    else:
                        chr = dict(
                            chord=Chord(c),
                            beats=self.beatsPerBar / len(bar.split(',')),
                            bar=bi)
                    self.chords.append(chr)

        self.nbBars = self.chords[-1]['bar'] + 1

    def findScale(self, chr, degree):
        # todo: There must be a better way
        # todo: Only looking for major keys
        # todo: Taking now the first one found
        mode = 'Ion'
        return [[Scale(k, mode), Scale(k, mode).hasChord(chr)] for k in Note.chrSharp if
                Scale(k, mode).getDegree(degree) == chr]

    def analyze(self, key=None):
        """
        Harmonic Analysis of the chord progression
        Args:
            key: force a given key (str)

        Following WalkThatBass:
        http://www.thejazzpianosite.com/jazz-piano-lessons/jazz-chord-progressions/how-to-analyse-a-chord-progression-harmonic-analysis/

        Level 1:
        - Find the most represented key
        - Annotate chords using this key
        Level 2:
        - Annotate Function: (PD,D,T)
        - Annotate Second Level Chords
            Everything before PD-D-T is a Tonic Prolongation (prolongs the tonic without a cadence)
            They can be Substitutions, or Quick Passing Chords
        - Look for non-diatonic chords:
            Long period (>1bar): Modulation
            Short Period (.5-1 bar): Passing Chord | Borrowed Chord | Secondary Dominant

        Improvisation:
        - first level: We can use the relevant mode under each chord, but we change scale all the time
        - or in the second level: We use the functionally important chords
        then we can go into crazy stuff i.e. side slipping, cycled patterns, chromatic runs etc...

        """
        # ---------------------------------- LEVEL 1 ----------------------------------
        # Find the most represented key:
        if key is None:
            key = self.findKey()[0][0]
        keyChords = Scale(key).chords(3) + Scale(key).chords(4)
        keyDegrees = Scale(key).chordsRoman(3) + Scale(key).chordsRoman(4)

        # Annotate chords from this key:
        for c in self.chords:
            if c['chord'] in keyChords:
                c['scale'] = Scale(key)
                c['degree'] = keyDegrees[keyChords.index(c['chord'])]

        # ---------------------------------- LEVEL 2 ----------------------------------
        # Annotate T, PD, D
        chordFunctions = dict(T=['I'], PD=['II'], D=['V'])
        for c in self.chords:
            if 'degree' in c:
                alt, deg, chrType = re.search(Scale.regexRoman, c['degree']).groups()
                for fn in chordFunctions:
                    if deg.upper() in chordFunctions[fn]:  c['function'] = fn

        # Find Single Chord Substitutions
        subs = Scale(key).possibleSubstitutions(True)
        for c in self.chords:
            if 'function' not in c:
                s = [[s[0][0], s[2]] for s in subs if len(s[1]) == 1 and Chord(s[1][0]) == c['chord']]
                if len(s) == 1:
                    # c['degree']=s[0][0]
                    c['function'] = s[0][1]
                    c['scale'] = Scale(key)
                elif len(s) > 1:
                    raise ValueError('Found multiple substitutions at bar ' + str(c['bar']) + ' ' + c['chord'].name)

    def asArray(self):
        P = []
        for c in self.chords:
            C = {}
            if 'chord' in c: C['chord'] = c['chord'].name
            if 'bar' in c: C['bar'] = c['bar']
            if 'beats' in c: C['beats'] = c['beats']
            if 'degree' in c: C['degree'] = c['degree']
            if 'function' in c: C['function'] = c['function']
            if 'scale' in c: C['scale'] = c['scale'].root.name + ' ' + c['scale'].mode
            P.append(C)
        return P

    def findKey(self):
        """
        Finds and orders potential keys for the progression using the number of corresponding chords.

        Returns:
            list of lists  [[<key>,<probability>],...]
        """
        S = []
        for k in Note.chrFlat:
            scaleChords = Scale(k, 'Ion').chords(3) + Scale(k, 'Ion').chords(4)
            S.append([str(k) + ' Ion',
                      100 * len([chr['chord'] for chr in self.chords if chr['chord'] in scaleChords]) / len(
                          self.chords)])
        S.sort(key=lambda s: s[1], reverse=True)
        return S

    def print(self):
        lastBar = -1
        print('{:4} |{:7} |{:8}| {:5} |{:10}'.format(
            'Bar', 'Chord', 'Function', 'Type', 'Scale'))

        for c in self.chords:
            print('{:4} |{:7} |{:8}| {:5} |{:10}'.format(
                str(c['bar'] + 1) if c['bar'] != lastBar else '',
                c['chord'].name,
                c['function'] if 'function' in c else '',
                c.get('degree', ''),
                c['scale'].name if 'scale' in c else '',
            ))
            lastBar = c['bar']

    def plotChord(self, ax, chr, pos, plotType='fn'):
        xChr, yChr, wChr, hChr = pos
        bgd = patches.Rectangle((xChr, yChr), wChr, hChr, fill=False, clip_on=False, color='k')
        ax.add_patch(bgd)
        # Function
        if plotType == 'fn':
            root, alt, chrType = re.search(Chord.regexChord, chr['chord'].name).groups()
            text(xChr + wChr / 2, yChr + 2 * hChr / 3, '{}{}$^{{{}}}$ '.format(root, alt, chrType.replace('#', '+')),
                 va='center', ha='right' if 'degree' in chr else 'center', fontSize=10,
                 bbox=dict(boxstyle='round4', fc='skyblue'), weight=1000)

            if 'degree' in chr:
                alt, deg, chrType = re.search(Scale.regexRoman, chr['degree']).groups()
                text(xChr + wChr / 2, yChr + 2 * hChr / 3, ' {}{}$^{{{}}}$'.format(alt, deg, chrType.replace('#', '+')),
                     va='center', ha='left', fontSize=10, weight=1000)
            if 'scale' in chr:
                text(xChr + 2, yChr, chr['scale'].name,
                     va='bottom', ha='left', fontSize=7, weight=1000, style='italic')

            x = xChr + wChr / 2
            y = yChr + hChr / 3
            if 'function' in chr:
                if chr['function'] == 'T' or 'sub1' in chr['function']: fnc = 'b'
                if chr['function'] == 'PD' or 'sub2' in chr['function']: fnc = 'g'
                if chr['function'] == 'D' or 'sub5' in chr['function']: fnc = 'g'
                bgd = patches.Rectangle((xChr, yChr), wChr, hChr, fill=True, clip_on=False, color=fnc, alpha=.1)
                ax.add_patch(bgd)
                text(x, y, chr['function'], va='center', ha='center', fontSize=10, weight='bold')

        if plotType == 'kbd':
            root, alt, chrType = re.search(Chord.regexChord, chr['chord'].name).groups()
            text(xChr + wChr / 2, yChr + hChr, '{}{}$^{{{}}}$ '.format(root, alt, chrType.replace('#', '+')),
                 fontsize=14, va='top', ha='right' if 'degree' in chr else 'center', fontSize=10,
                 bbox=dict(boxstyle='round4', fc='skyblue'), weight=1000)

            if 'degree' in chr:
                alt, deg, chrType = re.search(Scale.regexRoman, chr['degree']).groups()
                text(xChr + wChr / 2, yChr + hChr, ' {}{}$^{{{}}}$'.format(alt, deg, chrType.replace('#', '+')),
                     va='top', ha='left', fontSize=10, weight=1000)

            Chord(chr['chord']).plot(ax=ax, pos=[xChr + 3, yChr + 3 + (hChr - 10) / 2, wChr - 6, (hChr - 10) / 2],
                                     nbOctaves=1, showName=False)
            if 'scale' in chr:
                Scale(chr['scale'].name).plot(ax=ax, pos=[xChr + 3, yChr + 1, wChr - 6, (hChr - 10) / 2], nbOctaves=1,
                                              showName=False)

    def plotBar(self, b, pos, plotType='fn'):
        # Debug:
        # bgd = patches.Rectangle((xBar,yBar), wBar, hBar,color='r', fill=False, clip_on=True, alpha=1,linestyle='dashed')
        # ax.add_patch(bgd)
        xBar, yBar, wBar, hBar = pos
        chrs = [c for c in self.chords if c['bar'] == b]
        wBeat = (wBar - self.sepx * (len(chrs) - 1)) / self.beatsPerBar
        nBeats = 0
        ax = gca()
        for ic, c in enumerate(chrs):
            posChr = [xBar + wBeat * nBeats + self.sepx * (ic), yBar, c['beats'] * wBeat, hBar]
            self.plotChord(ax, c, posChr, plotType=plotType)
            nBeats += c['beats']
            if nBeats >= self.barsPerRow * self.beatsPerBar:
                nBeats = 0
                yBar -= (hBar + self.sepy)

        # Plot Bar
        plot([xBar - self.sepx / 2, xBar - self.sepx / 2], [yBar, yBar + hBar], color='k', lw=3)
        text(xBar - self.sepx / 2, yBar + hBar, '{:02}'.format(b + 1), color='w', va='top', ha='center', fontSize=8,
             weight=1000,
             bbox=dict(boxstyle='round4', fc='k'))

    def plot(self, plotType='fn'):
        # todo: Scaling issues
        if plotType == 'fn':
            self.barsPerRow = 4
            nbRows = np.ceil(self.nbBars / self.barsPerRow)
            figure(figsize=(2 * self.barsPerRow, nbRows))
        else:
            self.barsPerRow = 4
            nbRows = np.ceil(self.nbBars / self.barsPerRow)
            figure(figsize=(2.5 * self.barsPerRow, 2 * nbRows))

        x, y, w, h, self.sepx, self.sepy = [0, 0, 200, 200, 0, 5]

        nbRows = np.ceil(self.nbBars / self.barsPerRow)
        wBar = (w - (self.barsPerRow - 1) * self.sepx) / self.barsPerRow
        hBar = (h - (nbRows - 1) * self.sepy) / nbRows

        for b in range(self.chords[-1]['bar'] + 1):
            posBar = [x + (b % self.barsPerRow) * (wBar + self.sepx),
                      y + h - hBar * (1 + (b // self.barsPerRow)) - self.sepy * ((b // self.barsPerRow)), wBar, hBar]
            self.plotBar(b, posBar, plotType=plotType)

        axis('tight')
        axis('off')
        suptitle(self.name, size=30, weight='bold')

import re
from itertools import permutations
from jazzElements.note import Note
from jazzElements.viz import plotNotes
import warnings
class Chord:
    """
    Create a chord from chord name or list of notes

    Args:
        nameOrNotes: chord names or notes within chord

    Examples:
        c=Chord('Em7')
        c=Chord(['C','E','G'])
    """
    intLst = ['1', '♭2', '2', '♭3', '3', '4', '♭5', '5', '♯5', '6', '♭7', '7', '8', '♭9', '9', '♯9', '10', '11', '♯11',
              '12', '♯12', '13']

    regexChord = re.compile(r"([a-zA-Z]{1})([#b♭♯]*)(.*)")  # Regular expression to understand Chord Notation

    chrLst = {
        '1': [0],
        '5': [0, 7],
        'm': [0, 3, 7],
        'm6': [0, 3, 7, 9],
        'm7': [0, 3, 7, 10],
        'mM7':[0, 3, 7,11],
        'm6/9': [0, 3, 7, 9, 14],
        'm9': [0, 3, 7, 10, 14],
        'm11': [0, 3, 7, 10, 14, 17],
        'm11+': [0, 3, 7, 10, 14, 18],
        'm13': [0, 3, 7, 10, 14, 17, 21],
        'm7-9': [0, 3, 7, 10, 13],
        '+5': [0, 4, 8],
        'M': [0, 4, 7],
        '': [0, 4, 7],
        'M6': [0, 4, 7, 9],
        '6': [0, 4, 7, 9],
        '6/9': [0, 4, 7, 9, 14],
        'M6/9': [0, 4, 7, 9, 14],
        '7': [0, 4, 7, 10],
        'M7': [0, 4, 7, 11],
        'M13': [0, 4, 7, 11,13],
        'M7+5': [0, 4, 8, 11],
        'M7#5': [0, 4, 8, 11],
        '7-5': [0, 4, 6, 10],
        '7b5': [0, 4, 6, 10],
        '7-9': [0, 4, 7, 10, 13],
        '7b9': [0, 4, 7, 10, 13],
        '9': [0, 4, 7, 10, 14],
        'M9': [0, 4, 7, 11, 14],
        '7-10': [0, 4, 7, 10, 15],
        '11': [0, 4, 7, 10, 14, 17],
        'M11': [0, 4, 7, 11, 14, 17],
        '11+': [0, 4, 7, 10, 14, 18],
        '13': [0, 4, 7, 10, 14, 17, 21],

        '7+5': [0, 4, 8, 10],
        '7+5-9': [0, 4, 8, 10, 13],

        'sus4': [0, 5, 7],
        '7sus4': [0, 5, 7, 10],
        '9sus4': [0, 5, 7, 10, 14],

        'sus2': [0, 2, 7],
        '7sus2': [0, 2, 7, 10],
        '9sus2': [0, 2, 7, 10, 14],

        'o': [0, 3, 6],
        'o7': [0, 3, 6, 9],
        'ø': [0, 3, 6, 10],
        '9+5': [0, 10, 13],
        'm9+5': [0, 10, 14],
        'm+5': [0, 3, 8],
        'aug': [0, 3, 8],
        'aug6': [0, 3, 8,9],

        'm7+5': [0, 3, 8, 10],
        'm7+5-9': [0, 3, 8, 10, 13],
    }

    chrReplace = [('maj', 'M'), ('Maj', 'M'), ('hdim', 'ø'), ('m7-5', 'ø'), ('m7b5', 'ø'),
                  ('dim', 'o'), ('7#5', '7+5')]

    chrFamilies = \
        {
            'maj': ['M', 'M6', 'M7', 'M9', 'M13', '6/9',''],
            'min': ['m', 'm6', 'm7', 'm9', 'm11', 'm13','mM7'],
            'dim': ['o', 'o7', 'ø'],
            'dom': ['7', '7b5', '9', '13'],
            'aug': ['aug','aug6', '7+5'],
            'sus': ['sus4', 'sus2', '7sus4']
        }

    def update(self):
        self.notes = []
        self.intArr = []
        self.intStr = []
        if self.type not in self.chrLst:
            return
        self.intArr = self.chrLst[self.type]
        self.intStr = [self.intLst[n] for n in self.intArr]
        if self.intArr:
            self.notes = [Note(self.root.name, i - 12 if '♭' in iStr else i) for i, iStr in
                          zip(self.intArr, self.intStr)]
        if self.intStr[:3]==['1','♭3','♭5']: self.quality='dim'
        elif self.intStr[:4]==['1','3','5','♭7']: self.quality='dom'
        elif self.intStr[:4]==['1','3','♭5','♭7']: self.quality='dom'
        elif self.intStr[:3] == ['1', '♭3', '♯5']: self.quality = 'aug'
        elif self.intStr[:3] == ['1', '3', '♯5']: self.quality = 'aug'
        elif self.intStr[:3] == ['1', '2', '5']: self.quality = 'sus'
        elif self.intStr[:3] == ['1', '4', '5']: self.quality = 'sus'
        elif self.intStr[:3] == ['1', '3', '5']: self.quality = 'maj'
        elif self.intStr[:3] == ['1', '♭3', '5']: self.quality = 'min'
        else:
            self.quality='?'
            warnings.warn('cannot resolve chord quality for '+self.name)


    def __init__(self, nameOrNotes, checkInv=True):


        self.notes = []
        self.intArr = []
        self.intStr = []
        if isinstance(nameOrNotes, str):
            root, alt, chrType = re.search(self.regexChord, nameOrNotes).groups()
            self.root = Note(root + alt)

            for r in self.chrReplace:
                chrType = chrType.replace(r[0],r[1])

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
                chrdType.extend([lst[0]+cType for cType in self.chrLst if intervals==self.chrLst[cType]])

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
        self.update()

    def plot(self, ax=0, pos=None, nbOctaves=1, showName=True):
        if pos is None:
            pos = [0, 0, 100, 40]
        if self.notes != []:
            plotNotes(self.notes, ax=ax, pos=pos, nbOctaves=nbOctaves, name=showName * self.name)

    def guideTones(self, asStr=False):
        """
        Guide Tones are the 3rd and the 7th of a chord. They are the most harmonically important as they
        determine its quality, so we want to focus on them.
        Args:
            asStr: return a string list

        Returns:
            list of guide tones
        """
        if asStr:
            [self.notes[1].name if len(self.notes)>=2 else [], self.notes[3].name if len(self.notes)>=4 else []  ]
        else:
            return [self.notes[1] if len(self.notes)>=2 else [], self.notes[3] if len(self.notes)>=4 else []  ]


    # def avoidNotes(self, notesOrScale, asStr=False):
    #     """
    #     Avoid notes are notes one step above a chord note, use sparingly and while passing
    #     """
    #     if isinstance(notesOrScale, Scale):
    #         notesOrScale = notesOrScale.notes()
    #     if isinstance(notesOrScale, str):
    #         if ' ' in notesOrScale:
    #             notesOrScale = Scale(notesOrScale).notes()
    #
    #     avoid = [n + 1 for n in self.notes()]
    #     avoidNotes = [an for an in notesOrScale if an in avoid]
    #     return [str(gt) for gt in avoidNotes] if asStr else avoidNotes

    def relativeMinor(self, asStr=False):
        if self.intArr[1] == 4:
            if self.type == '':
                chr = Chord((self.root - 3).name + 'm')
            else:
                chr = Chord((self.root - 3).name + self.type.replace('M', 'm'))
            return chr.name if asStr else chr
        else:
            raise ValueError('Cannot calculate relative minor chord')


    def relativeMajor(self, asStr=False):
        if self.intArr[1] == 3:
            if self.type == '':
                chr = Chord((self.root + 3).name + 'M')
            else:
                chr = Chord((self.root + 3).name + self.type.replace('m', 'M'))
            return chr.name if asStr else chr
        else:
            raise ValueError('Cannot calculate relative major chord')

    def __str__(self):
        if not self.notes:
            return '?'
        else:
            return self.root.name+self.type

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.notes)

    def __eq__(self, chordOrStr):
        x = Chord(chordOrStr).notes
        y = self.notes
        if x and y and len(x) == len(y) and all([n in y for n in x]):
            return True
        else:
            return False

    # REMOVED TO FIX IMPORTS
    # def listScales(self):
    #     """
    #     Lists the keys on which we have this chord
    #     """
    #     lst = []
    #     for key in Scale('C', 'Chr').notes():
    #         for mode in Scale.modesLst:
    #             if mode is not 'Chr':
    #                 chr = Scale(key, mode).hasChord(self)
    #                 if chr:
    #                     lst.append([key.name + ' ' + mode, chr])
    #     return lst
import pandas as pd
from jazzElements.chord import Chord
from jazzElements.note import Note
from jazzElements.scale import Scale


class CadenceGraph():
    # todo: add T, SD, D
    ##
    fnLst = {
        'I': [(1, 'M'), (1, 'M7'), (1, 'M9'), (1, 'M6/9'), (1, 'M')],
        'ii': [(2, 'm'), (2, 'm7'), (2, 'm9'), (4, 'M6')],
        'iii': [(3, 'm'), (3, 'm7'), (3, 'm9'), (3, 'M6')],
        'IV': [(4, 'M'), (4, 'M7'), (4, 'M9'), (4, 'M6/9'), (4, 'M6'), (2, 'm7')],
        'V': [(5, 'M'), (5, '7'), (5, '9'), (5, '7#5')],  # todo: add ,(2b,'7')
        'vi': [(6, 'm'), (6, 'm7'), (6, 'm9'), (1, 'M6')],
        'vii': [(7, 'dim'), (7, 'hdim'), (7, 'm6')]
    }
    fnSeq = \
        {
            'I': ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii'],
            'ii': ['IV', 'V', 'vii'],
            'iii': ['ii', 'vi'],
            'IV': ['I', 'V', 'vi', 'vii'],
            'V': ['I', 'vi', 'IV'],
            'vi': ['ii', 'IV', 'V'],
            'vii': ['I', 'iii'],
        }

    fnTypes = dict(I='T', ii='SD', iii='T', IV='SD', V='D', vi='T', vii='D')

    def __init__(self, key):
        N = Scale(key, 'major').notes(asStr=True)
        self.degrees = {fn: [Chord(N[f[0] - 1] + f[1]) for f in self.fnLst[fn]] for fn in self.fnLst}
        self.chords = [Chord(chr) for chr in
                       set([item.name for sublist in [self.degrees[f] for f in self.degrees] for item in sublist])]

    def known(self, chr):
        return chr in self.chords

    def degree(self, chr):
        F = []
        for f in self.degrees:
            for c in self.degrees[f]:
                if c == chr and f not in F:
                    F.append(f)
        return F


class Annotate():
    def __init__(self, chords):
        self.name = ''
        self.description = ''
        self.ann = pd.DataFrame(columns=['fn', 'deg', 'sca', 'cad'])
        if isinstance(chords,pd.DataFrame):
            self.chords = [Chord(c) for c in chords['chr'].values]
        else:
            self.chords = [Chord(c) for c in chords]

        self.cleanup()

    def cleanup(self):
        self.fn = [[] for c in self.chords]
        self.deg = [[] for c in self.chords]
        self.sca = [[] for c in self.chords]
        self.cad = [[] for c in self.chords]

    def run(self, reduce=True):
        """
        Fills self.ann with the annotations
        format: (<function>,<degree>,<scale>,<cadence>)
        """

    def print(self):
        print('{:7}|{:3}|{:3}|{:3}|{:15}'.format('chord', 'fn', 'deg', 'sca', 'cadence'))
        for c in range(len(self.chords)):
            print('{:7}|{:3}|{:3}|{:3}|{:15}'.format(
                self.chords[c].name,
                ','.join(self.fn[c]),
                ','.join(self.deg[c]),
                ','.join(self.sca[c]),
                ','.join(self.cad[c])))


class annGraph(Annotate):
    def __init__(self, chords):
        Annotate.__init__(self, chords)
        self.name = 'Graph Method'
        self.description = 'We annotate first the longest sequences using a cadence graph'

    def findCadencesInKey(self, key):
        """
        Returns possible cadences in self.chords using key
        Returns:
            list of cadences: (<size>,<start>,<key>,<cadenceList>)
        """
        ##
        keyCad = CadenceGraph(key)
        Seq = []
        cur = []  # [(<start>,<list>),...]

        for ci, c in enumerate(self.chords):
            if c in keyCad.chords:  # Current chord is in keyCad
                if len(cur):  # At least an ongoing cadence
                    newCur = []
                    for x in cur:
                        for d in keyCad.degree(c):
                            if d in keyCad.fnSeq[x[1][-1]]:  # The current chord can continue this sequence
                                newCur.append((x[0], x[1] + [d]))

                            else:  # A new sequence starts here
                                newCur.append((ci, [d]))
                    cur = newCur.copy()

                else:  # No cadence ongoing
                    cur = [(ci, [x]) for x in keyCad.degree(c)]

            else:  # current chord isnt in keyCad
                for x in cur:
                    Seq.append((len(x[1]), x[0], key, x[1]))
                cur = []
        if cur:
            for x in cur:
                Seq.append((len(x[1]), x[0], key, x[1]))

        ##
        return Seq

    def annotate(self, reduce=True):
        self.cleanup()
        # Find cadences in all keys
        X = []  # [(<size>,<start>,<key>,<cadence>),...]
        for key in Note.chrFlat:
            X.extend(self.findCadencesInKey(key))
        X.sort(key=lambda x: x[0], reverse=True)  # Sort by size

        used = [False] * len(self.chords)
        for x in X:
            if not reduce or not all(used[x[1]:(x[1] + x[0])]):  # All spots are unused
                for ci, c in enumerate(range(x[1], (x[1] + x[0]))):
                    self.fn[c].append(CadenceGraph.fnTypes[x[3][ci]])
                    self.deg[c].append(x[3][ci])
                    self.sca[c].append(x[2])
                    self.cad[c].append('-'.join(x[3]))
                    used[c] = True

        self.ann = pd.DataFrame(dict(fn=self.fn, deg=self.deg, sca=self.sca, cad=self.cad))



import warnings

import pandas as pd

from jazzElements.chord import Chord
from jazzElements.note import Note
from jazzElements.scale import Scale


class CadenceGraph():
    cadGraphs = \
        {
            # majLotus deprecated, need to update to new format
            # 'majLotus':
            #     {
            #         'description': 'major chord progression from lotusmusic.com',
            #         'key': 'maj',
            #         'degrees':
            #             {
            #                 'I': [(1, 'M'), (1, 'M7'), (1, 'M9'), (1, 'M6/9'), (1, 'M')],
            #                 'ii': [(2, 'm'), (2, 'm7'), (2, 'm9'), (4, 'M6')],
            #                 'iii': [(3, 'm'), (3, 'm7'), (3, 'm9'), (3, 'M6')],
            #                 'IV': [(4, 'M'), (4, 'M7'), (4, 'M9'), (4, 'M6/9'), (4, 'M6'), (2, 'm7')],
            #                 'V': [(5, 'M'), (5, '7'), (5, '9'), (5, '7#5')],  # todo: add ,(2b,'7')
            #                 'vi': [(6, 'm'), (6, 'm7'), (6, 'm9'), (1, 'M6')],
            #                 'vii': [(7, 'dim'), (7, 'hdim'), (7, 'm6')]
            #             },
            #         'next':
            #             {
            #                 'I': ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii'],
            #                 'ii': ['ii', 'IV', 'V', 'vii'],
            #                 'iii': ['iii', 'ii', 'vi'],
            #                 'IV': ['IV', 'I', 'V', 'vi', 'vii'],
            #                 'V': ['V', 'I', 'vi', 'IV'],
            #                 'vi': ['vi', 'ii', 'IV', 'V'],
            #                 'vii': ['vii', 'I', 'iii'],
            #             },
            #         'types':
            #             dict(I='T', ii='SD', iii='T', IV='SD', V='D', vi='T', vii='D')
            #     },

            'majKostka':
                {
                    'description': 'major chord progression from Tonal Harmony by Stefan Kostka',
                    'key': 'maj',
                    'next':
                        {
                            1: [1,2,3,4,5,6,7],
                            2: [2,1,5,7],
                            3: [3,2,6,4],
                            4: [4,2,5,7,1],
                            5: [5,6,7,1],
                            6: [6,2,4],
                            7: [7,6,5,1],
                        },
                },

            'minKostka':
                {
                    # todo: add bVII
                    # todo: this one uses only the harmonic minor scale, should we do all three?
                    # todo: check all minor chords
                    # todo: find a way to find which chords should be there, maybe move to scale...
                    'description': 'minor chord progression from Tonal Harmony by Stefan Kostka',
                    'key': 'harMin',
                    'next':
                        {
                            1: [1, 2, 3, 4, 5, 6, 7],
                            2: [2, 1, 5, 7],
                            3: [3, 2, 6, 5],
                            4: [4, 2, 5, 7, 1],
                            5: [5, 6, 7, 1],
                            6: [6, 2, 4],
                            7: [7, 6, 5, 1],

                            # 'i': ['i', 'iio', 'III+', 'iv', 'V', 'VI', 'viio'],
                            # 'iio': ['iio', 'V', 'viio', 'i'],
                            # 'III+': ['III+', 'VI', 'V', 'iio'],
                            # 'iv': ['iv', 'iio', 'V', 'viio', 'i'],
                            # 'V': ['V', 'viio', 'VI', 'i'],
                            # 'VI': ['VI', 'iv', 'iio'],
                            # 'viio': ['viio', 'V', 'VI', 'i'],
                        },
                    'types':
                        {'i': 'T', 'iio': 'SD', 'III+': 'T', 'iv': 'SD', 'V': 'D', 'VI': 'T', 'viio': 'D'}
                },

        }

    def __init__(self, root, cadGraph='majKostka'):
        if cadGraph not in self.cadGraphs:
            raise ValueError(
                'scale type not implemented for cadence analysis (' + '|'.join(
                    [_ for _ in self.cadGraphs.keys()]) + ')')
        self.root = root
        self.cadGraph = cadGraph
        self.scaleType = self.cadGraphs[cadGraph]['key']
        self.fnSeq = self.cadGraphs[cadGraph]['next']
        self.fnTypes = {1:'T', 2:'ST', 3:'M', 4:'SD', 5:'D', 6:'SM', 7:'L'} #todo: can types be generic or moved to scale?
        self.degreesRoman=Scale(self.root,self.cadGraphs[cadGraph]['key']).degrees()
        self.degrees = {d+1:Scale(self.root, self.cadGraphs[cadGraph]['key']).getDegreeFamily(d+1) for d in range(len(self.degreesRoman))}
        self.chords = [Chord(chr) for chr in
                         set([item.name for sublist in [self.degrees[f] for f in self.degrees] for item in sublist])]

    def inCadence(self, chr):
        return chr in self.chords

    def getDegree(self, chr,strict=True):
        """
        Get the degree of a chord in a given cadence
        Args:
            chr:
            strict:

        Returns:

        """
        F = []
        for f in self.degrees:
            for c in self.degrees[f]:
                if strict:
                    if c.name == chr and f not in F:
                        F.append(f)
                else:
                    if c == chr and f not in F:
                        F.append(f)
        return F

    def plot(self, tgt='', showChords=True):
        try:
            if not len(tgt):
                tgt = self.root + ' ' + self.scaleType
            from graphviz import Digraph
            fnColor = dict(T='darkslategray3',M='darkslategray3',SM='darkslategray3', D='darkolivegreen1',L='darkolivegreen1', SD='darksalmon', ST='darksalmon')
            g = Digraph('g', node_attr={'shape': 'Mrecord', 'height': '.1'}, engine='dot', format='png')
            g.attr(size='20')
            ok = []
            for n1 in self.fnSeq:
                for n2 in self.fnSeq[n1]:
                    if (str(n1), str(n2)) not in ok and n1 != n2:
                        if n1 in self.fnSeq[n2]:
                            g.edge(str(n1),str(n2), rank='same', dir='both', color='red')
                        else:
                            g.edge(str(n1), str(n2), rank='same')
                        ok.append((str(n1), str(n2)))
                        ok.append((str(n2), str(n1)))

            for n in self.fnTypes:
                if showChords:
                    g.node(str(n), label=self.degreesRoman[n-1] + '\\n' + ', '.join([_.name for _ in self.degrees[n]]),
                           color=fnColor.get(self.fnTypes[n], 'white'), style='filled')
                else:
                    g.node(str(n), label=self.degreesRoman[n-1] + '\\n' + ', '.join([str(_[0]) + ' ' + _[1] for _ in self.fnLst[n]]),
                           color=fnColor.get(self.fnTypes[n], 'white'), style='filled')

            g.render(filename=tgt)
        except ImportError:
            warnings.warn('graphviz needs to be installed to plot cadence graphs')


class Annotate():
    def __init__(self, chords):
        self.name = ''
        self.description = ''
        self.ann = pd.DataFrame(columns=['fn', 'deg', 'sca', 'cad'])
        if isinstance(chords, pd.DataFrame):
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
    def __init__(self, chords, model='majKostka'):
        Annotate.__init__(self, chords)
        self.name = 'Graph Method'
        self.description = 'We annotate first the longest sequences using a cadence graph'
        self.model = model

    def findCadencesInKey(self, key, model):
        """
        Returns possible cadences in self.chords using key
        Returns:
            list of cadences: (<size>,<start>,<key>,<cadenceList>)
        """
        ##
        keyCad = CadenceGraph(key, model)
        Seq = []
        cur = []  # [(<start>,<list>),...]

        for ci, c in enumerate(self.chords):
            if c in keyCad.chords:  # Current chord is in keyCad
                if len(cur):  # At least an ongoing cadence
                    newCur = []
                    for x in cur:
                        for d in keyCad.getDegree(c):
                            if d in keyCad.fnSeq[x[1][-1]]:  # The current chord can continue this sequence
                                newCur.append((x[0], x[1] + [d]))
                            else:  # A new sequence starts here
                                newCur.append((ci, [d]))
                    cur = newCur.copy()

                else:  # No cadence ongoing
                    cur = [(ci, [x]) for x in keyCad.getDegree(c)]

            else:  # current chord isnt in keyCad
                for x in cur:
                    Seq.append((len(x[1]), x[0], key + keyCad.scaleType, [keyCad.degreesRoman[xi-1] for xi in x[1]]))
                cur = []
        if cur:
            for x in cur:
                Seq.append((len(x[1]), x[0], key + keyCad.scaleType, [keyCad.degreesRoman[xi-1] for xi in x[1]]))

        ##
        return Seq

    def annotate(self, reduce=True):
        self.cleanup()
        # Find cadences in all keys
        X = []  # [(<size>,<start>,<key>,<cadence>),...]
        for key in Note.chrFlat:
            X.extend(self.findCadencesInKey(key, self.model))
        X.sort(key=lambda x: x[0], reverse=True)  # Sort by size

        used = [False] * len(self.chords)
        for x in X:
            if not reduce or not all(used[x[1]:(x[1] + x[0])]):  # All spots are unused
                for ci, c in enumerate(range(x[1], (x[1] + x[0]))):
                    # self.fn[c].append(CadenceGraph.fnTypes[x[3][ci]]) #todo: fix
                    self.deg[c].append(x[3][ci])
                    self.sca[c].append(x[2])
                    self.cad[c].append('-'.join(x[3]))
                    used[c] = True

        self.ann = pd.DataFrame(dict(fn=self.fn, deg=self.deg, sca=self.sca, cad=self.cad))





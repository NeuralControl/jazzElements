import pandas as pd
from matplotlib.pyplot import *

from jazzElements.chord import Chord
from jazzElements.note import Note
from jazzElements.scale import Scale

class CadenceGraph():
    cadGraphs = \
        {
            'kostkaMaj':
                {
                    'description': 'major chord progression from Tonal Harmony by Stefan Kostka',
                    'key': 'ion',
                    'next':
                        {
                            1: [1, 2, 3, 4, 5, 6, 7], 2: [2, 1, 5, 7], 3: [3, 2, 6, 4],
                            4: [4, 2, 5, 7, 1], 5: [5, 6, 7, 1], 6: [6, 2, 4], 7: [7, 6, 5, 1],
                        },
                },
            'kostkaMin':
                {
                    # todo: add bVII
                    'description': 'hminor chord progression from Tonal Harmony by Stefan Kostka',
                    'key': 'hm',
                    'next':
                        {
                            1: [1, 2, 3, 4, 5, 6, 7], 2: [2, 1, 5, 7], 3: [3, 2, 6, 5],
                            4: [4, 2, 5, 7, 1], 5: [5, 6, 7, 1], 6: [6, 2, 4], 7: [7, 6, 5, 1],
                        },
                },

            'allTransMaj':
                {
                    'description': 'allow all major transitions',
                    'key': 'ion',
                    'next': {x: np.arange(1, 8) for x in np.arange(1, 8)}
                },
            'allTransMin':
                {
                    'description': 'allow all harmonic minor transitions',
                    'key': 'hm',
                    'next': {x: np.arange(1, 8) for x in np.arange(1, 8)}
                },
            'mainCadMaj':
                {
                    'description': 'chord detector and main major cadences',
                    'key': 'ion',
                    'next': {1: [1], 2: [2, 5], 3: [3], 4: [4], 5: [5, 1], 6: [6], 7: [7]}
                },
            'mainCadMin':
                {
                    'description': 'chord detector and main minor cadences',
                    'key': 'hm',
                    'next': {1: [1], 2: [2, 5], 3: [3], 4: [4], 5: [5, 1], 6: [6], 7: [7]}
                },
        }

    def __init__(self, root, model):
        if model not in self.cadGraphs:
            raise ValueError(
                'scale type not implemented for cadence analysis (' + '|'.join(
                    [_ for _ in self.cadGraphs.keys()]) + ')')

        self.scale = Scale(root, self.cadGraphs[model]['key'])
        self.model = model
        self.fnSeq = self.cadGraphs[model]['next']  # -> Sequence
        self.degreesRoman = self.scale.degrees()
        self.degrees = {d + 1: self.scale.getDegreeFamily(d + 1) for d in range(len(self.degreesRoman))}
        self.chords = [Chord(chr) for chr in
                       set([item.name for sublist in [self.degrees[f] for f in self.degrees] for item in sublist])]

    def hasChord(self, chr):
        return chr in self.chords

    def getDegree(self, chr, strict=True):
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
                    if c.name == chr.name and f not in F:
                        F.append(f)
                else:
                    if c == chr and f not in F:
                        F.append(f)
        return F

    def findCadences(self, chords):
        """
        Returns possible cadences in chords
        Args:
            chords: chords to analyze
        Returns:
            list of cadences: (<size>,<start>,<key>,<cadenceList>)
        """

        Seq = []
        cur = []  # [(<start>,<list>),...]

        for ci, c in enumerate(chords):
            if c in self.chords:  # Current chord is in key of interest
                if len(cur):  # At least an ongoing cadence
                    newCur = []
                    for x in cur:
                        for d in self.getDegree(c, strict=True):
                            if d in self.fnSeq[x[1][-1]]:  # The current chord can continue this sequence
                                newCur.append((x[0], x[1] + [d]))
                            else:  # A new sequence starts here
                                Seq.append((len(x[1]), x[0], self.scale.name,
                                            [self.degreesRoman[xi - 1] for xi in x[1]]))  # store this cadence
                                newCur.append((ci, [d]))  # add new sequence

                    cur = newCur.copy()

                else:  # No cadence ongoing
                    cur = [(ci, [x]) for x in self.getDegree(c)]

            else:  # current chord isnt in key, append all current cadences to Seq
                for x in cur:
                    Seq.append((len(x[1]), x[0], self.scale.name, [self.degreesRoman[xi - 1] for xi in x[1]]))
                cur = []
        if cur:
            for x in cur:
                Seq.append((len(x[1]), x[0], self.scale.name, [self.degreesRoman[xi - 1] for xi in x[1]]))
        return Seq

    def plot(self, tgt='', showChords=True):
        try:
            if not len(tgt):
                tgt = 'CadenceGraph' + self.scale.name
            from graphviz import Digraph
            fnColor = dict(T='darkslategray3', M='darkslategray3', SM='darkslategray3', D='darkolivegreen1',
                           L='darkolivegreen1', SD='darksalmon', ST='darksalmon')
            g = Digraph('g', node_attr={'shape': 'Mrecord', 'height': '.1'}, engine='dot', format='png')
            g.attr(size='20')
            ok = []
            for n1 in self.fnSeq:
                for n2 in self.fnSeq[n1]:
                    if (str(n1), str(n2)) not in ok and n1 != n2:
                        if n1 in self.fnSeq[n2]:
                            g.edge(str(n1), str(n2), rank='same', dir='both', color='red')
                        else:
                            g.edge(str(n1), str(n2), rank='same')
                        ok.append((str(n1), str(n2)))
                        ok.append((str(n2), str(n1)))

            for n in Scale.fnTypes:
                if showChords:
                    g.node(str(n),
                           label=self.degreesRoman[n - 1] + '\\n' + ', '.join([_.name for _ in self.degrees[n]]),
                           color=fnColor.get(Scale.fnTypes[n], 'white'), style='filled')
                else:
                    g.node(str(n), label=self.degreesRoman[n - 1] + '\\n' + ', '.join(
                        [str(_[0]) + ' ' + _[1] for _ in self.fnLst[n]]),
                           color=fnColor.get(Scale.fnTypes[n], 'white'), style='filled')

            g.render(filename=tgt)
        except ImportError:
            warnings.warn('graphviz needs to be installed to plot cadence graphs')


class annGraph():
    def __init__(self, chords,model):
        self.name = ''
        self.description = ''
        self.model = model

        if isinstance(chords, pd.DataFrame):
            self.chords = [Chord(c) for c in chords['chr'].values]
        else:
            self.chords = [Chord(c) for c in chords]
        self.resetAnnotations()

    def resetAnnotations(self):
        fields = ['fn', 'deg', 'sca', 'cad', 'cadPos', 'chrPos']
        self.ann = pd.DataFrame([[[] for _ in range(len(fields))] for _ in range(len(self.chords))],
                                columns=fields,
                                index=range(len(self.chords)))

    def append(self, idx, values):
        """
        Helper to set an ann chord with fn, cad etc
        Args:
            idx: chord index
            values: dict
        """
        for x in ['deg','sca','fn','cad']:
            if x not in values:
                values[x]='?'

        for k in self.ann:
            if k in values:
                self.ann.loc[idx][k].append(values[k])
            else:
                self.ann.loc[idx][k].append(None)


    def run(self,model=None):
        if model:
            self.model = model

        self.resetAnnotations()
        if self.model == 'kostka':
            self.annKostka()
        elif self.model == 'allTrans':
            self.annAllTrans()
        elif self.model == 'mainCad':
            self.annMainCad()
        else:
            raise ValueError('annotation model unknown ({})'.format(self.model))

    def findCadences(self,cads,updateAnn=True):
        """
        Uses the graph models to find all cadences in a progression
        Args:
            cads: list of cadence graphs

        Returns:
            [(<size>,<start>,<key>,<cadence>),...]
        """
        X = []
        for cad in cads:
            for key in Note.chrFlat:
                if cad in CadenceGraph.cadGraphs:
                    X.extend(CadenceGraph(key, cad).findCadences(self.chords))
                else:
                    raise ValueError('cadence unknown ({})'.format(cad))
        X.sort(key=lambda x: x[0], reverse=True)  # Sort by size

        if updateAnn:
            used = [False] * len(self.chords)
            for x in X:  # x=(<size>,<start>,<key>,<cadenceList>)
                rnk = max([max(self.ann.loc[c]['cadPos']) if self.ann.loc[c]['cadPos'] else -1 for c in
                           range(x[1], (x[1] + x[0]))]) + 1
                for ci, c in enumerate(range(x[1], (x[1] + x[0]))):
                    self.append(c,
                                dict(deg=x[3][ci],
                                     sca=x[2],
                                     cad='-'.join(x[3]), cadPos=rnk,
                                     chrPos=ci,
                                     fn=Scale.fnTypes[Scale(x[2]).degrees().index(x[3][ci]) + 1] if len(
                                         x[3]) > 1 else ''
                                     ))
                    used[c] = True
        return X

    def annKostka(self):
        self.findCadences(['kostkaMaj','kostkaMin'])

    def annAllTrans(self):
        self.findCadences(['allTransMaj','allTransMin'])

    def annMainCad(self):
        self.findCadences(['mainCadMin','mainCadMaj'])


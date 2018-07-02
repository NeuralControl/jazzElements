import pandas as pd
from matplotlib.pyplot import *

from jazzElements.chord import Chord
from jazzElements.note import Note
from jazzElements.scale import Scale


def annIsolated(chords, curKey):
    iso = []
    for ci in range(len(chords)):
        # Current key
        if isinstance(curKey, str):
            key = curKey
        else:
            key = curKey[ci] if curKey is not None else None

        # Diatonic Chord
        if key:
            deg = Scale(key).hasChord(chords[ci])
            if deg:
                iso.append((ci, 'dia', deg, key))

        # Secondary Dominant
        if ci < len(chords) - 1 and chords[ci] in Scale(chords[ci + 1].root, 'ion').getDegreeFamily(5):
            iso.append((ci, 'V' + Chord(chords[ci]).type + '/'))

        # Borrowed relative major
        if key and isinstance(Scale(key).relativeMajor(), Scale):
            if Scale(key).relativeMajor().hasChord(chords[ci]):
                iso.append((ci, 'bor', 'relMaj', Scale(key).relativeMajor().name,
                            Scale(key).relativeMajor().hasChord(chords[ci])))

        # Borrowed relative minor
        if key and isinstance(Scale(key).relativeMinor(), Scale):
            if Scale(key).relativeMinor().hasChord(chords[ci]):
                iso.append((ci, 'bor', 'relMin', Scale(key).relativeMinor().name,
                            Scale(key).relativeMinor().hasChord(chords[ci])))

        # Borrowed parallel minor
        if key and isinstance(Scale(key).parallelMinor(), Scale):
            if Scale(key).parallelMinor().hasChord(chords[ci]):
                iso.append((ci, 'bor', 'parMin', Scale(key).parallelMinor().name,
                            Scale(key).parallelMinor().hasChord(chords[ci])))

        # Borrowed parallel major
        if key and isinstance(Scale(key).parallelMajor(), Scale):
            if Scale(key).parallelMajor().hasChord(chords[ci]):
                iso.append((ci, 'bor', 'parMaj', Scale(key).parallelMajor().name,
                            Scale(key).parallelMajor().hasChord(chords[ci])))

        # Tritone sub of the current chord
        tri = chords[ci].tritoneSubstitution()
        if key and tri and Scale(key).hasChord(tri):
            iso.append((ci, 'tri', tri))

        # Tritone of next chord
        if ci < (len(chords) - 1):
            tri = chords[ci + 1].tritoneSubstitution()
            if tri and tri == chords[ci]:
                iso.append((ci, 'tri>', tri))

        # 3 sub 1
        if key and chords[ci] in Scale(key).getDegreeFamily(3):
            iso.append((ci, '3sub1'))

        # #io sub VI
        if key and chords[ci] in [Chord((Scale(key).root + 1).name + 'o'),
                                  Chord((Scale(key).root + 1).name + 'o7')]:
            iso.append((ci, '#iosub6'))

        # Approach chord
        if ci < (len(chords) - 1) and min(Chord(chords[ci]).root - Chord(chords[ci + 1]).root,
                                          (Chord(chords[ci + 1]).root - Chord(chords[ci]).root)) in [1, 2]:
            iso.append((ci, 'app'))

    return iso


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
            'mainCadHmin':
                {
                    'description': 'chord detector and main harmonic minor cadences',
                    'key': 'hm',
                    'next': {1: [1], 2: [2, 5], 3: [3], 4: [4], 5: [5, 1], 6: [6], 7: [7]}
                },
            'mainCadMin':
                {
                    'description': 'chord detector and main aeolian cadences',
                    'key': 'aeo',
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


class Annotate():
    def __init__(self, chords, model):
        self.name = ''
        self.description = ''
        self.model = model

        if isinstance(chords, pd.DataFrame):
            self.chords = [Chord(c) for c in chords['chr'].values]
        else:
            self.chords = [Chord(c) for c in chords]
        self.resetAnnotations()

    def resetAnnotations(self):
        fields = ['fn', 'deg', 'sca', 'cad', 'chrPos', 'rnk']
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
        V = dict(deg='?', sca='?', fn='?', chrPos=0, cad='')
        V.update(values)

        if isinstance(V['cad'], list):  # We got a cadence here, find out the rank first
            rnk = max(max(self.ann.loc[idx:(idx - 1 + len(V['cad']))]['rnk'], default=-1), default=-1) + 1
            for chrPos in range(len(V['cad'])):
                self.ann.loc[idx + chrPos]['cad'].append('-'.join(V['cad']))
                self.ann.loc[idx + chrPos]['rnk'].append(rnk)
                self.ann.loc[idx + chrPos]['chrPos'].append(chrPos)
                self.ann.loc[idx + chrPos]['sca'].append(V['sca'])
                self.ann.loc[idx + chrPos]['fn'].append(V['cad'][chrPos])
                self.ann.loc[idx + chrPos]['deg'].append(V['cad'][chrPos])
        else:
            if 'rnk' not in V:
                V['rnk'] = max(self.ann.loc[idx]['rnk']) + 1 if len(self.ann.loc[idx]['rnk']) else 0

            for k in self.ann:
                if k in V:
                    self.ann.loc[idx][k].append(V[k])
                else:
                    self.ann.loc[idx][k].append(None)

    def run(self, model=None):
        if model:
            self.model = model

        self.resetAnnotations()
        if self.model == 'kostka':
            self.annKostka()
        elif self.model == 'allTrans':
            self.annAllTrans()
        elif self.model == 'mainCad':
            self.annMainCad()
        elif self.model == 'wtb':
            self.annWtb()
        else:
            raise ValueError('annotation model unknown ({})'.format(self.model))

    def findCadences(self, cadGraphs, updateAnn=True, minSz=0):
        """
        Uses the graph models to find all cadences in a progression
        Args:
            cadGraphs: list of cadence graphs
            minSz: minimum cadence size
        Returns:
            [(<size>,<start>,<key>,<cadence>),...]
        """
        cads = []
        for cad in cadGraphs:
            for key in Note.chrFlat:
                if cad in CadenceGraph.cadGraphs:
                    cads.extend(CadenceGraph(key, cad).findCadences(self.chords))
                else:
                    raise ValueError('cadence unknown ({})'.format(cad))
        cads.sort(key=lambda x: x[0], reverse=True)  # Sort by size
        cads = [x for x in cads if x[0] >= minSz]  # Remove short cadences

        if updateAnn:
            for c in cads:
                self.append(c[1], dict(sca=c[2], cad=c[3]))
        return cads

    def annKostka(self):
        self.resetAnnotations()
        self.findCadences(['kostkaMaj', 'kostkaMin'])

    def annAllTrans(self):
        self.resetAnnotations()
        self.findCadences(['allTransMaj', 'allTransMin'])

    def annMainCad(self):
        self.resetAnnotations()
        self.findCadences(['mainCadMin', 'mainCadMaj'])

    def annWtb(self):
        self.resetAnnotations()
        # Calculate minimum cadences
        cads = self.findCadences(['mainCadMaj','mainCadMin','mainCadHmin'], minSz=2)

        ## calculate current/next key
        K = pd.Series([None] * len(self.chords))
        for c in cads:
            K[c[1]:c[1] + c[0]] = c[2]
        curKey = K.fillna(method='ffill').values
        nextKey = K.fillna(method='bfill').values

        ## calculate isolated self.chords
        iso = [[] for _ in self.chords]
        for a in annIsolated(self.chords, curKey):  # Within the current key
            iso[a[0]].append(a[1:])
        for a in annIsolated(self.chords, nextKey):  # Within the next key
            if len(iso[a[0]]) == 0:
                iso[a[0]].append(a[1:])

        for ci in range(len(iso)):
            for x in [f for f in iso[ci] if f[0] == 'dia']:
                self.append(ci, dict(deg=x[1], sca=x[2], fn='~(dia)'))
            for x in [f for f in iso[ci] if f[0].endswith('/')]:
                self.append(ci, dict(fn='SD', deg=x[0][:-1], sca=curKey[ci + 1], cad='V/'))
            for x in [f for f in iso[ci] if f[0] == 'bor']:
                self.append(ci, dict(sca=x[2], fn='~(' + x[1] + ')', deg=x[3]))
            for x in [f for f in iso[ci] if f[0] == 'tri']:
                self.append(ci, dict(fn='~(tri)', deg='tri'))
            for x in [f for f in iso[ci] if f[0] == 'tri>']:
                self.append(ci, dict(fn='~(tri)>', deg='tri>'))
            for x in [f for f in iso[ci] if f[0] == '3sub1']:
                self.append(ci, dict(fn='~(3sub1)', deg='1'))
            for x in [f for f in iso[ci] if f[0] == '#iosub6']:
                self.append(ci, dict(fn='~(#iosub6)', deg='#iosub6'))
            for x in [f for f in iso[ci] if f[0] == 'app']:
                self.append(ci, dict(fn='~(app)', sca='', deg=''))





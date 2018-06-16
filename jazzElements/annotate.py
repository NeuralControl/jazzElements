import pandas as pd
from matplotlib.pyplot import *

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
                    'key': 'major',
                    'next':
                        {
                            1: [1, 2, 3, 4, 5, 6, 7], 2: [2, 1, 5, 7], 3: [3, 2, 6, 4], 4: [4, 2, 5, 7, 1],
                            5: [5, 6, 7, 1], 6: [6, 2, 4], 7: [7, 6, 5, 1],
                        },
                },
            'minKostka':
                {
                    # todo: add bVII
                    # todo: this one uses only the harmonic minor scale, should we do all three?
                    'description': 'minor chord progression from Tonal Harmony by Stefan Kostka',
                    'key': 'Hmin',
                    'next':
                        {
                            1: [1, 2, 3, 4, 5, 6, 7], 2: [2, 1, 5, 7], 3: [3, 2, 6, 5], 4: [4, 2, 5, 7, 1],
                            5: [5, 6, 7, 1], 6: [6, 2, 4], 7: [7, 6, 5, 1],
                        },
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

            for n in self.fnTypes:
                if showChords:
                    g.node(str(n),
                           label=self.degreesRoman[n - 1] + '\\n' + ', '.join([_.name for _ in self.degrees[n]]),
                           color=fnColor.get(self.fnTypes[n], 'white'), style='filled')
                else:
                    g.node(str(n), label=self.degreesRoman[n - 1] + '\\n' + ', '.join(
                        [str(_[0]) + ' ' + _[1] for _ in self.fnLst[n]]),
                           color=fnColor.get(self.fnTypes[n], 'white'), style='filled')

            g.render(filename=tgt)
        except ImportError:
            warnings.warn('graphviz needs to be installed to plot cadence graphs')


##
class Annotate():
    def __init__(self, chords, ann=None):
        fields = ['fn', 'deg', 'sca', 'cad', 'cadPos', 'chrPos']
        self.name = ''
        self.description = ''
        if isinstance(ann, pd.DataFrame):
            self.ann = ann
        else:
            self.ann = pd.DataFrame([[[] for _ in range(len(fields))] for _ in range(len(chords))],
                                    columns=fields,
                                    index=range(len(chords)))
        if isinstance(chords, pd.DataFrame):
            self.chords = [Chord(c) for c in chords['chr'].values]
        else:
            self.chords = [Chord(c) for c in chords]

    def append(self, idx, v):
        if isinstance(v, dict):
            for k in v:
                self.ann.loc[idx][k].append(v[k])
        else:
            warnings.warn('arg error')

    def run(self, reduce=True):
        """
        Fills self.ann with the annotations
        format: (<function>,<degree>,<scale>,<cadence>)
        """


class annWalkThatBass():
    def __init__(self, chords):
        Annotate.__init__(self, chords)
        self.name = 'Walk That Bass Method'
        self.description = ''

    def run(self):
        pass

    # def findCadences(self):
    #     def findSeqInLst(seq, lst):
    #         idx = []
    #         for i in range(len(lst) - len(seq) + 1):
    #             if np.array_equal(lst[i:i + len(seq)], seq):
    #                 idx.append((i, i + len(seq) - 1))
    #         return idx
    #
    #     lstCadences = ['3-6-2-5-1', '1-6-2-5-1', '6-2-5-1', '1-6-2-5', '2-5-1', '2-5', '5-1']
    #     chords = [c['chr'] for c in self.chords]
    #     cadLst = []
    #     idx = 0
    #     # Find all the possible known minor or major cadences:
    #     for root in Note.chrFlat:
    #         # for mode in Scale.modesLst:  # ['Ion', 'Aeo']:
    #         for mode in ['Ion', 'Aeo']:
    #             key = root + ' ' + mode
    #             keyChords = Scale(key).chords(3) + Scale(key).chords(4)
    #             keyDegrees = np.tile(np.arange(1, len(Scale(key).chordsRoman(3)) + 1), 2)
    #             # Diatonic annotation
    #             dia = np.array([keyDegrees[keyChords.index(c)] if Chord(c) in keyChords else None for c in chords])
    #
    #             # Find Cadences:
    #             for cadence in lstCadences:
    #                 seq = np.array([int(d) for d in cadence.split('-')])
    #                 for cad in findSeqInLst(seq, dia):
    #                     cadLst.append((cad, key, cadence))
    #                     idx += 1
    #
    #     # Sort cadences by length:
    #     cadLst = sorted(cadLst, key=lambda x: x[0][1] - x[0][0], reverse=True)
    #     # Remove cadences embedded in another:
    #     cadLstOk = []
    #     chrFree = np.array([True] * len(chords))
    #     for cad in cadLst:
    #         if any(chrFree[cad[0][0]:cad[0][1] + 1]):
    #             cadLstOk.append(cad)
    #             chrFree[cad[0][0]:cad[0][1] + 1] *= False
    #
    #     for cad in cadLstOk:
    #         for idx, c in enumerate(range(cad[0][0], cad[0][1] + 1)):
    #             for x in ['scale', 'fn', 'cadence', 'degree']:
    #                 if x not in self.chords[c]:
    #                     self.chords[c][x] = []
    #
    #             if len(self.chords[c]['cadence']) and max([x[1] for x in self.chords[c]['cadence']]) > idx:
    #                 self.chords[c]['cadence'].append((cad[2], idx))  # Last one is first
    #                 self.chords[c]['scale'].append(cad[1])
    #                 self.chords[c]['fn'].append(cad[2].split('-')[idx])  # todo: improve
    #                 self.chords[c]['degree'].append(Scale(cad[1]).hasChord(self.chords[c]['chr']))
    #
    #             else:
    #                 self.chords[c]['cadence'].insert(0, (cad[2], idx))  # This one is first
    #                 self.chords[c]['scale'].insert(0, cad[1])
    #                 self.chords[c]['fn'].insert(0, cad[2].split('-')[idx])  # todo: improve
    #                 self.chords[c]['degree'].insert(0, Scale(cad[1]).hasChord(self.chords[c]['chr']))
    #
    # def findIsolated(self):
    #     currentKey = []
    #
    #     mainKey = self.countKeys()[0][0] if self.countKeys() else []
    #
    #     for ci, c in enumerate(self.chords):
    #         if 'scale' in c:
    #             currentKey = c['scale'][0]
    #
    #         nextKey = [c.get('scale', [[]])[0] for c in self.chords[(ci + 1):]][0] if ci < len(self.chords) - 1 else []
    #
    #         for k in [currentKey, nextKey, mainKey]:
    #
    #             # Searching if the chord is diatonic
    #             if 'fn' not in self.chords[ci] and k != []:
    #                 deg = Scale(k).hasChord(c['chr'])
    #                 if deg:
    #                     self.chords[ci]['scale'] = [k]
    #                     self.chords[ci]['degree'] = [deg]
    #                     self.chords[ci]['fn'] = ['~']
    #
    #             # Searching if the chord is a substitution in currentKey,nextKey,mainKey
    #             if 'fn' not in self.chords[ci] and k != []:
    #                 subs = Scale(k).possibleSubstitutions(asStr=True)
    #                 s = [[s[0][0], s[2]] for s in subs if len(s[1]) == 1 and Chord(s[1][0]) == c['chr']]
    #
    #                 if len(s) == 1:
    #                     self.chords[ci]['scale'] = [k]
    #                     self.chords[ci]['fn'] = [s[0][1]]
    #                     self.chords[ci]['degree'] = [Scale(k).hasChord(Chord(s[0][0]))]
    #                 elif len(s) > 1:
    #                     raise ValueError(
    #                         'Found multiple substitutions at bar ' + str(c['bar']) + ' ' + c['chr'])


class annGraph(Annotate):
    def __init__(self, chords):
        Annotate.__init__(self, chords)
        self.name = 'Graph Method'
        self.description = 'We annotate first the longest sequences using a cadence graph'

    def findCadencesInKey(self, key, model):
        """
        Returns possible cadences in self.chords using key
        Returns:
            list of cadences: (<size>,<start>,<key>,<cadenceList>)
        """

        keyCad = CadenceGraph(key, model)
        Seq = []
        cur = []  # [(<start>,<list>),...]

        for ci, c in enumerate(self.chords):
            if c in keyCad.chords:  # Current chord is in key of interest
                if len(cur):  # At least an ongoing cadence
                    newCur = []
                    for x in cur:
                        for d in keyCad.getDegree(c, strict=True):
                            if d in keyCad.fnSeq[x[1][-1]]:  # The current chord can continue this sequence
                                newCur.append((x[0], x[1] + [d]))
                            else:  # A new sequence starts here
                                Seq.append((len(x[1]), x[0], keyCad.scale.name,
                                            [keyCad.degreesRoman[xi - 1] for xi in x[1]]))  # store this cadence
                                newCur.append((ci, [d]))  # add new sequence

                    cur = newCur.copy()

                else:  # No cadence ongoing
                    cur = [(ci, [x]) for x in keyCad.getDegree(c)]

            else:  # current chord isnt in key, append all current cadences to Seq
                for x in cur:
                    Seq.append((len(x[1]), x[0], keyCad.scale.name, [keyCad.degreesRoman[xi - 1] for xi in x[1]]))
                cur = []
        if cur:
            for x in cur:
                Seq.append((len(x[1]), x[0], keyCad.scale.name, [keyCad.degreesRoman[xi - 1] for xi in x[1]]))
        return Seq

    def annotate(self):
        # Find cadences in all keys
        X = []  # [(<size>,<start>,<key>,<cadence>),...]
        for key in Note.chrFlat:
            X.extend(self.findCadencesInKey(key, 'minKostka'))
        for key in Note.chrFlat:
            X.extend(self.findCadencesInKey(key, 'majKostka'))

        X.sort(key=lambda x: x[0], reverse=True)  # Sort by size

        used = [False] * len(self.chords)
        for x in X:  # x=(<size>,<start>,<key>,<cadenceList>)
            rnk = max([max(self.ann.loc[c]['cadPos']) if self.ann.loc[c]['cadPos'] else -1 for c in range(x[1], (x[1] + x[0]))])+1
            # todo rank bug, e.g. myromance chord 2, two cadences have the same rank
            for ci, c in enumerate(range(x[1], (x[1] + x[0]))):
                self.append(c,
                            dict(deg    = x[3][ci],
                                 sca=x[2],
                                 cad    = '-'.join(x[3]), cadPos=rnk,
                                 chrPos = ci,
                                 fn     = Scale.fnTypes[Scale(x[2]).degrees().index(x[3][ci]) + 1]
                                 ))
                used[c] = True

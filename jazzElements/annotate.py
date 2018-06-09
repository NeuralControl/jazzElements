import warnings
import pandas as pd
from jazzElements.chord import Chord
from jazzElements.note import Note
from jazzElements.scale import Scale
from matplotlib.pyplot import *


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
                    'key': 'harMin',
                    'next':
                        {
                            1: [1, 2, 3, 4, 5, 6, 7], 2: [2, 1, 5, 7], 3: [3, 2, 6, 5], 4: [4, 2, 5, 7, 1],
                            5: [5, 6, 7, 1], 6: [6, 2, 4], 7: [7, 6, 5, 1],
                        },
                },
        }

    def __init__(self, root, model='majKostka'):
        if model not in self.cadGraphs:
            raise ValueError(
                'scale type not implemented for cadence analysis (' + '|'.join(
                    [_ for _ in self.cadGraphs.keys()]) + ')')

        self.scale = Scale(root, self.cadGraphs[model]['key'])
        self.model = model
        self.fnSeq = self.cadGraphs[model]['next']  # -> Sequence
        self.fnTypes = {1: 'T', 2: 'ST', 3: 'M', 4: 'SD', 5: 'D', 6: 'SM', 7: 'L'}  # todo: can types be generic or moved to scale?
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

class Annotate():
    def __init__(self, chords):
        self.name = ''
        self.description = ''
        self.ann = pd.DataFrame(columns=['fn', 'deg', 'sca', 'cad'])
        if isinstance(chords, pd.DataFrame):
            self.chords = [Chord(c) for c in chords['chr'].values]
        else:
            self.chords = [Chord(c) for c in chords]

    def run(self, reduce=True):
        """
        Fills self.ann with the annotations
        format: (<function>,<degree>,<scale>,<cadence>)
        """

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

        keyCad = CadenceGraph(key, model)
        Seq = []
        cur = []  # [(<start>,<list>),...]

        for ci, c in enumerate(self.chords):
            if c in keyCad.chords:  # Current chord is in key of interest
                if len(cur):  # At least an ongoing cadence
                    newCur = []
                    for x in cur:
                        for d in keyCad.getDegree(c,strict=True):
                            if d in keyCad.fnSeq[x[1][-1]]:  # The current chord can continue this sequence
                                newCur.append((x[0], x[1] + [d]))
                            else:  # A new sequence starts here
                                Seq.append((len(x[1]), x[0], keyCad.scale.name,
                                             [keyCad.degreesRoman[xi - 1] for xi in x[1]])) # store this cadence
                                newCur.append((ci, [d])) # add new sequence

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

    def annotate(self, reduce=True):
        fn = [[] for c in self.chords]
        deg = [[] for c in self.chords]
        sca = [[] for c in self.chords]
        cad = [[] for c in self.chords]
        rank=[[] for c in self.chords]
        pos=[[] for c in self.chords]

        # Find cadences in all keys
        X = []  # [(<size>,<start>,<key>,<cadence>),...]
        for key in Note.chrFlat:
            X.extend(self.findCadencesInKey(key, self.model))
        X.sort(key=lambda x: x[0], reverse=True)  # Sort by size

        used = [False] * len(self.chords)
        for x in X:
            if not reduce or not all(used[x[1]:(x[1] + x[0])]):  # All spots are unused
                rnk=max([len(sca[c]) for c in range(x[1], (x[1] + x[0]))])

                for ci, c in enumerate(range(x[1], (x[1] + x[0]))):
                    # self.fn[c].append(CadenceGraph.fnTypes[x[3][ci]]) #todo: fix
                    deg[c].append(x[3][ci])
                    sca[c].append(x[2])
                    cad[c].append('-'.join(x[3]))
                    used[c] = True
                    rank[c].append(rnk)
                    pos[c].append(ci)
        self.ann = pd.DataFrame(dict(fn=fn, deg=deg, sca=sca, cad=cad,cadPos=rank,chrPos=pos))




    def plot(self):
        figure()
        chrSpcX=100
        cadSpcY=5
        chrSpcY=cadSpcY*(max([max(p) for p in self.ann.cadPos if len(p)])+1)+2*cadSpcY
        chrPerRow=16

        def chrPos(ci):
            return (ci%chrPerRow)*chrSpcX,-((ci)//chrPerRow)*chrSpcY

        cad = []
        for idx,r in self.ann.iterrows():
            for i in range(len(r['cad'])):
                if r['chrPos'][i]==0:
                    cad.append((idx,
                                idx+len( r['cad'][i].split('-'))-1,
                                r['chrPos'][i],
                                r['cadPos'][i],
                                r['cad'][i],
                                         r['sca'][i] )  )
        # cad = [<start>,<stop>,<chrPos>,<cadPos>,<cadence>,<scale> ]


        for ci,chr in enumerate(self.chords): #todo: add duration to chord?
            text(chrPos(ci)[0],chrPos(ci)[1],chr.name,va='bottom',ha='center',fontweight='bold',fontSize=9)
        for c in cad:
            text(chrPos(c[0])[0]-chrSpcX/2,-cadSpcY+chrPos(c[0])[1]-c[3]*cadSpcY,c[5].replace(' Ion','M')+': '+c[4],fontSize=8,ha='left',va='bottom')
            if c[1]>c[0]:
                arrow(chrPos(c[0])[0]-chrSpcX/2,-cadSpcY+chrPos(c[0])[1]-c[3]*cadSpcY,(len(c[4].split('-'))-.5)*chrSpcX,0,
                      shape='right',width=5,head_width=10,alpha=.3,edgecolor='w')

        xlim(-50,chrSpcX*chrPerRow+50)
        ylim(chrPos(len(self.chords))[1]-100,0)

        axis('off');box('off')

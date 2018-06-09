import re

import pandas as pd
from matplotlib import patches
from matplotlib.pyplot import *

from jazzElements.annotate import annGraph
from jazzElements.chord import Chord
from jazzElements.note import Note
from jazzElements.scale import Scale

progressions = \
    {
        'Satin Doll': '|Dm7,G7|%|Em7,A7|%|Am7,D7|Abm7,Db7|CM7|%|',

        'Misty': '|Fm7,Bb7|EbM7|Bbm7,Eb7|AbM7|Abm7,Db7|EbM7,Cm7|Fm7,Bb7|Gm7,C7|Fm7,Bb7'
                         '|EbM7|Bbm7,Eb7|AbM7|Abm7,Db7|EbM7,Cm7|Fm7,Bb7|EbM7#5,Ab7|EbM7,Do7,G7alt,Cm7,Bm7'
                 '|Bbm7|Eb7b9|AbM7|%'
                 '|Am7|D7,F67|Gm7b5|C7b9|Fm7,Bb7'
                 '|EbM7|Bbm7,Eb7|AbM7|Abm7,Db7|EbM7,Cm7|Fm7,Bb7|Gm7,C7|Fm7,Bb7|Eb6|Fm7,Bb7|',

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

        'Giant Steps': '|DbM7,E9|AM7,C9|FM7|Bm9,E9|AM7,C9|FM7,Ab9|DbM7|Gm9,C9|FM9|Bm9,E9|AM7|Ebm7,Ab9|DbM7|Gm9,C9|FM7|Ebm7,Ab9|',

        'unitTest 2-5-1 to 6-2-5-1':
            '|Dm7|Dm7|Eø|Am7|Dm7|G7|CM7|CM7|',

    }


class Progression:
    def __init__(self, prg, name=''):
        # todo: chords are now of equal duration within a bar.

        self.cfg = \
            {
                'colors': ['#c0d6e4', '#afeeee', '#dddddd', '#ffb6c1', '#e6e6fa', '#f5f5dc', '#ccff00', '#31698a',
                           '#f08080', '#ffa500', '#008080'] * 2,
                'barsPerRow': 4,
                'sepx': 0,
                'sepy': 20,
                'beatsPerBar':4,

            }

        self.name = name

        if '|' not in prg:
            self.name = prg
            prg = progressions[prg]

        chords = []
        for bi, bar in enumerate(prg.strip('|').split('|')):
            if len(bar):
                for c in bar.split(','):
                    if c == '%':
                        chr = [bi, chords[-1][1], self.cfg['beatsPerBar'] / len(bar.split(','))]

                    else:
                        chr = [bi, c, self.cfg['beatsPerBar'] / len(bar.split(','))]
                    chords.append(chr)

        self.chords = pd.DataFrame(chords, columns=['bar', 'chr', 'beats'])
        self.nbBars = self.chords['bar'].max() + 1
        self.ann = None

    def findScale(self, chr, degree):
        # todo: There must be a better way
        # todo: Only looking for major keys
        # todo: Taking now the first one found
        mode = 'Ion'
        return [[Scale(k, mode), Scale(k, mode).hasChord(chr)] for k in Note.chrSharp if
                Scale(k, mode).getDegree(degree) == chr]

    def print(self):
        lastBar = -1
        print('{:4}|{:7}|{:5}|{:10}|{:12}|{:12}'.format(
            'Bar', 'Chord', 'Fn', 'Degree', 'Scale', 'Cadence'))
        # todo: will crash if no annotation

        for ci, c in pd.concat([self.chords, self.ann.ann], 1).iterrows():
            print('{:4}|{:7}|{:5}|{:10}|{:12}|{:12}'.format(
                str(c['bar'] + 1) if c['bar'] != lastBar else '',
                c['chr'],
                ','.join(c['fn']) if 'fn' in c else '',
                ','.join(c['deg']) if 'deg' in c else '',
                ','.join(c['sca']) if 'sca' in c else '',
                ','.join(c['cad']) if 'cad' in c else '',
            ))
            lastBar = c['bar']

    def plotChord(self, ax, chr, pos, plotType='fn'):
        chord = self.chords.loc[chr]
        ann = self.ann.ann.loc[chr] if self.ann else None

        xChr, yChr, wChr, hChr = pos
        bgd = patches.Rectangle((xChr, yChr), wChr, hChr, fill=False, clip_on=False, color='k')
        ax.add_patch(bgd)

        # Function
        if plotType == 'fn':
            root, alt, chrType = re.search(Chord.regexChord, chord['chr']).groups()
            text(xChr + wChr / 2, yChr + hChr, '{}{}$^{{{}}}$ '.format(root, alt, chrType.replace('#', '+')),
                 va='top', ha='center', fontSize=10,
                 bbox=dict(boxstyle='round4', fc='w'), weight=1000)
            cadh = 15
            if 'sca' in ann:
                for si, s in enumerate(ann['sca']):
                    if len(s):
                        bgd = patches.Rectangle((xChr, yChr + si * cadh), wChr, cadh, fill=True, clip_on=False,
                                                color=self.cfg['scaleColors'][s], alpha=1, ec='k')
                        ax.add_patch(bgd)

                        if chr == 0 or s not in self.chords.loc[chr - 1].get('sca', []):
                            text(xChr + 2, yChr + cadh / 2 + si * cadh, s,
                                 color='k', va='center',
                                 ha='left', fontSize=10, weight='bold')

            if 'deg' in ann:
                for di, d in enumerate(ann['deg']):
                    text(xChr + wChr, yChr + cadh / 2 + di * cadh - 1, d, color='k',
                         va='center', ha='right', fontSize=10, weight='bold')

            if 'cad' in ann:
                for ci, c in enumerate(ann['cad']):
                    if chr == 0 or c[0] not in [x[0] for x in self.ann.ann.loc[chr - 1].get('cad', [])]:
                        text(xChr + wChr / 2, yChr + ci * cadh + cadh / 2, c, color='k', va='center', ha='center',
                             fontSize=10, weight='bold')
                    else:
                        if len(c) > 1 and c[1] == len(c[0].split('-')) - 1:
                            arrow(xChr + 50, yChr + ci * cadh + cadh / 2, wChr - 100, 0, head_width=15, head_length=20,
                                  fc='k', lw=1)

                        else:
                            arrow(xChr + 50, yChr + ci * cadh + cadh / 2, wChr - 100 - 20, 0, head_width=0,
                                  head_length=20, fc='k', lw=1)
            else:
                if 'fn' in ann:
                    text(xChr + wChr / 2, yChr + cadh / 2, '/'.join(ann['fn']), color='k', va='center',
                         ha='center',
                         fontSize=10, weight='bold')

        if plotType == 'kbd':
            root, alt, chrType = re.search(Chord.regexChord, chord['chr']).groups()
            wBeat = wChr / chord['beats']
            for beat in range(int(np.ceil(chord['beats']))):
                if beat == 0:
                    text(xChr + beat * wBeat + wBeat / 2,
                         yChr + hChr - 20,
                         '{}{}$^{{{}}}$ '.format(root, alt, chrType.replace('#', '+')),
                         va='center', ha='center', fontSize=10, bbox=dict(boxstyle='round4', fc='skyblue'), weight=1000)
                else:
                    text(xChr + beat * wBeat + wBeat / 2,
                         yChr + hChr - 20, '%',
                         va='center', ha='center', fontSize=10, weight=1000)

            Chord(chord['chr']).plot(ax=ax,
                                     pos=[xChr + 5, yChr + 10 + (hChr - 50) / 2, min(wChr - 10, 100),
                                          (hChr - 50) / 2],
                                     nbOctaves=1, showName=False)

            if 'sca' in ann and len(ann['sca']):
                Scale(ann['sca'][0]).plot(ax=ax, pos=[xChr + 5, yChr + 5, min(wChr - 10, 100), (hChr - 50) / 2],
                                          nbOctaves=1,
                                          showName=False)

    def plotBar(self, b, pos, plotType='fn'):
        xBar, yBar, wBar, hBar = pos
        wBeat = (wBar - self.cfg['sepx'] * (len(self.chords['bar'] == b) - 1)) / self.cfg['beatsPerBar']
        nBeats = 0
        ax = gca()
        for ic, c in self.chords[self.chords['bar'] == b].iterrows():
            posChr = [xBar + wBeat * nBeats + self.cfg['sepx'] * (ic), yBar, c['beats'] * wBeat, hBar]
            self.plotChord(ax, ic, posChr, plotType=plotType)
            nBeats += c['beats']
            if nBeats >= self.cfg['barsPerRow'] * self.cfg['beatsPerBar']:
                nBeats = 0
                yBar -= (hBar + self.cfg['sepy'])

        # Plot Bar
        plot([xBar - self.cfg['sepx'] / 2, xBar - self.cfg['sepx'] / 2], [yBar, yBar + hBar], color='k', lw=3)
        text(xBar - self.cfg['sepx'] / 2, yBar + hBar, '{:02}'.format(b + 1), color='w', va='top', ha='center', fontSize=8,
             weight=1000,
             bbox=dict(boxstyle='round4', fc='k'))

    def countKeys(self):
        if 'sca' in self.ann.ann:
            s = [val for sublist in self.ann.ann.sca for val in sublist]
            s = [(x, s.count(x)) for x in set(s)]
            s.sort(key=lambda s: s[1], reverse=True)
            return s
        else:
            return []

    def plot(self, plotType='fn'):
        # todo: Scaling issues
        self.cfg['scaleColors'] = {x[0]: self.cfg['colors'][i] for i, x in enumerate(self.countKeys())}

        nbRows = np.ceil(self.nbBars / self.cfg['barsPerRow'])
        wBar, hBar = 400, 150
        h = nbRows * hBar
        x, y = [0, 0]
        fig = figure(figsize=(16, nbRows))
        fig.subplots_adjust(left=0, right=1, bottom=0, top=.9)

        for b in self.chords['bar'].unique():
            posBar = [x + (b % self.cfg['barsPerRow']) * (wBar + self.cfg['sepy']),
                      y + h - hBar * (1 + (b // self.cfg['barsPerRow'])) - self.cfg['sepy'] * (
                      (b // self.cfg['barsPerRow'])), wBar, hBar]
            self.plotBar(b, posBar, plotType=plotType)

        # axis('tight')
        axis('off')
        suptitle(self.name, size=20, weight='bold')
        # axis('equal')

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

    def annotate(self, method='graph',model='majKostka', reduce=True):
        if method == 'graph':
            self.ann = annGraph(self.chords,model)
        else:
            warnings.warn('not implemented')

        self.ann.annotate(reduce=reduce)

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


prg=Progression('My Romance')
prg.annotate(method='graph',model='majKostka',reduce=False)

self=annGraph(prg.chords)
self.annotate(reduce=False)
self.plot()
#
# prg=Progression('unitTest 2-5-1 to 6-2-5-1')
# prg.annotate(method='graph',model='minKostka')
# prg.plot()

# prg=Progression('My Romance')
# prg.annotate(method='graph',model='majKostka',reduce=False)
# prg.plot()

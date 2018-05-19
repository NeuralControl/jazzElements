from jazzElements.base import *

self = Progression('All The Things You Are')


def findSeqInLst(seq, lst):
    idx = []
    for i in range(len(lst) - len(seq) + 1):
        if np.array_equal(lst[i:i + len(seq)],seq):
            idx.append((i, i + len(seq) - 1))
    return idx


lstCadences = ['3-6-2-5-1', '2-5-1', '2-5', '5-1']
chords = [c['chord'] for c in self.chords]
dia = {}
fn = {}
cadences = []
for root in Note.chrFlat:
    for mode in ['Ion', 'Aeo']:
        key = root + ' ' + mode
        keyChords = Scale(key).chords(3) + Scale(key).chords(4)
        keyDegrees = np.tile(np.arange(1, len(Scale(key).chordsRoman(3)) + 1), 2)

        # Diatonic annotation
        dia[key] = np.array([keyDegrees[keyChords.index(c)] if c in keyChords else None for c in chords])

        # Find Cadences:
        for cadence in lstCadences:
            seq = np.array([int(d) for d in cadence.split('-')])
            cadLst = findSeqInLst(seq, dia[key])
            for cad in cadLst:
                #dia[key][cad[0]:cad[1] + 1]*=-1
                cadences.append((key, cad, cadence))
                for c in np.arange(cad[0],cad[1]+1):
                    self.chords[c]['scale']=Scale(key)
                    self.chords[c]['function']=cadence


self.print()
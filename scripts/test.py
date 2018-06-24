import pandas as pd

from jazzElements.annotate import annGraph
from jazzElements.chord import Chord
from jazzElements.progression import Progression
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
            if Scale(key).relativeMajor().hasChord(key):
                iso.append((ci, 'bor', 'relMaj', Scale(key).relativeMajor().name))

        # Borrowed relative minor
        if key and isinstance(Scale(key).relativeMinor(), Scale):
            if Scale(key).relativeMinor().hasChord(chords[ci]):
                iso.append((ci, 'bor', 'relMin', Scale(key).relativeMinor().name))

        # Borrowed parallel minor
        if key and isinstance(Scale(key).parallelMinor(), Scale):
            if Scale(key).parallelMinor().hasChord(chords[ci]):
                iso.append((ci, 'bor', 'parMin', Scale(key).parallelMinor().name))

        # Borrowed parallel major
        if key and isinstance(Scale(key).parallelMajor(), Scale):
            if Scale(key).parallelMajor().hasChord(chords[ci]):
                iso.append((ci, 'bor', 'parMaj', Scale(key).parallelMajor().name))

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


def findCurrentNextKeys(cad, sca, chrPos):
    Key = []
    for ci in range(len(cad)):
        key = None
        for pi, pos in enumerate(chrPos[ci]):
            if pos == 2:
                key = sca[ci][pi]
        Key.append(key)
    K = pd.DataFrame(dict(lastKey=Key, nextKey=Key))
    K['lastKey'].fillna(method='ffill', inplace=True)
    K['nextKey'].fillna(method='bfill', inplace=True)
    return K['lastKey'].values, K['nextKey'].values


## Analysis:
chrStr = '|Dm7|G7|CM7|Cmaj7|C#dim7|Dm7|G7|'
# Base
prg = Progression('My Romance')
# prg.annotate(model='mainCad')
# prg.ann.ann['chords'] = prg.ann.chords
# ann = prg.ann.ann
# curKey, nextKey = findCurrentNextKeys(ann['cad'], ann['sca'], ann['chrPos'])


## First we find the basic cadences
# todo:  we may not need to do find cadences for this one, maybe look for chord quality sequence...
prg.ann = annGraph(prg.chords['chr'].values, 'mainCad')
cads = prg.ann.findCadences(['mainCadMin', 'mainCadMaj'], updateAnn=False)
cads = [x for x in cads if x[0] >= 2]
chords = prg.ann.chords
## calculate current/next key
K = pd.Series([None] * len(chords))
for c in cads:
    K[c[1]:c[1] + c[0]] = c[2]
curKey = K.fillna(method='ffill').values
nextKey = K.fillna(method='bfill').values

##
iso = [[] for _ in chords]
for a in annIsolated(chords, curKey):
    iso[a[0]].append(a[1:])
for a in annIsolated(chords, nextKey):
    iso[a[0]].append(a[1:])

C = [[] for _ in chords]
for c in cads:
    for ci in range(c[0]):
        C[c[1] + ci].append(('-'.join(c[3]), c[2], ci))

## REDUCE
prg.ann.resetAnnotations()

for ci in range(len(chords)):
    if len(C[ci]):
        for cad in C[ci]:
            prg.ann.append(ci, dict(cad=cad[0], sca=cad[1], chrPos=cad[2],
                                    deg=cad[0].split('-')[cad[2]], cadPos=len(prg.ann.ann['cadPos'][ci]),
                                    fn=cad[0].split('-')[cad[2]]+'?'))
    else:
        # 3sub1 #iosub6 app
        for x in [f for f in iso[ci] if f[0] == 'dia']:
            prg.ann.append(ci,
                           dict(deg=x[1], sca=x[2], fn='~', chrPos=0, cadPos=len(prg.ann.ann['cadPos'][ci])))
        for x in [f for f in iso[ci] if f[0].endswith('/')]:
            prg.ann.append(ci, dict(fn='SD', deg=x[0][:-1], sca=curKey[ci + 1], cad='V/',
                                    cadPos=len(prg.ann.ann['cadPos'][ci])))
        for x in [f for f in iso[ci] if f[0] == 'bor']:
            prg.ann.append(ci, dict(sca=x[2], fn=x[0], cad=x[1], cadPos=len(prg.ann.ann['cadPos'][ci])))
        for x in [f for f in iso[ci] if f[0] == 'tri']:
            prg.ann.append(ci, dict(fn='~', deg='TRI TODO', cadPos=len(prg.ann.ann['cadPos'][ci])))  # todo
        for x in [f for f in iso[ci] if f[0] == 'tri>']:
            prg.ann.append(ci, dict(fn='~', deg='TRI> TODO', cadPos=len(prg.ann.ann['cadPos'][ci])))  # todo
        for x in [f for f in iso[ci] if f[0] == '3sub1']:
            prg.ann.append(ci, dict(fn='~', deg='3sub1 TODO', cadPos=len(prg.ann.ann['cadPos'][ci])))  # todo
        for x in [f for f in iso[ci] if f[0] == '3sub1']:
            prg.ann.append(ci, dict(fn='~', deg='3sub1 TODO', cadPos=len(prg.ann.ann['cadPos'][ci])))  # todo
        for x in [f for f in iso[ci] if f[0] == '#iosub6']:
            prg.ann.append(ci, dict(fn='~', deg='#iosub6 TODO', cadPos=len(prg.ann.ann['cadPos'][ci])))  # todo
        for x in [f for f in iso[ci] if f[0] == 'app']:
            prg.ann.append(ci, dict(fn='~', deg='app TODO', cadPos=len(prg.ann.ann['cadPos'][ci])))  # todo

print(prg.ann.ann)
prg.plot()

from jazzElements.base import Progression
from jazzElements.scale import Scale
from jazzElements.chord import Chord
from jazzElements.note import Note


def test_basics():
    assert [Chord(c['chord']).root for c in Progression(''.join(['|{}m7'.format(k) for k in Note.chrFlat])+'|').chords]==Note.chrFlat
    assert Progression('|Cm7|%|').chords == Progression('|Cm7|Cm7|').chords
    assert Progression('|Cm7,%|').chords == Progression('|Cm7,Cm7|').chords

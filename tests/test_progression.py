from jazzElements.base import Note, Chord, Scale,Progression


def test_basics():
    assert [c['chord'].root for c in Progression(''.join(['|{}m7'.format(k) for k in Note.chrFlat])+'|').chords]==Note.chrFlat
    assert Progression('|Cm7|%|').chords == Progression('|Cm7|Cm7|').chords
    assert Progression('|Cm7,%|').chords == Progression('|Cm7,Cm7|').chords

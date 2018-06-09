from jazzElements.progression import Progression
from jazzElements.chord import Chord
from jazzElements.note import Note


def test_basics():
    assert [Chord(c).root for c in Progression(''.join(['|{}m7'.format(k) for k in Note.chrFlat])+'|').chords['chr']]==Note.chrFlat
    assert all(Progression('|Cm7|%|').chords['chr'].values == Progression('|Cm7|Cm7|').chords['chr'].values)
    assert all(Progression('|Cm7,%|').chords['chr'].values == Progression('|Cm7,Cm7|').chords['chr'].values)

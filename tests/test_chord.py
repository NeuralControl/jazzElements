from jazzElements.base import Note, Chord, Scale

def test_fromName():
    assert Chord('Cm7') == Chord('EbM6')
    assert Chord('Cm7') == 'EbM6'
    assert not Chord('Cm') == 'Cm7'
    assert not 'Cm7' == Chord('Cm')

def test_fromNotes():
    assert Chord('C').notes() == ['C', Note('E'), 'G']
    from itertools import permutations
    for lst in list(permutations(['C', 'Eb', 'G', 'Bb'], 4)):
        assert (Chord(lst).name in ['Cm7','E♭6'])


def test_guideAndAvoid():
    assert Chord('Dm7').guideTones() == ['F', 'C']
    assert Chord('G7').guideTones() == ['B', 'F']
    assert Chord('CM7').guideTones() == ['E', 'B']
    assert Chord('Cm7').avoidNotes(Scale('C Ion')) == ['E', 'B']
    assert Chord('Cm7').avoidNotes(Note.chrFlat) == ['D♭', 'E', 'A♭', 'B']

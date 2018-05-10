#
#

from jazzTheory.jazzTheory.base import Note, Chord, Scale


def test_Note():
    for note in Note.chrSharp + Note.chrFlat:
        assert Note(note) == note
        assert Note(note).name == note
        assert Note(note) + 12 == note
        assert Note(note) - 12 == note
        assert Note(note + '#b#b#b') == Note(note)

    # Alterations
    assert Note('C♯#') == Note('D')
    assert Note('C##') == 'D'
    assert str(Note('C♯♯')) == 'D'
    assert Note('Dbb') == Note('C')
    assert Note('C##♯♯') == Note('E')
    assert Note('C###').name == 'D♯'
    assert Note('Fbb').name == 'E♭'

    # We want to keep alterations
    assert [Note('C') - alt for alt in range(15)] == \
           ['C', 'B', 'B♭', 'A', 'A♭', 'G', 'G♭', 'F', 'E', 'E♭', 'D', 'D♭', 'C', 'B', 'B♭']
    assert [Note('C') + alt for alt in range(15)] == \
           ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B', 'C', 'C♯', 'D']

    # Notes relationship
    assert Note('C') - Note('D') == 10
    assert Note('D') - Note('C') == 2
    assert Note('B') - Note('C') == 11
    assert Note('C') - Note('B') == 1
    assert Note('C') - Note('C') == 0
    assert Note('G') - Note('C') == 7
    assert Note('C') - Note('G') == 5

    assert Note('A#') == Note('Bb')
    assert Note(Note('C')) == 'C'


def test_Chord():
    assert Chord('C').notes() == ['C', Note('E'), 'G']
    assert Chord('Cm7') == Chord('EbM6')
    assert Chord('Cm7') == 'EbM6'
    assert not Chord('Cm') == 'Cm7'
    assert not 'Cm7' == Chord('Cm')

    from itertools import permutations
    for lst in list(permutations(['C', 'Eb', 'G', 'Bb'], 4)):
        assert (Chord(lst).name == 'Cm7')

    # Guide tones and avoid notes
    assert Chord('Dm7').guideTones() == ['F', 'C']
    assert Chord('G7').guideTones() == ['B', 'F']
    assert Chord('CM7').guideTones() == ['E', 'B']
    assert Chord('Cm7').avoidNotes(Scale('C', 'Ionian')) == ['E', 'B']
    assert Chord('Cm7').avoidNotes(Note.chrFlat) == ['D♭', 'E', 'A♭', 'B']

def test_Scale():
    assert Scale('C ionian').notes() == ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    assert Scale('C ionian').chords(asStr=True) == {'I': 'CM7', 'II': 'Dm7', 'III': 'Em7', 'IV': 'FM7',
                                                       'V': 'G7', 'VI': 'Am7', 'VII': 'Bø'}
    assert Scale('C dorian').hasChord(Chord('Gm7'))
    assert Scale('C dorian').hasChord('Gm7')

    assert Scale('D Ionian').relativeMinor() == Scale('B Aeolian')

    for key in Note.chrSharp:
        assert Scale(key, 'Ionian').relativeMinor() == Scale(key, 'Ionian')
        assert Scale(key, 'Aeolian').relativeMajor() == Scale(key, 'Aeolian')

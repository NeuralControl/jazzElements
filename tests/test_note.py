from jazzElements.scale import Scale
from jazzElements.chord import Chord
from jazzElements.note import Note


def test_basics():
    for note in Note.chrSharp + Note.chrFlat:
        assert Note(note) == note
        assert Note(note).name == note
        assert Note(note) + 12 == note
        assert Note(note) - 12 == note
        assert Note(note + '#b#b#b') == Note(note)

def test_alterations():
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

def test_relationships():
    assert Note('C') - Note('D') == 10
    assert Note('D') - Note('C') == 2
    assert Note('B') - Note('C') == 11
    assert Note('C') - Note('B') == 1
    assert Note('C') - Note('C') == 0
    assert Note('G') - Note('C') == 7
    assert Note('C') - Note('G') == 5

    assert Note('A#') == Note('Bb')
    assert Note(Note('C')) == 'C'

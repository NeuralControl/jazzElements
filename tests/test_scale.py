from jazzTheory.base import Note, Chord, Scale

def test_Basics():
    assert Scale('C ionian').notes() == ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    assert Scale('C ionian').chords(asStr=True) == ['CM7', 'Dm7', 'Em7', 'FM7', 'G7', 'Am7', 'Bø']
    assert Scale('C dorian').hasChord(Chord('Gm7'))
    assert Scale('C dorian').hasChord('Gm7')
    assert Scale('C dorian').hasChord('Gm')


def test_relativeMinorMajor():
    assert Scale('D Ionian').relativeMinor() == Scale('B Aeolian')
    for key in Note.chrSharp:
        assert Scale(key, 'Ionian').relativeMinor() == Scale(key, 'Ionian')
        assert Scale(key, 'Aeolian').relativeMajor() == Scale(key, 'Aeolian')


def test_Numerals():
    assert Scale('C Major').chordsNumerals(nbNotes=3) == ['I', 'ii m', 'iii m', 'IV', 'V', 'vi m', 'vii o']
    assert Scale('C Minor').chordsNumerals(nbNotes=3) == ['i m', 'ii o', 'III', 'iv m', 'v m', 'VI', 'VII']


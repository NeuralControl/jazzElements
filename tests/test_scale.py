from jazzTheory.base import Note, Chord, Scale

def test_Basics():
    assert Scale('C ion').notes() == ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    assert Scale('C ion').chords(asStr=True) == ['CM7', 'Dm7', 'Em7', 'FM7', 'G7', 'Am7', 'Bø']
    assert Scale('C dor').hasChord(Chord('Gm7'))
    assert Scale('C dor').hasChord('Gm7')
    assert Scale('C dor').hasChord('Gm')


def test_relativeMinorMajor():
    for key in Note.chrSharp:
        assert Scale(key, 'ion').relativeMinor() == Scale(Scale(key, 'ion').notes()[5].name, 'aeo')
        assert Scale(key, 'aeo').relativeMajor() == Scale(Scale(key, 'aeo').notes()[2].name, 'ion')


def test_Numerals():
    assert Scale('C Major').chordsNumerals(nbNotes=3) == ['I', 'ii m', 'iii m', 'IV', 'V', 'vi m', 'vii o']
    assert Scale('C Minor').chordsNumerals(nbNotes=3) == ['i m', 'ii o', 'III', 'iv m', 'v m', 'VI', 'VII']




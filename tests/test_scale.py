from jazzElements.base import Note, Chord, Scale

def test_Basics():
    assert Scale('C ion').notes() == ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    assert Scale('C ion').chords(asStr=True) == ['CM7', 'Dm7', 'Em7', 'FM7', 'G7', 'Am7', 'Bø']
    assert Scale('C dor').hasChord(Chord('Gm7'))
    assert Scale('C dor').hasChord('Gm7')
    assert Scale('C dor').hasChord('Gm')


def test_relativeModes():
    for key in Note.chrSharp:
        assert Scale(key, 'ion').relativeMinor() == Scale(Scale(key, 'ion').notes()[5].name, 'aeo')
        assert Scale(key, 'aeo').relativeMajor() == Scale(Scale(key, 'aeo').notes()[2].name, 'ion')

    # Relative keys should have the same notes
    for k in Note.chrSharp:
        for m in Scale.modesLst:
            scale = Scale(k+' '+m)
            for s in scale.relativeModes():
                assert sorted(s.notes(asStr=True)) == sorted(scale.notes(asStr=True))

def test_Numerals():
    assert Scale('C Major').chordsRoman(nbNotes=3) == ['I', 'iim', 'iiim', 'IV', 'V', 'vim', 'viio']
    assert Scale('C Minor').chordsRoman(nbNotes=3) == ['im', 'iio', 'III', 'ivm', 'vm', 'VI', 'VII']
    assert Scale('C Minor').chordsRoman(nbNotes=4) == ['im7', 'iiø', 'IIIM7', 'ivm7', 'vm7', 'VIM7', 'VII7']


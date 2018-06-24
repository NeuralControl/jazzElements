ex1 = \
    {
        'orgPrg': '|Dm7|G7|CM7|CM7|Dm7|',  # 251 then 1-2
        'tri<': '|Dm7|G7|CM7|CM7,G♭7|Dm7|',  # tritone sub of previous chord
        'tri>': '|Dm7|G7|CM7|CM7,A♭7|Dm7|',  # tritone sub of next chord
        'app1': '|Dm7|G7|CM7|CM7,Em7|Dm7|',  # approach (diatonic)
        'app2': '|Dm7|G7|CM7|CM7,Db7|Dm7|',  # approach (semitone)
        'app3': '|Dm7|G7|CM7|CM7,Eb7|Dm7|',  # approach (semitone)
        'app4': '|Dm7|G7|CM7|CM7,D♭o7|Dm7|',  # approach (semitone dim)
        'app5': '|Dm7|G7|CM7|CM7,E♭o7|Dm7|',  # approach (semitone dim)
        'domMin': '|Dm7|G7|CM7|CM7,D7|Dm7|',  # dominant minor ???
        '5/': '|Dm7|G7|CM7|CM7,A7|Dm7|',  # secondary 5
        '2-5/': '|Dm7|G7|CM7|CM7,Em7,A7|Dm7|',  # secondary 2-5
        '3sub1u': '|Dm7|G7|CM7|Em7|Dm7|', # 3sub1 using a 3rd up
        '3sub1d': '|Dm7|G7|CM7|Am7|Dm7|',# 3sub1 using a 3rd down
    }

ex2 = \
    {
        'orgPrg': '|Dm7|G7|CM7|Am7|Dm7|G7|',
        'secDom': '|Dm7|G7|CM7|A7|Dm7|G7|',  # Secondary Dominant
        'secLTChord1': '|Dm7|G7|CM7|C#ø7|Dm7|G7|',  # Secondary Leading Tone Chord
        'secLTChord2': '|Dm7|G7|CM7|C#o7|Dm7|G7|',  # Secondary Leading Tone Chord
        '3sub6u': '|Dm7|G7|CM7|CM7|Dm7|G7|',  # 3sub6 using a 3rd up
        '3sub6d': '|Dm7|G7|CM7|FM7|Dm7|G7|', # 3sub6 using a 3rd up
        '#Vo7sub': '|Dm7|G7|CM7|Am7|Dm7|G#dim7 |', # #Vo7 sub for a DOM chord
    }

ex3 = \
    {
        'orgPrg': '|Dm7|G7|CM7|Dm7|G7|CM7|',  # 251251
        'bor1': '|Dm7|G7|CM7|Dm7♭5|G7♭9|CM7|',  # Borrowed from harmonic minor
        'bor2': '|Dm7|G7|CM7|Gm7|CM7|Dm7♭5|',  # Borrowed from Aeolian
        'bor3': '|Dm7|G7|CM7|D♭M7|Gm7♭5|CM7|',  # Borrowed from Phrygian
        'bor4': '|Dm7|G7|CM7|D7|GM7|CM7|',  # Borrowed from Lydian
    }

ex4 = \
    {
        'allOfMe': '|C7|C7|E7|E7|A7|A7|Dm7|Dm7|E7|E7|Am7|Am7|D7|D7|Dm7|G7|',
        'allOfMePass1':
            '|C7|C7,Dm7|E7|E7,B♭7|A7|A7,Eø7,A7|Dm7|Dm7,D#o7|E7|E7,Bø7|Am7|Am7,A♭7|'
            'D7|D7,A♭7|Dm7,Do7|G7,D♭7|',
        'allOfMePass2':
            '|C7,C#dim|Dm7,D#o7|E7,CMaj7|Bø7,E7|A7,A♭7|A7,G7|Dm7,C#o7|Dm7,D#o7'
            '|E7,F7|G7,G#7|Am7,E7|A♭7,E♭7|D7,D#o7|D7,Eø7|Dm7,Do7|G7,D♭7|',
        'cycl1': '|CMaj7,B7|Em7,A7|Dm7,G7|CMaj7|',  # Cycling Secondary Dominant
        'cycl2': '|CMaj7,B7|E7,A7|D7,G7|CMaj7|',  # Cycling Secondary Dominant without resolving
        'cycl3': '|Em7,A7|E♭m7,A♭7|Dm7|G7|',  # Chromatic Cycling Secondary ii, V
        'sec25': '|CMaj7|Em7,A7|Dm7|G7|',  # Secondary ii, V
        'pivot': '|Dm7|G7|CMaj7|Em7|A7|DMaj7|', # 251 in C then 251 in D with Em7 as pivot
        'pivot2': '|Cm7|F7|B♭M7|E♭M7|Am7♭5|D7|Gm7|Gm7|', # pivot chord (EbM7) in autumn leaves
        'chain':'|FMaj7|Em7♭5,A7|Dm7,G7|Cm7,F7|B♭7|', #blues for alice, succession of 2-5 to move quickly through keys, moving down by semitone, tone or fifth
        'secDom2': '|C|F|D7|G7|C|',  # I IV V/V V I
    }

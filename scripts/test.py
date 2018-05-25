from jazzElements.base import *

# Can we simplify chords definitions?


typesLst = {
    # Major
    '': '1-3-5',
    'M6': '1-3-5-6',
    '6': '1-3-5-6',
    '6/9': '1-3-5-6-4',
    'M7': '1-3-5-7',
    'M7#5': '1-3-#5-7',
    'M9': '1-3-5-7-2',
    'M9(no7)': '1-3-5-2',
    'M(add9)': '1-3-5-2',
    'M11': '1-3-5-7-2-4',

    # Minor
    'm': '1-b3-5',
    'm6': '1-b3-5-6',
    'm7': '1-b3-5-b7',
    'm9': '1-b3-5-b7-2',
    'm9(no7)': '1-b3-5-2',
    'm7b9': '1-b3-5-b7-b2',
    'm7b5b9': '1-b3-b5-b7-b2',
    'm11': '1-b3-5-b7-2-4',

    # Dominant
    '7': '1-3-5-b7',
    '7+5': '1-3-#5-b7',
    '7#5': '1-3-#5-b7',
    '9': '1-3-5-b7-2',
    '7b9': '1-3-5-b7-b2',
    '11': '1-3-5-b7-2-4',
    '11(no7)': '1-3-5-2-4',
    '11(no7,no9)': '1-3-5-4',
    '11(no9)': '1-3-5-b7-4',
    '13': '1-3-5-b7-2-4-6',
    '13(no7)': '1-3-5-2-4-6',  # todo ugly
    '13(no9)': '1-3-5-b7-4-6',
    '13(no11)': '1-3-5-b7-2-6',
    '13(no7no9)': '1-3-5-4-6',
    '13(no7no11)': '1-3-5-2-6',
    '13(no9no11)': '1-3-5-b7-2-4-6',

    # diminished
    'o': '1-b3-b5',
    'o7': '1-b3-b5-6',  # bb7->6
    'dim': '1-b3-b5',
    'dim7': '1-b3-b5-6',  # bb7->6
    'ø': '1-b3-b5-b7',
    'hdim': '1-b3-b5-b7',
    'm7b5': '1-b3-b5-b7',
    # augmented
    'aug': '1-3-#5',
    '+': '1-3-#5',
    # sus
    'sus4': '1-4-5',
    'sus2': '1-2-5',
    '7sus4': '1-4-5-b7',
    '7sus2': '1-2-5-b7',
    '9sus4': '1-4-5-b7-2',
    '9sus2': '1-2-5-b7-2',
    # misc:
    '5': '1-3',

}


accidentals = "(b|bb)?",
chords = "(m|maj7|maj|min7|min|sus)?",
suspends = "(1|2|3|4|5|6|7|8|9)?",
sharp = "(#)?",
regex = new
RegExp("\\b" + notes + accidentals + chords + suspends + "\\b" + sharp, "g");

def testMyTypes():
    root = 'C♭'
    ok=[]
    nok=[]
    for chr in typesLst:
        try:
            result = ','.join(findChords(root + chr)[0])
            print('{:15} | {}'.format(root + chr, result))
            ok.append(root + chr)
        except:
            #print('{:15} | {}'.format(root + chr, 'FAIL'))
            nok.append(root+chr)
#    print('ok   :'+','.join(ok))
    print('nok  :'+','.join(nok))
    print('ok: ' + str(100 * len(ok) / len(typesLst)))

def findChords(chrStr):
    # todo: dont forget to compile
    notes = "([CDEFGABX])"
    accidentals = "(#|#|b|♭|♯)*"
    chords = "(maj|min|m|sus[0-9]*|aug|dim|m|M|o|hdim|ø|\+|\-)*"
    additions = "([0-9]*|sus[0-9]*|add[0-9]*|no[0-9]*)*"
    return re.findall(r'\b' + notes + accidentals + chords + additions + r'(?!\w)', chrStr.replace(',',''))

testMyTypes()

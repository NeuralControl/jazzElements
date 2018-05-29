

class Note:
    """
    Create a new note with format verification and simplification
    Args:
        note: note string format (can use unicode b,♭,#,♯ )
        alt: additional alteration
    Examples:
        n=Note('Db')
        n=Note('D♭')
        n=Note('D♭♭♭♭♭♭♭')
        n=Note('D♭',+3)
    """

    chrSharp = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B']
    chrFlat = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'G♭', 'G', 'A♭', 'A', 'B♭', 'B']

    sharp = '#'
    Sharp = u"\u266f"
    flat = 'b'
    Flat = u"\u266d"
    natural = 'n'
    Natural = u"\u266e"
    altLst = {sharp: 1, Sharp: 1, flat: -1, Flat: -1, natural: 0, Natural: 0, '?': 0, '-': -1, '+': 1}

    def __init__(self, note, alt=0):
        if isinstance(note, Note):
            self.name = note.name
        else:
            if note[0].upper() in self.chrSharp:
                self.name = note[0].upper()
            else:
                raise ValueError('Note unknown')

            for alti in note[1:]:
                if alti in self.altLst:
                    alt += self.altLst[alti]
                else:
                    raise ValueError('Alteration unknown: {}'.format(alti))
        alt = alt % 12 if alt > 0 else alt
        if alt == 0:
            return
        elif alt < 0:
            chrScale = self.chrFlat[::-1] * 2 + self.chrSharp[::-1] * 2
        else:
            chrScale = self.chrSharp * 2 + self.chrFlat * 2

        self.name = chrScale[(chrScale.index(self.name)) + abs(alt) % 12]

    def __str__(self):
        return self.name

    def __add__(self, alt):
        """
        Adds alt half steps to a given note
        Args:
            alt: number of half steps to add
        Returns:
            Altered Note
        Examples:
            Note('C')+2 returns Note('D')
        """
        return Note(self, alt)

    def __sub__(self, altOrNote):
        """
        Returns the steps from another note, OR transpose down alt halfSteps

        Args:
            altOrNote: <int>: number of halfSteps to substract
                       <Note>:  the note to compare to

        Returns:
            number of halfSteps or altered Note

        Examples:
            Note('D')-Note('C') returns 2
            Note('D')-2 returns Note('C')
        """

        if isinstance(altOrNote, Note):
            n1 = ((self.chrFlat + self.chrSharp).index(self.name)) % 12
            n2 = ((self.chrFlat + self.chrSharp).index(altOrNote.name)) % 12
            return n1 - n2 if n1 - n2 >= 0 else 12 + n1 - n2
        else:
            return Note(self, -altOrNote)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, note):
        """
        Tests if self is equivalent to another Note
        Args:
            note: Note to compare to
        Returns:
            bool
        """
        if isinstance(note, str):
            note = Note(note)
        return (self - note) == 0
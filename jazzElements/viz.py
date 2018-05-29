from matplotlib.patches import FancyBboxPatch
from matplotlib.pyplot import *
from jazzElements.note import Note

def printNotes(notes, fmt='shade'):
    if isinstance(notes[0], str):
        notes = [Note(n) for n in notes]
    if fmt == 'square':
        b, w, spc = [u"\u25A1", u"\u25A0", u"\u2005"]
    elif fmt == 'shade':
        b, w, spc = [u"\u2591", u"\u2588", u"\u2005"]
    else:
        b, w, spc = [u"\u2591", u"\u2588", u"\u2005"]

    N = [b] * 12
    for ni, n in enumerate([Note(n) for n in ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B']]):
        if n in notes: N[ni] = w

    print(3 * spc + N[1] + 2 * spc + N[3] + 9 * spc + N[6] + 2 * spc + N[8] + 2 * spc + N[10] + 7 * spc +
          3 * spc + N[1] + 2 * spc + N[3] + 9 * spc + N[6] + 2 * spc + N[8] + 2 * spc + N[10] + '\n' +
          N[0] + 2 * spc + N[2] + 2 * spc + N[4] + 4 * spc + N[5] + 2 * spc + N[7] + 2 * spc + N[9] + 2 * spc + N[
              11] + 3 * spc +
          N[0] + 2 * spc + N[2] + 2 * spc + N[4] + 4 * spc + N[5] + 2 * spc + N[7] + 2 * spc + N[9] + 2 * spc + N[
              11])

def plotNotes(notes, pos=None, name='', ax=0, nbOctaves=1):
    if pos is None:
        pos = [0, 0, 100, 40]

    def plotKey(ax, x, y, w, h, keyType, status):
        lw = .5
        pad = 0.5
        # edgeColor = 'w'
        # parms = dict(
        #     black=dict(color=['skyblue', 'steelblue'], z=1),
        #     white=dict(color=['skyblue', 'steelblue'], z=0)
        # )

        edgeColor = 'k'
        parms = dict(
            black=dict(color=['k', 'skyblue'], z=1),
            white=dict(color=['w', 'skyblue'], z=0)
        )

        ax.add_patch(FancyBboxPatch((x + pad, y + pad),
                                    abs(w) - 2 * pad, abs(h) - 2 * pad,
                                    boxstyle="round,pad=" + str(pad),
                                    fc=parms[keyType]['color'][status], ec=edgeColor, zorder=parms[keyType]['z'],
                                    lw=lw))

    nb = int(np.ceil(len(notes) / (nbOctaves * 12)) * (nbOctaves * 12))
    start = 'C' if notes[0] - Note('C') < notes[0] - Note('F') else 'F'
    chromatic = Note.chrSharp * 4
    chromatic = chromatic[chromatic.index(Note(start)):]
    chromatic = chromatic[:nb]
    whites = [n for n in chromatic if n in [Note(n) for n in ['C', 'D', 'E', 'F', 'G', 'A', 'B']]]
    whiteWidth = pos[2] / len(whites)
    blackWidth = whiteWidth / 2

    if ax == 0:
        figure(figsize=(3, 1))
        ax = gca()
    axis('off')

    nWhites = 0
    for i, n in enumerate(chromatic):
        if n in whites:
            plotKey(ax, pos[0] + (nWhites) * whiteWidth, pos[1], whiteWidth, pos[3], keyType='white', status=n in notes)
            nWhites += 1
        else:
            plotKey(ax, pos[0] + (nWhites) * whiteWidth - blackWidth / 2, pos[1] + pos[3] / 3, blackWidth,
                    2 * pos[3] / 3, keyType='black', status=n in notes)
    plot(0, 0, '.w', zorder=-1)
    if name:
        text(pos[0], pos[1] + pos[3] / 2, name, ha='right', va='center', rotation=90)



from __future__ import division
from itertools import combinations
import pc_sets


PC_SETS = pc_sets.pc_sets


def flatten(alist):
    return [item for sublist in alist for item in sublist]


def mod12(n):
    return n % 12


def interval(x, y):
    return mod12(x - y)


def interval_class(x, y):
    return min(interval(x, y), interval(y, x))


def intervals(notes):
    return [interval_class(y, x) for x,y in zip(notes, rotate(notes)[:-1])]


def all_intervals(notes):
    return sorted(flatten([intervals(n) for n in combinations(sorted(notes), 2)]))


def set_sizes(pset):
    return [interval(x, y) for x,y in zip(rotate(pset, len(pset) - 1), pset)]


def set_size(pset):
    return mod12(pset[-1] - pset[0])


def transposition(notes, index):
    return [mod12(n + index) for n in notes]


def inversion(notes, index=0):
    # FIXME: check Jama's reisa and document
    return [mod12(index - n) for n in notes]


def transposition_startswith(notes, start):
    return transposition(notes, start - notes[0])


def inversion_startswith(notes, start):
    transp = transposition_startswith(notes, 0)
    return transposition_startswith(inversion(transp), start)


def inversion_first_note(notes):
    return inversion(notes, 2 * notes[0])


def rotate(item, n=1):
    modn = n % len(item)
    return item[modn:] + item[0:modn]


def rotate_set(pset):
    # return all rotations of a set
    return [rotate(pset, x) for x in range(0, len(pset))]


def retrograde(notes):
    return list(reversed(notes))



def interval_vector(notes):
    vector = [0, 0, 0, 0, 0, 0]

    for i in all_intervals(notes):
        vector[i-1] += 1

    return vector


def order_set(notes):
    # it doesn't eliminate repetition
    return sorted([mod12(n) for n in notes])


def interval_tie(pset):
    # return interval of between second-to-last and first, according to Straus.
    return interval(pset[-2], pset[0])


def normal_form(notes):
    oset = order_set(notes)
    rotations = rotate_set(oset)
    min_size = min(set_sizes(oset))
    smallest_sets = [x for x in rotations if set_size(x) == min_size]

    if len(smallest_sets) == 1:
        return smallest_sets[0]
    else:
        min_pack_size = min([interval_tie(x) for x in smallest_sets])
        packed_sets = [x for x in smallest_sets if interval_tie(x) == min_pack_size]

        return packed_sets[0]


def prime_form(notes):
    set_zero = transposition_startswith(normal_form(notes), 0)
    set_inv = transposition_startswith(normal_form(inversion(set_zero)), 0)
    if interval_tie(set_zero) <= interval_tie(set_inv):
        return set_zero
    else:
        return set_inv


def matrix(row):
    return [transposition_startswith(row, n) for n in inversion_first_note(row)]


def row_matrix_search(matrix, notes):
    # return positions
    return [[row.index(note) for note in notes] for row in matrix]


def column_matrix_search(matrix, notes):
    return [[row.index(note) for note in notes] for row in zip(*matrix)]


def note_to_lily(note, octave=''):
    ## note as integer
    names = "c cis d dis e f fis g gis a ais b".split()
    return names[note % 12] + octave + "!"


def notes_to_lily(notes):
    note_list = []
    prev_note = notes[0]
    for note in notes:
        if interval(note, prev_note) > 6:
            octave = "'"
        else:
            octave = ""
        note_list.append(note_to_lily(note, octave))
        prev_note = note
    return " ".join(note_list)


def notes_as_lily_chord(notes):
    ## an interable as a lily chord
    return "<{0}>".format(notes_to_lily(notes))


def note_name(number):
    notes = "C C# D D# E F F# G G# A A# B".split()
    return notes[mod12(number)]


def notes_names(notes):
    return [note_name(x) for x in notes]


def accidentals(note_string):
    acc = len(note_string[1:])
    if "#" in note_string:
        return acc
    elif "b" in note_string:
        return -acc
    else:
        return 0


# Return a tuple in the format (note_integer, accidental):
# >>>note_accidental("Eb")
# >>>(4, -1)
def note_accidental(note_string):
    notes = "C . D . E F . G . A . B".split()
    name = note_string[0:1].upper()
    number = notes.index(name)
    acc = accidentals(note_string)
    return number, acc

    
def name_to_number(note_string):
    number, acc = note_accidental(note_string)
    return mod12(number + acc)


def note_duration(note_value, unity, tempo):
    return (60.0 * note_value) / (tempo * unity)


def durations(notes_values, unity, tempo):
    return [note_duration(nv, unity, tempo) for nv in notes_values]


def diatonic_interval(note_string1, note_string2):
    interval_names = "Unison Second Second Third Third Fourth . Fifth Sixth Sixth Seventh Seventh".split()

    n1, acc1 = note_accidental(note_string1)
    n2, acc2 = note_accidental(note_string2)
    pitch1 = name_to_number(note_string1)
    pitch2 = name_to_number(note_string2)

    simple_interval = interval(n1, n2)
    interval_name = interval_names[simple_interval]
    interval_class = interval(pitch1, pitch2)

    print interval_name, interval_class, simple_interval

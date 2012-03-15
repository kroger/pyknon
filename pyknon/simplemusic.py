from __future__ import division
import pc_sets


PC_SETS = pc_sets.pc_sets


def mod12(n):
    return n % 12


def interval(x, y):
    return mod12(y - x)

def interval_class(x, y):
    return min(interval(x, y), interval(y, x))


def intervals(notes):
    return [interval_class(y, x) for x,y in zip(notes, rotate(notes)[:-1])]


def transposition(notes, index):
    return [mod12(n + index) for n in notes]


def inversion(notes, index=0):
    return [mod12(index - n) for n in notes]


def transposition_startswith(notes, start):
    return transposition(notes, start - notes[0])


def inversion_startswith(notes, start):
    transp0 = transposition_startswith(notes, 0)
    inv0 = inversion(transp0, 0)
    return transposition_startswith(inv0, start)


def rotate(item, n=1):
    modn = n % len(item)
    return item[modn:] + item[0:modn]


def rotate_set(pset):
    # return all rotations of a set
    return [rotate(pset, x) for x in range(0, len(pset))]


def retrograde(notes):
    return list(reversed(notes))


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

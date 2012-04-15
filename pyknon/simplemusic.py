"""
A simple numeric library for music computation.

This module is good for teaching, demonstrations, and quick hacks. To
generate actual music you should use the music module.

"""

from __future__ import division
from itertools import combinations, chain


def mod12(n):
    return n % 12


def interval(x, y):
    """Return the numeric interval between two notes."""
    return mod12(x - y)


def interval_class(x, y):
    return min(interval(x, y), interval(y, x))


def intervals(notes):
    return [interval_class(y, x) for x,y in zip(notes, rotate(notes)[:-1])]


def all_intervals(notes):
    intervals_list = [intervals(n) for n in combinations(sorted(notes), 2)]
    return sorted(chain.from_iterable(intervals_list))


def transposition(notes, index):
    """Transpose a set of notes by a numerical index."""
    return [mod12(n + index) for n in notes]


def transposition_startswith(notes, start):
    """Transpose a set of notes so it begins with `start` note."""
    return transposition(notes, start - notes[0])


def inversion(notes, index=0):
    """Invert a set of notes though an inversion index.

    The inversion index is not very musical. the function
    :func:`inversion_startswith` is probably more useful.
    """
    return [mod12(index - n) for n in notes]


def inversion_startswith(notes, start):
    """Invert a set of notes so it begins with `start` note."""
    transp = transposition_startswith(notes, 0)
    return transposition_startswith(inversion(transp), start)


def inversion_first_note(notes):
    return inversion(notes, 2 * notes[0])


def rotate(item, n=1):
    modn = n % len(item)
    return item[modn:] + item[0:modn]


def rotate_set(notes):
    """Return all rotations of a collection of notes."""
    return [rotate(notes, x) for x in range(0, len(notes))]


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


def name_to_number(note_string):
    notes = "C . D . E F . G . A . B".split()
    name = note_string[0:1].upper()
    number = notes.index(name)
    acc = accidentals(note_string)
    return mod12(number + acc)


def name_to_diatonic(note_string):
    """Return a number from 0 to 6 for the note name without the accidental."""
    notes = "C D E F G A B".split()
    name = note_string[0:1].upper()
    return notes.index(name)


def note_duration(note_value, unity, tempo):
    return (60.0 * note_value) / (tempo * unity)


def durations(notes_values, unity, tempo):
    return [note_duration(nv, unity, tempo) for nv in notes_values]


def get_quality(diatonic_interval, chromatic_interval):
    ## Doesn't work for Doubly Diminished Unison
    if diatonic_interval in [0, 3, 4]:
        quality_map = ["Diminished", "Perfect", "Augmented"]
    else:
        quality_map = ['Diminished', 'Minor', 'Major', 'Augmented']

    index_map = [-1, 0, 2, 4, 6, 7, 9]
    index = chromatic_interval - index_map[diatonic_interval]
    # special case for diminished unison
    index = 0 if index == 12 else index
    # make sure i is between 0 and the largest index
    i = min(max(index, 0), len(quality_map) - 1)
    return "Doubly " * abs(index - i) + quality_map[i]


def diatonic_interval(note1, note2):
    quantities = ["Unison", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh"]
    n1, n2 = name_to_number(note1), name_to_number(note2)
    d1, d2 = name_to_diatonic(note1), name_to_diatonic(note2)
    diatonic_interval = (d2 - d1) % 7
    chromatic_interval = interval(n2, n1)
    quantity_name = quantities[diatonic_interval]
    quality_name = get_quality(diatonic_interval, chromatic_interval)
    return "%s %s" % (quality_name, quantity_name)

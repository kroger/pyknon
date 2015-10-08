"""
A simple numeric library for music computation.

This module is good for teaching, demonstrations, and quick hacks. To
generate actual music you should use the music module.

"""

from __future__ import division
from itertools import combinations, chain
from fractions import Fraction


class SimpleMusicError(Exception):
    pass


def mod12(n):
    return n % 12


def interval(x, y):
    return mod12(x - y)


def interval_class(x, y):
    return min(interval(x, y), interval(y, x))


def intervals(notes):
    return [interval_class(y, x) for x, y in zip(notes, rotate(notes)[:-1])]


def all_intervals(notes):
    intervals_list = [intervals(n) for n in combinations(sorted(notes), 2)]
    return sorted(chain.from_iterable(intervals_list))


def transposition(notes, index):
    return [mod12(n + index) for n in notes]


def transposition_startswith(notes, start):
    return transposition(notes, start - notes[0])


def is_related_by_transposition(notes1, notes2):
    rotations = rotate_set(sorted(notes2))
    transpositions = [transposition(sorted(notes1), n) for n in range(0, 12)]
    return any(True for rotation in rotations if rotation in transpositions)


def inversion(notes, index=0):
    return [mod12(index - n) for n in notes]


def inversion_startswith(notes, start):
    transp = transposition_startswith(notes, 0)
    return transposition_startswith(inversion(transp), start)


def inversion_first_note(notes):
    return inversion(notes, 2 * notes[0])


def rotate(notes, n=1):
    modn = n % len(notes)
    return notes[modn:] + notes[0:modn]


def rotate_set(notes):
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
    notes = "C D E F G A B".split()
    name = note_string[0:1].upper()
    return notes.index(name)


def note_duration(note_value, unity, tempo):
    return (60.0 * note_value) / (tempo * unity)


def dotted_duration(duration, dots):
    ratio = Fraction(1, 2)
    return duration * (1 - ratio ** (dots + 1)) / ratio


def durations(notes_values, unity, tempo):
    return [note_duration(nv, unity, tempo) for nv in notes_values]


def get_quality(diatonic_interval, chromatic_interval):
    if diatonic_interval in [0, 3, 4]:
        quality_map = ["Diminished", "Perfect", "Augmented"]
    else:
        quality_map = ['Diminished', 'Minor', 'Major', 'Augmented']

    index_map = [-1, 0, 2, 4, 6, 7, 9]
    try:
        return quality_map[chromatic_interval - index_map[diatonic_interval]]
    except IndexError:
        raise SimpleMusicError("Sorry, I can't deal with this interval :-(")


def interval_name(note1, note2):
    quantities = ["Unison", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh"]
    n1, n2 = name_to_number(note1), name_to_number(note2)
    d1, d2 = name_to_diatonic(note1), name_to_diatonic(note2)
    chromatic_interval = interval(n2, n1)
    diatonic_interval = (d2 - d1) % 7
    quantity_name = quantities[diatonic_interval]
    quality_name = get_quality(diatonic_interval, chromatic_interval)
    return "%s %s" % (quality_name, quantity_name)

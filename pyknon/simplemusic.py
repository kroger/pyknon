"""
A simple numeric library for music computation.

This module is good for teaching, demonstration, and quick hacks. To
generate actual music you should use the music module.

"""

from __future__ import division
from itertools import combinations, chain


def mod12(n):
    return n % 12


def interval(x, y):
    return mod12(x - y)


def interval_class(x, y):
    return min(interval(x, y), interval(y, x))


def intervals(notes):
    return [interval_class(y, x) for x,y in zip(notes, rotate(notes)[:-1])]


def all_intervals(notes):
    intervals_list = [intervals(n) for n in combinations(sorted(notes), 2)]
    return sorted(chain.from_iterable(intervals_list))


def transposition(notes, index):
    return [mod12(n + index) for n in notes]


def transposition_startswith(notes, start):
    return transposition(notes, start - notes[0])


def inversion(notes, index=0):
    return [mod12(index - n) for n in notes]


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
    pass

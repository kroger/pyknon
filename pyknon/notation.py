import re


REGEX_NOTE = re.compile("([a-gA-GRr])([b#]*)([0-9]*)([.]*)([',]*)")
NOTE_NAMES = "c # d # e f # g # a # b".split()


class NotationError(Exception):
    pass


def parse_accidental(acc):
    n = len(acc) if acc else 0
    return -n if "b" in acc else n


def parse_octave(string):
    """5 is central octave. Return 5 as a fall-back"""

    if string:
        size = string.count(string[0])
        return size + 4 if string[0] == "'" else -size + 5
    else:
        return 5


def parse_dur(dur, dots=""):
    if dur in (0, "breve", "brevis"):
        base = 2
    elif dur == "longa":
        base = 4
    elif dur == "maxima":
        base = 8
    else:
        base = int(dur) ** -1

    return sum([base / (2 ** x) for x in range(0, len(dots) + 1)])


def note_number(pitch, acc):
    pitch_number = NOTE_NAMES.index(pitch.lower())
    return (pitch_number + parse_accidental(acc)) % 12


def parse_note(note, volume=120, prev_octave=5, prev_dur=0.25):
    m = REGEX_NOTE.match(note)
    if m:
        pitch, acc, dur, dots, octv = m.groups()
    else:
        raise NotationError("You need to have at least one note.")

    octave = parse_octave(octv) if octv else prev_octave
    duration = parse_dur(dur, dots) if dur else prev_dur

    if pitch in ["r", "R"]:
        return None, octave, duration, None
    else:
        return note_number(pitch, acc), octave, duration, volume


def parse_notes(notes, volume=120):
    # (number, octave, dur, volume)
    prev_oct = 5       # default octave
    prev_dur = 0.25    # default duration is 1/4, but it's 1 in the MIDI library

    result = []
    for item in notes:
        number, octave, dur, vol = parse_note(item, volume, prev_oct, prev_dur)
        result.append((number, octave, dur, vol))
        prev_oct = octave
        prev_dur = dur
    return result

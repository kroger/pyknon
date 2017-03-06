import collections
import copy
from pyknon import notation


class MusiclibError(Exception):
    pass


class Rest(object):
    """Class representing a musical rest; basically a pause where no
       Notes are playing.
    """
    def __init__(self, dur=0.25):
        self.dur = dur

    def __repr__(self):
        return "<R: {0}>".format(self.dur)

    def __eq__(self, other):
        return self.dur == other.dur

    @property
    def verbose(self):
        return "<Rest: {0}>".format(self.dur)

    @property
    def midi_dur(self):
        # The MIDI library uses 1 for quarter note but we use 0.25
        return self.dur * 4

    def stretch_dur(self, factor):
        return Rest(self.dur * factor)


class Note(object):
    """class representing a musical note
       the 12 musical notes in one octave are represented as one of 
         C C# D D# E F F# G G# A A# B
       we stores this as a number from 0-11 (inclusive)
       we also store the octave number
       as well as the duration the note should play for 
       and the volume it should play at
    """
    def __init__(self, value=0, octave=5, dur=0.25, volume=100):
        # if `value` is a string
        if isinstance(value, str):
            # attempt to parse the musical notation
            self.value, self.octave, self.dur, self.volume = notation.parse_note(value)
        else:
            # otherwise build the Note object manually
            # we accept any number for the value
            # but break it up into the octave offset and the note value
            # the note value is the given value mod 12
            # the octave offset is floor( value / 12 ) + the given octave
            # this means we can pass in value=18, octave=0 to get note #6 in octave #1
            # and we can also pass in value=30, octave=4 to get note #6 in octave #6
            offset, val = divmod(value, 12) # divmod(x,y) returns (x//y, x%y)
            self.value = val
            self.octave = octave + offset
            self.dur = dur
            self.volume = volume

    def __eq__(self, other):
        return self.value == other.value and self.dur == other.dur and self.octave == other.octave

    def __sub__(self, other):
        return self.midi_number - other.midi_number

    def __repr__(self):
        return "<{0}>".format(self.name)

    @property
    def verbose(self):
        return "<Note: {0}, {1}, {2}>".format(self.value, self.octave, self.dur)

    @property
    def name(self):
        note_names = "C C# D D# E F F# G G# A A# B".split()
        return note_names[self.value % 12]

    @property
    def midi_number(self):
        """MIDI represents every note as a single number
           octave #0 contains notes 0-11, octave #1 contains notes 12-23, etc.
        """
        return self.value + (self.octave * 12)

    @property
    def midi_dur(self):
        # The MIDI library uses 1 for quarter note but we use 0.25
        return self.dur * 4

    def __note_octave(self, octave):
        """Return a note value in terms of a given octave

           n = Note(11, 4)
           __note_octave(n, 5) = -1
        """

        return self.value + ((self.octave - octave) * 12)

    def transposition(self, index):
        """move the note up by `index` number of semitones
           if `index` is negative
        """
        return Note(self.value + index, self.octave, self.dur, self.volume)

    ## FIXME: transpose down
    def tonal_transposition(self, index, scale):
        """using the given `scale` (sequence of notes)
           move the note to the `index`-th note
           index=1 means no change
        """
        pos = index + scale.index(self) - 1        # get note position in scale
        octave, rest = divmod(pos, 7)              # get octave offset (ignore `rest`)
        note = copy.copy(scale[pos % len(scale)])  # get the note object from the scale and clone it
        note.octave += octave
        return note

    def harmonize(self, scale, interval=3, size=3):
        """generate a sequence of `size` number of notes
           each pair of notes in the produced sequence are 
                (`interval`-1) notes apart in the given `scale`
        """
        i = (interval - 1)
        indices = range(1, size*i, i)
        return [self.tonal_transposition(x, scale) for x in indices]

    def inversion(self, index=0, initial_octave=None):
        """invert the note around the given `index` in a given `initial_octave`
           if the current note's value is x semitones above `index`, 
                the resulting note's value will be x semitones below `index`
                and if the current note's value is x semitones below `index`
                the resulting note's value will be x semitones above `index`
           the same relationship will be true between the current note's octave, 
                the `initial_octave`, and the resulting note's octave 
        """
        value = self.__note_octave(initial_octave) if initial_octave else self.value
        octv = initial_octave if initial_octave else self.octave
        note_value = (2 * index) - value
        return Note(note_value, octv, self.dur, self.volume)

    def stretch_dur(self, factor):
        return Note(self.value, self.octave, self.dur * factor, self.volume)


class NoteSeq(collections.MutableSequence):
    """Class representing an arbitrary sequence of Notes and Rests
    """
    @staticmethod
    def _is_note_or_rest(args):
        """Returns True if all items in the NoteSeq are either a Note or Rest
        """
        return all([True if isinstance(x, Note) or isinstance(x, Rest) else False for x in args])

    @staticmethod
    def _make_note_or_rest(note_list):
        # `note_list` takes the form (number, octave, dur, volume)
        if note_list[0] is not None:
            return Note(*note_list)
        else:
            # if the note number is None, this represents a rest
            # make a Rest object with the given duration
            return Rest(note_list[2])

    @staticmethod
    def _parse_score(filename):
        """parse a file for a list of notes
           assume each line is a space-separated sequence of notes
           return the list of the string representation for each note
        """
        with open(filename) as score:
            notes = []
            for line in score:
                notes.extend([note for note in line.split()])
            return notes

    def __init__(self, args=None):
        if isinstance(args, str):
            if args.startswith("file://"):
                # parse a file for list of notes
                filename = args.replace("file://", "")
                note_lists = notation.parse_notes(self._parse_score(filename))
            else:
                # parse the string assuming it's a space-separated list of notes
                note_lists = notation.parse_notes(args.split())
            # notation.parse_notes() returns a list of lists of attributes for a Note/Rest
            # build the Note or Rest objects from that list
            self.items = [self._make_note_or_rest(x) for x in note_lists]
        elif isinstance(args, collections.Iterable):
            # if we got a list, tuple, or other iterable object
            # make sure everything in the iterable is a note or rest
            if self._is_note_or_rest(args):
                self.items = args
            else:
                raise MusiclibError("Every argument have to be a Note or a Rest.")
        elif args is None:
            self.items = []
        else:
            raise MusiclibError("NoteSeq doesn't accept this type of data.")

    def __iter__(self):
        for x in self.items:
            yield x

    def __delitem__(self, i):
        del self.items[i]

    def __getitem__(self, i):
        # indexing with []
        # if `i` is an int, look up that item
        if isinstance(i, int):
            return self.items[i]
        else:
            # `i` is not an int so we assume a slice was requested
            # get the slice of our Notes/Rests and create a new NoteSeq from that slice
            return NoteSeq(self.items[i])

    def __len__(self):
        return len(self.items)

    def __setitem__(self, i, value):
        self.items[i] = value

    def __repr__(self):
        return "<Seq: {0}>".format(self.items)

    def __eq__(self, other):
        """Two NoteSeq objects are only equal if
           all of their elements are pairwise equal
        """
        if len(self) == len(other):
            return all(x == y for x, y in zip(self.items, other.items))

    def __add__(self, other):
        if isinstance(other, NoteSeq):
            # Adding one NoteSeq to another NoteSeq: combine items
            return NoteSeq(self.items + other.items)

        elif isinstance(other, Note) or isinstance(other, Rest):
            # Adding a Note or Rest to a NoteSeq: append that Note/Rest to the items
            # ie. NoteSeq(1,2) + Note(3) => NoteSeq(1,2,3)
            return NoteSeq(self.items + [other])


    def __radd__(self, other):
        if isinstance(other, NoteSeq):
            #  This should never be called because the other NoteSeq should
            #  handle the concatenation, but it's here for completness sake
            return NoteSeq(other.items + self.items)

        elif isinstance(other, Note) or isinstance(other, Rest):
            # Adding a NoteSeq to a Note/Rest: put that Note/Rest at 
            # the beginning of the NoteSeq
            # ie. Note(3) + NoteSeq(1,2)) => NoteSeq(3,1,2)
            return NoteSeq([other] + self.items)


    def __mul__(self, n):
        return NoteSeq(self.items * n)

    @property
    def verbose(self):
        string = ", ".join([note.verbose for note in self.items])
        return "<NoteSeq: [{0}]>".format(string)

    def retrograde(self):
        """Reverse the sequence
           "retrograde" is the musical term for "play it backward"
        """
        return NoteSeq(list(reversed(self.items)))

    def insert(self, i, value):
        self.items.insert(i, value)

    def transposition(self, index):
        """Transpose all Notes in the NoteSeq by `index` amount
           See Note.transposition(index) for more details
        """
        return NoteSeq([x.transposition(index) if isinstance(x, Note) else x
                        for x in self.items])

    def _make_note(self, item):
        return Note(item) if (isinstance(item, int) or isinstance(item, str)) else item

    def transposition_startswith(self, note_start):
        """transpose the NoteSeq such that the result starts with `note_start`
        """
        note = self._make_note(note_start)
        # determine the difference between `note_start` and the first item
        # this is how far we need to transpose the first item in order to get to `note_start`
        return self.transposition(note - self.items[0])

    def inversion(self, index=0):
        """Invert all Notes in the NoteSeq around `index` and the octave of the first note
           See Note.inversion(index) for more details
        """
        initial_octave = self.items[0].octave
        return NoteSeq([x.inversion(index, initial_octave) if isinstance(x, Note)
                        else x for x in self.items])

    def inversion_startswith(self, note_start):
        """Invert all Notes in the NoteSeq
           then transpose such that the first Note in the resulting 
                NoteSeq is `note_start` 
        """
        note = self._make_note(note_start)
        # transpose all notes into the correct octave, then invert all notes
        inv = self.transposition_startswith(Note(0, note.octave)).inversion()
        # transpose all notes so that we start at the desire note
        return inv.transposition_startswith(note)

    def harmonize(self, interval=3, size=3):
        """Returns a list of harmonies formed from each note in the NoteSeq
        """
        return [NoteSeq(note.harmonize(self, interval, size)) for note in self]

    def rotate(self, n=1):
        """Simulates a N rotations
            a single rotation removes the first item and adds it on to the end
        """
        modn = n % len(self)    # only need to rotate n mod length times
                                # because rotation is periodic
        result = self.items[modn:] + self.items[0:modn]
        return NoteSeq(result)

    def stretch_dur(self, factor):
        """Stretch all Notes and Rests by `factor`
        """
        return NoteSeq([x.stretch_dur(factor) for x in self.items])

    ## TODO: gives an error with rests
    def intervals(self):
        """Returns a list of the interval distance between successive pairs of Notes
        """
        v1 = self[:]
        v2 = self.rotate()

        return [y - x for x, y in zip(v1, v2[:-1])]

    def stretch_interval(self, factor):
        """Returns a NoteSeq where all interval distances between 
           successive pairs of Notes are increased by `factor`
        """
        intervals = [x + factor for x in self.intervals()]  # list of new interval distances
        note = copy.copy(self[0])
        result = NoteSeq([note])
        for i in intervals:                 # for each new interval distance:
            note = note.transposition(i)    #   create a new Note transposed 
                                            #     from the previous Note by that distance
            result.append(note) 
        return result

    # Aliases
    transp = transposition_startswith
    inv = inversion_startswith

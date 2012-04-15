from __future__ import division

try:
    import unittest2 as unittest
except:
    import unittest

import pyknon.simplemusic as music


class TestSimplemusic(unittest.TestCase):
    def test_mod12(self):
        self.assertEqual(music.mod12(0), 0)
        self.assertEqual(music.mod12(1), 1)
        self.assertEqual(music.mod12(13), 1)
        self.assertEqual(music.mod12(14), 2)
        self.assertEqual(music.mod12(-1), 11)

    def test_interval(self):
        self.assertEqual(music.interval(3, 4), 11)
        self.assertEqual(music.interval(4, 3), 1)
        self.assertEqual(music.interval(0, 12), 0)
        self.assertEqual(music.interval(1, 10), 3)
        self.assertEqual(music.interval(10, 1), 9)

    def test_interval_class(self):
        self.assertEqual(music.interval_class(1, 9), 4)
        self.assertEqual(music.interval_class(9, 1), 4)
        self.assertEqual(music.interval_class(11, 1), 2)
        self.assertEqual(music.interval_class(1, 11), 2)
        self.assertEqual(music.interval_class(1, -1), 2)
        self.assertEqual(music.interval_class(3, 2), 1)

    def test_intervals(self):
        self.assertEqual(music.intervals([1, 2, 3]), [1, 1])
        self.assertEqual(music.intervals([0, 4, 7]), [4, 3])
        self.assertEqual(music.intervals([0, 11, 3]), [1, 4])

    def test_all_intervals(self):
        self.assertEqual(music.all_intervals([0, 1, 4]), [1, 3, 4])
        self.assertEqual(music.all_intervals([4, 1, 0]), [1, 3, 4])

    def test_transposition(self):
        n1 = [3, 7, 11, 10]
        n2 = [6, 10, 2, 1]
        self.assertEqual(music.transposition(n1, 3), n2)

    def test_inversion(self):
        n1 = [0, 4, 7]
        n2 = [0, 8, 5]
        n3 = music.inversion(n1, 0)
        self.assertEqual(n3, n2)
        self.assertEqual(music.inversion(n3), n1)

    def test_transposition_startswith(self):
        n1 = [3, 7, 11, 10]
        n2 = [4, 8, 0, 11]
        self.assertEqual(music.transposition_startswith(n1, 4), n2)

    def test_inversion_startswith(self):
        n1 = [3, 7, 11, 10]
        n2 = [3, 11, 7, 8]
        self.assertEqual(music.inversion_startswith(n1, 3), n2)
        self.assertEqual(music.inversion_startswith([11, 10, 7], 1), [1, 2, 5])

    def test_inversion_first_note(self):
        self.assertEqual(music.inversion_first_note([3, 7, 9]), [3, 11, 9])

    def test_rotate(self):
        n1 = [0, 1, 3, 7]
        self.assertEqual(music.rotate(n1, 0), n1)
        self.assertEqual(music.rotate(n1, 1), [1, 3, 7, 0])
        self.assertEqual(music.rotate(n1, 2), [3, 7, 0, 1])
        self.assertEqual(music.rotate(n1, 3), [7, 0, 1, 3])
        self.assertEqual(music.rotate(n1, 4), [0, 1, 3, 7])

    def test_rotate_set(self):
        all_rotations = [[1,2,3], [2,3,1], [3,1,2]]
        self.assertEqual(music.rotate_set([1,2,3]), all_rotations)

    def test_retrograde(self):
        self.assertEqual(music.retrograde([0, 4, 7, 10]), [10, 7, 4, 0])

    def test_note_name(self):
        self.assertEqual(music.note_name(0), "C")
        self.assertEqual(music.note_name(12), "C")
        self.assertEqual(music.note_name(1), "C#")
        self.assertEqual(music.note_name(3), "D#")

    def test_notes_names(self):
        notes = [0, 4, 8, 10, 14]
        self.assertEqual(music.notes_names(notes), ['C', 'E', 'G#', 'A#', 'D'])

    def test_accidentals(self):
        self.assertEqual(music.accidentals("C##"), 2)
        self.assertEqual(music.accidentals("D##"), 2)
        self.assertEqual(music.accidentals("Ebb"), -2)
        self.assertEqual(music.accidentals("Ab"), -1)

    def test_name_to_number(self):
        self.assertEqual(music.name_to_number("D###"), 5)
        self.assertEqual(music.name_to_number("D"), 2)
        self.assertEqual(music.name_to_number("A"), 9)
        self.assertEqual(music.name_to_number("Eb"), 3)
        self.assertEqual(music.name_to_number("Cbbb"), 9)

    def test_name_to_diatonic(self):
        self.assertEqual(music.name_to_diatonic("C"), 0)
        self.assertEqual(music.name_to_diatonic("D###"), 1)
        self.assertEqual(music.name_to_diatonic("Bb"), 6)

    def test_note_duration(self):
        self.assertEqual(music.note_duration(1/4, 1/4, 60), 1.0)
        self.assertEqual(music.note_duration(1/2, 1/4, 60), 2.0)

    def test_durations(self):
        self.assertEqual(music.durations([1/2, 1/4, 1/8], 1/4, 60), [2.0, 1.0, 0.5])
        self.assertEqual(music.durations([1/2, 1/4, 1/8], 1/4, 120), [1.0, 0.5, 0.25])

    def test_diatonic_interval(self):
        self.assertEqual(music.diatonic_interval("C", "C"), "Perfect Unison")
        self.assertEqual(music.diatonic_interval("C", "C#"), "Augmented Unison")
        self.assertEqual(music.diatonic_interval("C", "Cb"), "Diminished Unison")
        self.assertEqual(music.diatonic_interval("D", "Db"), "Diminished Unison")
        self.assertEqual(music.diatonic_interval("D", "F"), "Minor Third")
        self.assertEqual(music.diatonic_interval("D", "F#"), "Major Third")
        self.assertEqual(music.diatonic_interval("D", "Fb"), "Diminished Third")
        self.assertEqual(music.diatonic_interval("C", "E"), "Major Third")
        self.assertEqual(music.diatonic_interval("C", "Eb"), "Minor Third")
        self.assertEqual(music.diatonic_interval("D", "E"), "Major Second")
        self.assertEqual(music.diatonic_interval("D", "Eb"), "Minor Second")
        self.assertEqual(music.diatonic_interval("E", "F"), "Minor Second")
        self.assertEqual(music.diatonic_interval("E", "F#"), "Major Second")
        self.assertEqual(music.diatonic_interval("Eb", "F#"), "Augmented Second")
        self.assertEqual(music.diatonic_interval("Eb", "F##"), "Doubly Augmented Second")
        self.assertEqual(music.diatonic_interval("D", "B"), "Major Sixth")
        self.assertEqual(music.diatonic_interval("D", "B#"), "Augmented Sixth")
        self.assertEqual(music.diatonic_interval("E", "C"), "Minor Sixth")
        self.assertEqual(music.diatonic_interval("Eb", "C"), "Major Sixth")
        self.assertEqual(music.diatonic_interval("Db", "F#"), "Augmented Third")
        self.assertEqual(music.diatonic_interval("Db", "F##"), "Doubly Augmented Third")
        self.assertEqual(music.diatonic_interval("D", "Fbb"), "Doubly Diminished Third")
        self.assertEqual(music.diatonic_interval("D#", "Fbb"), "Doubly Doubly Diminished Third")
        self.assertEqual(music.diatonic_interval("D", "A"), "Perfect Fifth")
        self.assertEqual(music.diatonic_interval("C", "F"), "Perfect Fourth")
        self.assertEqual(music.diatonic_interval("C", "F#"), "Augmented Fourth")
        self.assertEqual(music.diatonic_interval("C", "Fb"), "Diminished Fourth")
        self.assertEqual(music.diatonic_interval("C", "Gb"), "Diminished Fifth")
        self.assertEqual(music.diatonic_interval("C", "G"), "Perfect Fifth")
        self.assertEqual(music.diatonic_interval("C", "G#"), "Augmented Fifth")
        self.assertEqual(music.diatonic_interval("Bb", "F"), "Perfect Fifth")
        self.assertEqual(music.diatonic_interval("Bb", "F#"), "Augmented Fifth")
        self.assertEqual(music.diatonic_interval("B", "F"), "Diminished Fifth")
        self.assertEqual(music.diatonic_interval("C", "F##"), "Doubly Augmented Fourth")
        self.assertEqual(music.diatonic_interval("Db", "A#"), "Doubly Augmented Fifth")
        self.assertEqual(music.diatonic_interval("F", "B"), "Augmented Fourth")

    @unittest.expectedFailure
    def test_diatonic_interval_fail(self):
        self.assertEqual(music.diatonic_interval("C", "Cbb"), "Doubly Diminished Unison")
        self.assertEqual(music.diatonic_interval("E", "Fbb"), "Doubly Diminished Second")


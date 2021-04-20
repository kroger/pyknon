from fractions import Fraction as F
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

    def test_is_related_by_transposition(self):
        self.assertTrue(music.is_related_by_transposition([0, 4, 7], [1, 5, 8]))
        self.assertTrue(music.is_related_by_transposition([0, 7, 4], [5, 8, 1]))
        self.assertTrue(music.is_related_by_transposition([4, 0, 7], [5, 1, 8]))
        self.assertFalse(music.is_related_by_transposition([4, 0, 7], [0, 3, 7]))

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

    def test_dotted_duration(self):
        self.assertEqual(music.dotted_duration(F(1/4), 0), F(1/4))
        self.assertEqual(music.dotted_duration(F(1/4), 1), F(3/8))
        self.assertEqual(music.dotted_duration(F(1/4), 2), F(7/16))

    def test_durations(self):
        self.assertEqual(music.durations([1/2, 1/4, 1/8], 1/4, 60), [2.0, 1.0, 0.5])
        self.assertEqual(music.durations([1/2, 1/4, 1/8], 1/4, 120), [1.0, 0.5, 0.25])


class TestIntervalName(unittest.TestCase):
    def test_interval_name_unison(self):
        self.assertEqual(music.interval_name("C", "C"), "Perfect Unison")
        self.assertEqual(music.interval_name("C", "C#"), "Augmented Unison")

    def test_interval_name_second(self):
        self.assertEqual(music.interval_name("D", "E"), "Major Second")
        self.assertEqual(music.interval_name("D", "Eb"), "Minor Second")
        self.assertEqual(music.interval_name("E", "F"), "Minor Second")
        self.assertEqual(music.interval_name("E", "F#"), "Major Second")
        self.assertEqual(music.interval_name("Eb", "F#"), "Augmented Second")
        self.assertEqual(music.interval_name("E", "Fb"), "Diminished Second")

    def test_interval_name_third(self):
        self.assertEqual(music.interval_name("D", "F"), "Minor Third")
        self.assertEqual(music.interval_name("D", "F#"), "Major Third")
        self.assertEqual(music.interval_name("D", "Fb"), "Diminished Third")
        self.assertEqual(music.interval_name("C", "E"), "Major Third")
        self.assertEqual(music.interval_name("C", "Eb"), "Minor Third")
        self.assertEqual(music.interval_name("Db", "F#"), "Augmented Third")

    def test_interval_name_fourth(self):
        self.assertEqual(music.interval_name("C", "F"), "Perfect Fourth")
        self.assertEqual(music.interval_name("C", "F#"), "Augmented Fourth")
        self.assertEqual(music.interval_name("C", "Fb"), "Diminished Fourth")
        self.assertEqual(music.interval_name("F", "B"), "Augmented Fourth")

    def test_interval_name_fifth(self):
        self.assertEqual(music.interval_name("D", "A"), "Perfect Fifth")
        self.assertEqual(music.interval_name("C", "Gb"), "Diminished Fifth")
        self.assertEqual(music.interval_name("B", "F"), "Diminished Fifth")
        self.assertEqual(music.interval_name("Bb", "F#"), "Augmented Fifth")

    def test_interval_name_sixth(self):
        self.assertEqual(music.interval_name("D", "B"), "Major Sixth")
        self.assertEqual(music.interval_name("E", "C"), "Minor Sixth")
        self.assertEqual(music.interval_name("D", "B#"), "Augmented Sixth")
        self.assertEqual(music.interval_name("E", "Cb"), "Diminished Sixth")

    def test_interval_name_seventh(self):
        self.assertEqual(music.interval_name("C", "B"), "Major Seventh")
        self.assertEqual(music.interval_name("E", "D#"), "Major Seventh")
        self.assertEqual(music.interval_name("D", "C"), "Minor Seventh")
        self.assertEqual(music.interval_name("D", "Cb"), "Diminished Seventh")

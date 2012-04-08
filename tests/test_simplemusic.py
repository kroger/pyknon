from __future__ import division
import sys

try:
    import unittest2 as unittest
except:
    import unittest
    
import pyknon.simplemusic as music


class TestNote(unittest.TestCase):
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

    def test_set_sizes(self):
        self.assertEqual(music.set_sizes([0, 4, 8, 9, 11]), [11, 8, 8, 11, 10])

    def test_set_size(self):
        self.assertEqual(music.set_size([0, 3, 11]), 11)
        self.assertEqual(music.set_size([3, 4, 11]), 8)
        self.assertEqual(music.set_size([4, 5, 10]), 6)

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

    def test_interval_vector(self):
        self.assertEqual(music.interval_vector([0, 4, 7]), [0, 0, 1, 1, 1, 0])

    def test_order_set(self):
        self.assertEqual(music.order_set([13, 14, 1, 3, 4]), [1, 1, 2, 3, 4])

    def test_interval_tie(self):
        self.assertEqual(music.interval_tie([0, 1, 4, 7]), 4)

    def test_normal_form(self):
        self.assertEqual(music.normal_form([9, 8, 11, 4, 0]), [8, 9, 11, 0, 4])
        self.assertEqual(music.normal_form([0, 1, 6]), [0, 1, 6])
        self.assertEqual(music.normal_form([3, 6, 9, 0]), [0, 3, 6, 9])
        self.assertEqual(music.normal_form([4, 8, 0]), [0, 4, 8])

    def test_prime_form(self):
        self.assertEqual(music.prime_form([0, 4, 7]), [0, 3, 7])
        # those are from previous bugs, keep'em
        self.assertEqual(music.prime_form([0, 1, 2, 4, 5]), [0, 1, 2, 4, 5])
        self.assertEqual(music.prime_form([0, 2, 3, 6, 7, 9]), [0, 2, 3, 6, 7, 9])

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
        
    def test_note_accidental(self):
        self.assertEqual(music.note_accidental("Eb"), (4, -1))
        self.assertEqual(music.note_accidental("C"), (0, 0))
        self.assertEqual(music.note_accidental("D#"), (2, 1))
        self.assertEqual(music.note_accidental("B#"), (11, 1))
        self.assertEqual(music.note_accidental("Bb"), (11, -1))

    def test_name_to_number(self):
        self.assertEqual(music.name_to_number("D###"), 5)
        self.assertEqual(music.name_to_number("D"), 2)
        self.assertEqual(music.name_to_number("A"), 9)
        self.assertEqual(music.name_to_number("Eb"), 3)
        self.assertEqual(music.name_to_number("Cbbb"), 9)

    def test_note_duration(self):
        self.assertEqual(music.note_duration(1/4, 1/4, 60), 1.0)
        self.assertEqual(music.note_duration(1/2, 1/4, 60), 2.0)

    def test_durations(self):
        self.assertEqual(music.durations([1/2, 1/4, 1/8], 1/4, 60), [2.0, 1.0, 0.5])
        self.assertEqual(music.durations([1/2, 1/4, 1/8], 1/4, 120), [1.0, 0.5, 0.25])

    @unittest.skip('I need to think how to implement diatonic interval')
    def test_diatonic_interval(self):
        self.assertEqual(music.diatonic_interval("C", "Cb"), "Diminished Unison")
        self.assertEqual(music.diatonic_interval("C", "C"), "Perfect Unison")
        self.assertEqual(music.diatonic_interval("C", "Db"), "Minor Second")
        self.assertEqual(music.diatonic_interval("C", "C#"), "Augmented Unison")
        self.assertEqual(music.diatonic_interval("C", "D"), "Major Second")
        self.assertEqual(music.diatonic_interval("C", "D#"), "Augmented Second")
        self.assertEqual(music.diatonic_interval("C", "Eb"), "Minor Third")
        self.assertEqual(music.diatonic_interval("C", "E"), "Major Third")
        self.assertEqual(music.diatonic_interval("C", "Fb"), "Diminished Fourth")
        self.assertEqual(music.diatonic_interval("C", "F"), "Perfect Fourth")
        self.assertEqual(music.diatonic_interval("C", "F#"), "Augmented Fourth")
        self.assertEqual(music.diatonic_interval("C", "Gb"), "Diminished Fifth")
        self.assertEqual(music.diatonic_interval("C", "G"), "Perfect Fifth")
        self.assertEqual(music.diatonic_interval("C", "G#"), "Augmented Fifth")
        self.assertEqual(music.diatonic_interval("C", "Ab"), "Minor Sixth")
        self.assertEqual(music.diatonic_interval("C", "A"), "Major Sixth")
        self.assertEqual(music.diatonic_interval("C", "A#"), "Augmented Sixth")
        self.assertEqual(music.diatonic_interval("C", "Bb"), "Minor Seventh")
        self.assertEqual(music.diatonic_interval("C", "B"), "Major Seventh")

        self.assertEqual(music.diatonic_interval("G", "A"), "Major Second")
        self.assertEqual(music.diatonic_interval("A", "G"), "Minor Seventh")
        self.assertEqual(music.diatonic_interval("G#", "A"), "Minor Second")
        self.assertEqual(music.diatonic_interval("A", "G#"), "Major Seventh")

        self.assertEqual(music.diatonic_interval("D", "F#"), "Major Third")
        self.assertEqual(music.diatonic_interval("F#", "D"), "Minor Sixth")
        self.assertEqual(music.diatonic_interval("D", "F"), "Minor Third")
        self.assertEqual(music.diatonic_interval("F", "D"), "Major Sixth")


class MatrixTest(unittest.TestCase):
    def setUp(self):
        self.webern_row = [4, 5, 7, 1, 6, 3, 8, 2, 11, 0, 9, 10]
        self.webern_matrix = [[4, 5, 7, 1, 6, 3, 8, 2, 11, 0, 9, 10],
            [3, 4, 6, 0, 5, 2, 7, 1, 10, 11, 8, 9],
            [1, 2, 4, 10, 3, 0, 5, 11, 8, 9, 6, 7],
            [7, 8, 10, 4, 9, 6, 11, 5, 2, 3, 0, 1],
            [2, 3, 5, 11, 4, 1, 6, 0, 9, 10, 7, 8],
            [5, 6, 8, 2, 7, 4, 9, 3, 0, 1, 10, 11],
            [0, 1, 3, 9, 2, 11, 4, 10, 7, 8, 5, 6],
            [6, 7, 9, 3, 8, 5, 10, 4, 1, 2, 11, 0],
            [9, 10, 0, 6, 11, 8, 1, 7, 4, 5, 2, 3],
            [8, 9, 11, 5, 10, 7, 0, 6, 3, 4, 1, 2],
            [11, 0, 2, 8, 1, 10, 3, 9, 6, 7, 4, 5],
            [10, 11, 1, 7, 0, 9, 2, 8, 5, 6, 3, 4]]

    def test_matrix(self):
        self.assertEqual(music.matrix(self.webern_row), self.webern_matrix)

    def test_row_matrix_search(self):
        result = [[9, 3, 5], [3, 7, 0], [5, 0, 4], [10, 11, 9],
                  [7, 5, 1], [8, 9, 7], [0, 1, 2], [11, 8, 3],
                  [2, 6, 11], [6, 10, 8], [1, 4, 6], [4, 2, 10]]

        self.assertEqual(music.row_matrix_search(self.webern_matrix, [0, 1, 3]), result)

    def test_column_matrix_search(self):
        result = [[6, 2, 1], [10, 6, 4], [8, 11, 6], [1, 0, 7],
                  [11, 10, 2], [2, 4, 0], [9, 8, 10], [4, 1, 5],
                  [5, 7, 9], [0, 5, 3], [3, 9, 11], [7, 3, 8]]
        self.assertEqual(music.column_matrix_search(self.webern_matrix, [0, 1, 3]), result)



if __name__ == '__main__':
    unittest.main()

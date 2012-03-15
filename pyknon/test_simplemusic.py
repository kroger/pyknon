from __future__ import division
import unittest
import simplemusic as music


class TestNote(unittest.TestCase):
    def test_mod12(self):
        self.assertEqual(music.mod12(0), 0)
        self.assertEqual(music.mod12(1), 1)
        self.assertEqual(music.mod12(13), 1)
        self.assertEqual(music.mod12(14), 2)

    def test_interval(self):
        self.assertEqual(music.interval(3, 4), 1)
        self.assertEqual(music.interval(4, 3), 11)
        self.assertEqual(music.interval(0, 12), 0)
        self.assertEqual(music.interval(1, 10), 9)
        self.assertEqual(music.interval(10, 1), 3)

    def test_transposition(self):
        n1 = [3, 7, 11, 10]
        n2 = [6, 10, 2, 1]
        self.assertEqual(music.transposition(n1, 3), n2)

    def test_inversion(self):
        n1 = [0, 4, 7]
        n2 = [0, 8, 5]
        self.assertEqual(music.inversion(n1, 0), n2)

    def test_transposition_startswith(self):
        n1 = [3, 7, 11, 10]
        n2 = [4, 8, 0, 11]
        self.assertEqual(music.transposition_startswith(n1, 4), n2)

    def test_inversion_startswith(self):
        n1 = [3, 7, 11, 10]
        n2 = [3, 11, 7, 8]
        self.assertEqual(music.inversion_startswith(n1, 3), n2)

    def test_rotate(self):
        n1 = [0, 1, 3, 7]
        self.assertEqual(music.rotate(n1, 0), n1)
        self.assertEqual(music.rotate(n1, 1), [1, 3, 7, 0])
        self.assertEqual(music.rotate(n1, 2), [3, 7, 0, 1])
        self.assertEqual(music.rotate(n1, 3), [7, 0, 1, 3])
        self.assertEqual(music.rotate(n1, 4), [0, 1, 3, 7])

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

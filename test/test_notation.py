import unittest
from pyknon import notation


class TestNotation(unittest.TestCase):
    def test_parse_accidental(self):
        acc1 = notation.parse_accidental("###")
        acc2 = notation.parse_accidental("bbb")
        acc3 = notation.parse_accidental("")
        self.assertEqual(acc1, 3)
        self.assertEqual(acc2, -3)
        self.assertEqual(acc3, 0)

    def test_parse_octave(self):
        oct1 = notation.parse_octave("'")
        oct2 = notation.parse_octave("''")
        oct3 = notation.parse_octave("")
        oct4 = notation.parse_octave(",")
        oct5 = notation.parse_octave(",,")
        self.assertEqual(oct1, 5)
        self.assertEqual(oct2, 6)
        self.assertEqual(oct3, 5)
        self.assertEqual(oct4, 4)
        self.assertEqual(oct5, 3)

    def test_parse_dur(self):
        dur1 = notation.parse_dur("8")
        dur2 = notation.parse_dur("4")
        dur3 = notation.parse_dur("4", ".")
        dur4 = notation.parse_dur("4", "..")
        dur5 = notation.parse_dur("2")
        self.assertEqual(dur1, 0.125)
        self.assertEqual(dur2, 0.25)
        self.assertEqual(dur3, 0.375)
        self.assertEqual(dur4, 0.4375)
        self.assertEqual(dur5, 0.5)

    def test_parse_note(self):
        note1 = notation.parse_note("C#'")
        note2 = notation.parse_note("C2")
        note3 = notation.parse_note("Cb8,")
        note4 = notation.parse_note("B#16''")
        self.assertEqual(note1, (1, 5, 0.25, 120))
        self.assertEqual(note2, (0, 5, 0.5, 120))
        self.assertEqual(note3, (11, 4, 0.125, 120))
        self.assertEqual(note4, (0, 6, 0.0625, 120))

    def test_parse_notes(self):
        notes1 = notation.parse_notes(["C", "D", "E"])
        notes2 = notation.parse_notes(["Cb4'", "D#8,", "E#16,"])
        list_notes1 = [(0, 5, 0.25, 120), (2, 5, 0.25, 120), (4, 5, 0.25, 120)]
        list_notes2 = [(11, 5, 0.25, 120), (3, 4, 0.125, 120), (5, 4, 0.0625, 120)]
        self.assertEqual(notes1, list_notes1)
        self.assertEqual(notes2, list_notes2)

    def test_parse_notes_dur_dot(self):
        notes1 = notation.parse_notes(["C4.''", "D4..", "E8."])
        list_notes1 = [(0, 6, 0.375, 120), (2, 6, 0.4375, 120), (4, 6, 0.1875, 120)]
        self.assertEqual(notes1, list_notes1)

import unittest
import tempfile
from pyknon.MidiFile import MIDIFile
from pyknon.genmidi import Midi, MidiError
from pyknon.music import NoteSeq, Note, Rest


class TestMidi(unittest.TestCase):
    def test_init(self):
        midi = Midi(1, tempo=120)
        self.assertEqual(midi.number_tracks, 1)
        self.assertIsInstance(midi.midi_data, MIDIFile)

    def test_seq_notes_with_more_tracks_than_exists(self):
        midi = Midi(1)
        with self.assertRaises(MidiError):
            midi.seq_notes(NoteSeq("C D"), track=0)
            midi.seq_notes(NoteSeq("D E"), track=1)

    def test_seq_notes(self):
        midi = Midi(2)
        midi.seq_notes(NoteSeq("C D"), track=0)
        midi.seq_notes(NoteSeq("D E"), track=1)

    def test_seq_chords(self):
        chords = [NoteSeq("C E G"), NoteSeq("G B D")]
        midi = Midi()
        midi.seq_chords(chords)
        
    def test_seq_chords_with_rest(self):
        chords = [Rest(), NoteSeq("G B D")]
        midi = Midi()
        midi.seq_chords(chords)
        

class TestWriteMidi(unittest.TestCase):
    def test_write_midifile(self):
        notes1 = NoteSeq("D4 F#8 R A")
        midi = Midi(1, tempo=133)
        midi.seq_notes(notes1, track=0)
        midi.write(tempfile.TemporaryFile())

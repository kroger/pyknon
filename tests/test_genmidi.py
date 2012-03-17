import unittest
import tempfile
from pyknon.genmidi import Midi
from pyknon.musiclib import NoteSeq, Note


class TestRest(unittest.TestCase):
    def test_write_midifile(self):
        notes1 = NoteSeq("D4 F#8 A")
        midi = Midi(1, tempo=133)
        midi.seq_notes(notes1, track=0)
        midi.write_file(tempfile.TemporaryFile())

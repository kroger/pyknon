#!/usr/bin/env python

from pyknon.genmidi import Midi
from pyknon.musiclib import NoteSeq, Note


def demo():
    notes1 = NoteSeq("D4 F#8 A Bb4")
    notes2 = NoteSeq([Note(2, dur=1), Note(6, dur=0.5),
                      Note(9, dur=0.5), Note(10, dur=1)])
    midi = Midi(2, tempo=90)
    midi.seq_notes(notes1, track=0)
    midi.seq_notes(notes2, track=1)
    midi.write_file("demo.mid")


if __name__ == "__main__":
    demo()

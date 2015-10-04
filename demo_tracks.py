from pyknon.genmidi import Midi
from pyknon.music import NoteSeq

# Notes on two tracks

notes1 = NoteSeq("C4.'' B8' A4 D")
notes2 = NoteSeq("E4 F G4. A8")

m = Midi(2, tempo=100, instrument=[12, 14])
m.seq_notes(notes1, track=0)
m.seq_notes(notes2, track=1)
m.write("tracks.mid")

# Chords on two tracks

chords1 = [NoteSeq("C2 E G"), NoteSeq("G2 B D")]
chords2 = [NoteSeq("C,4 E"), NoteSeq("E, G"), NoteSeq("G, B"), NoteSeq("B, D'")]

midi = Midi(2, tempo=60, instrument=[40, 20])
midi.seq_chords(chords1, track=0)
midi.seq_chords(chords2, track=1)
midi.write("chords.mid")

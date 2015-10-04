from pyknon.genmidi import Midi
from pyknon.music import NoteSeq

# Notes on two tracks using the defaults

notes1 = NoteSeq("C4.'' B8' A4 D")
notes2 = NoteSeq("E4 F G4. A8")

m = Midi(2, tempo=100, instrument=[12, 14])
m.seq_notes(notes1, track=0)
m.seq_notes(notes2, track=1)
m.write("tracks.mid")

# Chords on two tracks using the defaults

chords1 = [NoteSeq("C2 E G"), NoteSeq("G2 B D")]
chords2 = [NoteSeq("C,4 E"), NoteSeq("E, G"), NoteSeq("G, B"), NoteSeq("B, D'")]

midi = Midi(2, tempo=60, instrument=[40, 20])
midi.seq_chords(chords1, track=0)
midi.seq_chords(chords2, track=1)
midi.write("chords.mid")

# Notes on two tracks using percussion

# In the MIDI library, the tracks and channels are numbered from 0,
# While the MIDI Standard is numbered from 1,
# So to use percussion you must use channel 9 in the library

n1 = NoteSeq("C4 D E F")
n2 = NoteSeq("C8 C G, G C' C G, G")

m2 = Midi(2, tempo=123, channel=[0, 9], instrument=[20, 40])
m2.seq_notes(n1, track=0, channel=0)
m2.seq_notes(n2, track=1, channel=9)
m2.write("percussion.mid")


from pyknon.genmidi import Midi
from pyknon.music import NoteSeq

notes1 = NoteSeq("C4 D E F G A B C''")
notes2 = NoteSeq("r1 r1 C4 D E F G A B C''")

table = [
    (60, 261.63), # 261.63
    (62, 280),    # 293.66
    (64, 333),    # 329.63
    (65, 349),    # 349.23
    (67, 391.99), # 391.99
    (69, 444),    # 440.00
    (71, 510),    # 493.88
    (72, 523.25)  # 523.25
]

m = Midi(2, tempo=120)
m.seq_notes(notes1, track=0)
m.seq_notes(notes2, track=1)
m.change_tuning(0, table)
m.write("micro.mid")

from pyknon.MidiFile import MIDIFile
from pyknon.music import Note, NoteSeq


class MidiError(Exception):
    pass


class Midi(object):
    def __init__(self, number_tracks=1, tempo=60, instrument=0):
        """
        instrument: can be an integer or a list
        """

        self.number_tracks = number_tracks
        self.midi_data = MIDIFile(number_tracks)

        for track in range(number_tracks):
            self.midi_data.addTrackName(track, 0, "Track {0}".format(track))
            self.midi_data.addTempo(track, 0, tempo)
            instr = instrument[track] if isinstance(instrument, list) else instrument
            self.midi_data.addProgramChange(track, 0, 0, instr)

    def seq_chords(self, seqlist, track=0, time=0):
        if track + 1 > self.number_tracks:
            raise MidiError("You are trying to use more tracks than we have.")

        for seq in seqlist:
            if isinstance(seq, NoteSeq):
                volume = seq[0].volume
                dur = seq[0].midi_dur
                for note in seq:
                    self.midi_data.addNote(track, 0, note.midi_number, time, dur, volume)
                time += dur
            else:
                raise MidiError("The input should be a list of NoteSeq but yours is a {0}: {1}".format(type(seqlist), seqlist))
        return time

    def seq_notes(self, noteseq, track=0, time=0):
        if track + 1 > self.number_tracks:
            raise MidiError("You are trying to use more tracks than we have.")

        for note in noteseq:
            if isinstance(note, Note):
                self.midi_data.addNote(track, 0, note.midi_number, time, note.midi_dur, note.volume)
            else:
                # we ignore the rests
                pass
            time += note.midi_dur

        return time

    def write(self, filename):
        if isinstance(filename, str):
            with open(filename, 'wb') as midifile:
                self.midi_data.writeFile(midifile)
        else:
            self.midi_data.writeFile(filename)

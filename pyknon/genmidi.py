from pyknon.MidiFile import MIDIFile
from pyknon.music import Note


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

    def seq_notes(self, noteseq, track=0, time=0):
        if track + 1 > self.number_tracks:
            raise MidiError("You are trying to use more tracks than we have.")

        for note in noteseq:
            if isinstance(note, Note):
                self.midi_data.addNote(track, 0, note.midi_number, time, note.midi_dur, note.volume)
            time += note.midi_dur

    def write(self, filename):
        if isinstance(filename, str):
            with open(filename, 'wb') as midifile:
                self.midi_data.writeFile(midifile)
        else:
            self.midi_data.writeFile(filename)

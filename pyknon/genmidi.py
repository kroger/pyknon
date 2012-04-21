from pyknon.MidiFile import MIDIFile
from pyknon import music


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

        for note, octave, dur, volume in noteseq.note_list():
            # The MIDI library uses 1 for quarter note but we use 0.25
            midi_dur = dur * 4
            if note == -1:
                # just skip the rest, the next note will start on the right time
                pass
            else:
                self.midi_data.addNote(track, 0, note + (12 * octave), time, midi_dur, volume)
            time += midi_dur

    def write(self, filename):
        if isinstance(filename, str):
            with open(filename, 'wb') as midifile:
                self.midi_data.writeFile(midifile)
        else:
            self.midi_data.writeFile(filename)

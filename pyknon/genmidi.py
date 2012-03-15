from MidiFile import MIDIFile
import musiclib


DURATIONS = [0.0625, 0.125, 0.25, 0.5, 1, 2, 3, 4]


class Midi(object):
    def __init__(self, number_tracks=1, tempo=60, instrument=0):
        """
        instrument: can be an integer or a list
        """

        self.midi_data = MIDIFile(number_tracks)

        for track in range(number_tracks):
            self.midi_data.addTrackName(track, 0, "Track {0}".format(track))
            self.midi_data.addTempo(track, 0, tempo)
            instr = instrument[track] if isinstance(instrument, list) else instrument
            self.midi_data.addProgramChange(track, 0, 0, instr)

    def seq_notes_same_dur(self, notes, track=0, time=0, dur=0.25):
        for note in notes:
            self.midi_data.addNote(track, 0, note, time, dur, 100)
            time += dur

    def seq_notes(self, notes, track=0, time=0):
        """notes is iterable where every item is (pitch, octave, dur,
        volume) or a NoteSeq instance
        """

        if isinstance(notes, musiclib.NoteSeq):
            note_list = notes.note_list()
        else:
            note_list = notes
            
        for note, octave, dur, volume in note_list:
            if note == -1:
                # just skip the rest, the next note will start on the right time
                pass
            else:
                self.midi_data.addNote(track, 0, note + (12 * octave), time, dur, volume)
            time += dur

    def write_file(self, filename):
        with open(filename, 'wb') as midifile:
            self.midi_data.writeFile(midifile)

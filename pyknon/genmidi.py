from pyknon.MidiFile import MIDIFile
from pyknon.music import Note, NoteSeq, Rest


class MidiError(Exception):
    pass


class Midi(object):
    def __init__(self, number_tracks=1, tempo=60, instrument=0, channel=None):
        """
        instrument: can be an integer or a list
        channel: can be an integer or a list
        """

        self.number_tracks = number_tracks
        self.midi_data = MIDIFile(number_tracks)

        for track in range(number_tracks):
            self.midi_data.addTrackName(track, 0, "Track {0}".format(track))
            self.midi_data.addTempo(track, 0, tempo)
            instr = instrument[track] if isinstance(instrument, list) else instrument
            if channel is None:
                _channel = track
            elif isinstance(channel, list):
                _channel = channel[track]
            else:
                _channel = channel
            self.midi_data.addProgramChange(track, _channel, 0, instr)

    def seq_chords(self, seqlist, track=0, time=0, channel=None):
        if track + 1 > self.number_tracks:
            raise MidiError("You are trying to use more tracks than we have.")

        _channel = channel if channel is not None else track

        for item in seqlist:
            if isinstance(item, NoteSeq):
                volume = item[0].volume
                dur = item[0].midi_dur
                for note in item:
                    self.midi_data.addNote(track, _channel, note.midi_number, time, dur, volume)
                time += dur
            elif isinstance(item, Rest):
                time += item.midi_dur
            else:
                raise MidiError("The input should be a list of NoteSeq but yours is a {0}: {1}".format(type(seqlist), seqlist))
        return time

    def seq_notes(self, noteseq, track=0, time=0, channel=None):
        if track + 1 > self.number_tracks:
            raise MidiError("You are trying to use more tracks than we have.")

        _channel = channel if channel is not None else track

        for note in noteseq:
            if isinstance(note, Note):
                #print note.midi_number, track
                self.midi_data.addNote(track, _channel, note.midi_number, time, note.midi_dur, note.volume)
            else:
                # we ignore the rests
                pass
            time += note.midi_dur

        return time

    def change_tuning(self, track, tunings, real_time=False, tuning_program=0):
        self.midi_data.changeNoteTuning(track, tunings, realTime=real_time, tuningProgam=tuning_program)

    def write(self, filename):
        if isinstance(filename, str):
            with open(filename, 'wb') as midifile:
                self.midi_data.writeFile(midifile)
        else:
            self.midi_data.writeFile(filename)

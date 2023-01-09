from get_chords import extract_chords
from youtube_dl import download, youtube_search
from midiutil import MIDIFile
from mingus.core import chords
import librosa

YOUTUBE_WATCH_STRING = "https://www.youtube.com/watch?v="
"""
Gets the youtube watch link for the first search result of a youtube query
"""
def get_first_result_of_youtube_search(query : str) -> str:
  out = youtube_search(query)
  return YOUTUBE_WATCH_STRING + out[0]["id"]

"""
downloads a youtube link and returns the filepath for this file.
"""
def download_youtube_link(link : str, outpath : str) -> str:
  download(link, outpath)
  return outpath

from typing import Tuple, List
def get_beats_from_mp3(file : str) -> Tuple[int, List[float]]:
  arr, sr = librosa.load(file)
  tempo, beat_track = librosa.beat.beat_track(arr,sr=sr)
  beats = librosa.frames_to_time(beat_track, sr=sr)
  return tempo, beats




NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)

errors = {
    'notes': 'Bad input, please refer this spec-\n'
}


def swap_accidentals(note):
    if note == 'Db':
        return 'C#'
    if note == 'D#':
        return 'Eb'
    if note == 'E#':
        return 'F'
    if note == 'Gb':
        return 'F#'
    if note == 'G#':
        return 'Ab'
    if note == 'A#':
        return 'Bb'
    if note == 'B#':
        return 'C'
    if note == 'Cb':
        return 'B'
    return note


def note_to_number(note: str, octave: int) -> int:
    note = swap_accidentals(note)
    assert note in NOTES, errors['notes']
    assert octave in OCTAVES, errors['notes']

    note = NOTES.index(note)
    note += (NOTES_IN_OCTAVE * octave)

    assert 0 <= note <= 127, errors['notes']

    return note

  
def get_tick_from_timestamp(tempo : int, timestamp : float, ticks_per_quarternote : int) -> int:
    #find ticks / second
    # ticks / second = b/m * m / 60 seconds * 1 quarter note / beat * ticks per quarter note 
    tps = tempo * (1/60) * ticks_per_quarternote
    return round(timestamp * tps)

def create_midi_from_chordchange_array_and_tempo(tempo : float, chords_array : List[Tuple[str, int]]):
    track = 0
    channel = 0
    time = 0  # In beats
    volume = 100  # 0-127, as per the MIDI standard
    ticks_per_quarternote = 240
    MyMIDI = MIDIFile(1, ticks_per_quarternote=ticks_per_quarternote, eventtime_is_ticks=True)
    MyMIDI.addTempo(track, time, round(tempo))
     
    for chord in chords_array:
        print(chord)
        if chord[0] != 'N':
          notes = chords.from_shorthand(chord[0])
          print(notes)
          time = get_tick_from_timestamp(tempo, chord[1], ticks_per_quarternote)
          for note in notes:
              pitch = note_to_number(note, 4)
              MyMIDI.addNote(track, channel, pitch, time, ticks_per_quarternote, volume)
    with open("pure-edm-fire-arpeggio.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)


def get_chord_array_and_tempo(youtube_query : str, download_path : str) -> Tuple[List[List[str, float]], float]:
    """
    Returns a list of chords along with the timestamps they start at and the tempo of the song
    for the first result of the supplied youtube query
    """
    link = get_first_result_of_youtube_search(youtube_query)
    downloaded = download_youtube_link(link, download_path)
    chords_array = extract_chords(downloaded)
    arr = list(chords_array)
    tempo, _  = get_beats_from_mp3(downloaded)
    return [arr, tempo]
    # create_midi_from_chordchange_array_and_tempo(tempo, arr)
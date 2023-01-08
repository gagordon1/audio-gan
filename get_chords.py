from chord_extractor.extractors import Chordino

def extract_chords(path_to_mp3_file : str):
    # Setup Chordino with one of several parameters that can be passed
    chordino = Chordino(roll_on=1)  
    # Run extraction
    chords = chordino.extract(path_to_mp3_file)
    return chords

if __name__ == "__main__":
    # chords = extract_chords('test_audio.mp3')\
    pass

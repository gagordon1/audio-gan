from chord_extractor.extractors import Chordino
from typing import List, Tuple

def extract_chords(path_to_mp3_file : str) -> List[Tuple[str, float]]:
    """Gets chords from an mp3 file

    Args:
        path_to_mp3_file (str): path to the mp3 file

    Returns:
        List[Tuple[str, float]]: list of chords with their shorthand name and timestamp when they start.
    """
    # Setup Chordino with one of several parameters that can be passed
    chordino = Chordino(roll_on=1)  
    # Run extraction
    chords = chordino.extract(path_to_mp3_file)
    return map(lambda x : (x.chord, x.timestamp), chords)

if __name__ == "__main__":
    # chords = extract_chords('test_audio.mp3')\
    pass

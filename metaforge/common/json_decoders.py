from pathlib import Path
from uuid import UUID

def path_decoder(path: str):
    '''
    This decoder returns a pathlib.Path based on a given string representation
    '''
    return Path(path)
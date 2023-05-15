from pathlib import Path

from metaforge.parsers.metaforgeparser import MetaForgeParser

def path_encoder(path: Path):
    '''
    This encoder returns a string representation of a given pathlib.Path value
    '''
    return str(path)

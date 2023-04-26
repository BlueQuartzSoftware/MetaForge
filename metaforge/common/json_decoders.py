from pathlib import Path

def path_decoder(cls):
    '''
    This decoder returns a pathlib.Path based on a given string representation
    '''
    return Path(cls)

def listofpaths_decoder(cls):
    '''
    This decoder returns a pathlib.Path based on a given string representation
    '''
    return [path_decoder(path) for path in cls]
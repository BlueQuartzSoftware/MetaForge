def path_encoder(cls):
    '''
    This encoder returns a string representation of a given pathlib.Path value
    '''
    return str(cls)

def listofpaths_encoder(cls):
    '''
    This encoder returns a string representation of a given pathlib.Path value
    '''
    return [path_encoder(path) for path in cls]

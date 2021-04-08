import os


def dict_to_ht_metadata(metadata_dict):
    """
    Converts the incoming metadata dictionary into a list of metadata json
    objects usable by HyperThought endpoints.

    Parameters
    ----------
    metadata_dict
        The metadata dictionary that will be converted to a list of metadata
        json objects

    Returns
    -------
    List
        The list of metadata json objects usable by HyperThought endpoints.
    """

    for key, value in metadata_dict.items():
        print(key)

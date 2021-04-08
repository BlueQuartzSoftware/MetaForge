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

    # This method still needs to be written!

    # The dictionary of metadata table entries needs to be converted into json that HyperThought can use.

    # Example HyperThought metadata list:
    # [
    #     {
    #         'keyName': 'Key1',
    #         'value': {
    #             'type': 'string',
    #             'link': "I am the first key."
    #         },
    #         'unit': None,
    #         'annotation': "http://www.google.com"
    #     },
    #     {
    #         'keyName': 'RandomNumber',
    #         'value': {
    #             'type': 'string',     # Even though this data is an integer, its type for HyperThought purposes should be set to string
    #             'link': 291001
    #         },
    #         'unit': None,
    #         'annotation': 'A random number'
    #     }
    # ]

    pass

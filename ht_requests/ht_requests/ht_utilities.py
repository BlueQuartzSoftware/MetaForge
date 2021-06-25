import os
import json

from typing import List

from ezmodel.ezmetadatamodel import EzMetadataModel
from ezmodel.ezmetadataentry import EzMetadataEntry



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

    metadataJson = []
    for i in range(len(metadata_dict)):
        if metadata_dict[i]['Default'] == 2:
            metadataJson.append({ 'keyName': metadata_dict[i]['Key'], 'value': {'type': 'string', 'link': metadata_dict[i]['Value']}, 'unit': metadata_dict[i]['Units'], 'annotation': metadata_dict[i]['Annotation']})
        elif metadata_dict[i]['Default'] == 0:
            metadataJson.append(
                { 'keyName': metadata_dict[i]['Key'], 
                   'value': 
                   {
                        'type': 'string', 
                        'link': metadata_dict[i]['HT Value']
                   }, 
                   'unit': metadata_dict[i]['Units'], 
                   'annotation': metadata_dict[i]['Annotation']
                }
                )
    return metadataJson


def ezmodel_to_ht_metadata(model: EzMetadataModel, missing_entries: List[EzMetadataEntry]):
    """

    """

    metadataJson = []
    entries = model.entries
    for e in entries:
        if e.enabled and (e not in missing_entries or e.override_source_value is True):
            metadataJson.append(
                {"keyName": e.ht_name,
                    "value":
                    {
                        "type": "string",
                        "link": e.ht_value
                    },
                    "unit": e.ht_units,
                    "annotation": e.ht_annotation
                }
            )
    return metadataJson


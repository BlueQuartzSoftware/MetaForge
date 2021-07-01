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
            ht_entry = _create_ht_entry(metadata_dict[i]['Key'],
                                        metadata_dict[i]['Value'],
                                        metadata_dict[i]['Units'],
                                        metadata_dict[i]['Annotation'])
            metadataJson.append(ht_entry)
        elif metadata_dict[i]['Default'] == 0:
            ht_entry = _create_ht_entry(metadata_dict[i]['Key'],
                                        metadata_dict[i]['HT Value'],
                                        metadata_dict[i]['Units'],
                                        metadata_dict[i]['Annotation'])
            metadataJson.append(ht_entry)
    return metadataJson


def ezmodel_to_ht_metadata(model: EzMetadataModel,
                           missing_entries: List[EzMetadataEntry],
                           metadata_file_chosen: bool):
    """

    """

    metadataJson = []
    entries = model.entries
    for e in entries:
        if e.enabled:
            if e.source_type is EzMetadataEntry.SourceType.FILE:
                if e.override_source_value is True:
                    ht_entry = _create_ht_entry(e.ht_name, e.ht_value, e.ht_units, e.ht_annotation)
                    metadataJson.append(ht_entry)
                elif e not in missing_entries:
                    if metadata_file_chosen is True:
                        ht_entry = _create_ht_entry(e.ht_name, e.ht_value, e.ht_units, e.ht_annotation)
                    else:
                        ht_entry = _create_ht_entry(e.ht_name, e.source_value, e.ht_units, e.ht_annotation)
                    metadataJson.append(ht_entry)
            elif e.source_type is EzMetadataEntry.SourceType.CUSTOM:
                ht_entry = _create_ht_entry(e.ht_name, e.ht_value, e.ht_units, e.ht_annotation)
                metadataJson.append(ht_entry)
    return metadataJson

def _create_ht_entry(ht_name: str, ht_value: str, ht_units: str, ht_annotation: str):
    return {
                "keyName": ht_name,
                "value":
                        {
                            "type": "string",
                            "link": ht_value
                        },
                "unit": ht_units,
                "annotation": ht_annotation
            }


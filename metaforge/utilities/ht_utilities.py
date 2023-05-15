from typing import List
from hyperthought.metadata import MetadataItem

from metaforge.models.metadatamodel import MetadataModel
from metaforge.models.metadataentry import MetadataEntry

def dict_to_ht_metadata(metadata_dict) -> List[MetadataItem]:
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

    ht_metadata_items: List[MetadataItem] = []
    for i in range(len(metadata_dict)):
        if metadata_dict[i]['Default'] == 2:
            ht_metadata_item = _create_ht_metadata_item(metadata_dict[i]['Key'],
                                        metadata_dict[i]['Value'],
                                        metadata_dict[i]['Units'],
                                        metadata_dict[i]['Annotation'])
            ht_metadata_items.append(ht_metadata_item)
        elif metadata_dict[i]['Default'] == 0:
            ht_metadata_item = _create_ht_metadata_item(metadata_dict[i]['Key'],
                                        metadata_dict[i]['HT Value'],
                                        metadata_dict[i]['Units'],
                                        metadata_dict[i]['Annotation'])
            ht_metadata_items.append(ht_metadata_item)
    return ht_metadata_items


def ezmodel_to_ht_metadata(model: MetadataModel,
                           missing_entries: List[MetadataEntry],
                           metadata_file_chosen: bool) -> List[MetadataItem]:
    """

    """

    ht_metadata_items: List[MetadataItem] = []
    entries = model.entries
    for e in entries:
        if e.enabled:
            if e.source_type is MetadataEntry.SourceType.FILE:
                if e.override_source_value is True:
                    ht_metadata_item = _create_ht_metadata_item(e.ht_name, e.ht_value, e.ht_units, e.ht_annotation)
                    ht_metadata_items.append(ht_metadata_item)
                elif e not in missing_entries:
                    if metadata_file_chosen is True:
                        ht_metadata_item = _create_ht_metadata_item(e.ht_name, e.ht_value, e.ht_units, e.ht_annotation)
                    else:
                        ht_metadata_item = _create_ht_metadata_item(e.ht_name, e.source_value, e.ht_units, e.ht_annotation)
                    ht_metadata_items.append(ht_metadata_item)
            elif e.source_type is MetadataEntry.SourceType.CUSTOM:
                ht_metadata_item = _create_ht_metadata_item(e.ht_name, e.ht_value, e.ht_units, e.ht_annotation)
                ht_metadata_items.append(ht_metadata_item)
    return ht_metadata_items

def _create_ht_metadata_item(ht_name: str, ht_value: str, ht_units: str, ht_annotation: str) -> MetadataItem:
    value_type_name = type(ht_value).__name__
    if value_type_name == 'list':
        s = ', '
        ht_value = '[' + s.join([str(val) for val in ht_value]) + ']'

    return MetadataItem(key=ht_name,
                        value=ht_value,
                        units=ht_units,
                        annotation=ht_annotation)
    # return {
    #             "keyName": ht_name,
    #             "value":
    #                     {
    #                         "type": "string",
    #                         "link": ht_value
    #                     },
    #             "unit": ht_units,
    #             "annotation": ht_annotation
    #         }


from __future__ import annotations
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
import json
from typing import List

from ezmodel.ezmetadataentry import EzMetadataEntry


@dataclass_json
@dataclass
class EzMetadataModel:
    entries: List[EzMetadataEntry] = field(default_factory=list)
    original_data_file: str = ''
    template_version: str = '1.0'

    @staticmethod
    def create_model(model_dict: dict, data_file_path: str, source_type: EzMetadataEntry.SourceType) -> EzMetadataModel:
        model = EzMetadataModel([], original_data_file=data_file_path)
        EzMetadataModel._add_model_entry(model_dict, '', model, source_type)
        return model

    @staticmethod
    def _add_model_entry(item, parent_path: str, model: EzMetadataModel, source_type: EzMetadataEntry.SourceType):
        for key, value in item.items():
            if type(value) is dict:
                new_parent_path = parent_path + key + '/'
                EzMetadataModel._add_model_entry(
                    value, new_parent_path, model, source_type)
            else:
                item_path = parent_path + key
                if value is None:
                    value = ''
                metadata_entry = EzMetadataEntry(source_path=item_path,
                                                 source_value=value,
                                                 source_type=source_type,
                                                 ht_name=key,
                                                 ht_value='',
                                                 ht_annotation='',
                                                 ht_units='')
                model.append(metadata_entry)

    def append(self, entry: EzMetadataEntry):
        self.entries.append(entry)

    def insert(self, entry: EzMetadataEntry, index: int):
        self.entries.insert(index, entry)

    def remove(self, entry: EzMetadataEntry):
        if len(self.entries) > 0:
            self.entries.remove(entry)
            return True
        return False

    def remove_by_index(self, index: int):
        if len(self.entries) > 0:
            del self.entries[index]
            return True
        return False

    def remove_last(self) -> bool:
        if len(self.entries) > 0:
            del self.entries[-1]
            return True
        return False

    def remove_first(self) -> bool:
        if len(self.entries) > 0:
            del self.entries[0]
            return True
        return False

    def entry(self, index: int) -> EzMetadataEntry:
        return self.entries[index]

    def entry_by_source(self, source: str) -> EzMetadataEntry:
        for e in self.entries:
            if e.source_path == source:
                return e
        return None

    def index_from_source(self, source: str) -> int:
        index = 0
        for e in self.entries:
            if e.source_path == source:
                return index
            index = index + 1
        return index

    def to_file_tree_dict(self) -> dict:
        tree_dict = {}

        for entry in self.entries:
            if entry.source_type is not EzMetadataEntry.SourceType.FILE:
                continue

            source_path = entry.source_path
            source_tokens = source_path.split('/')
            tree_obj = tree_dict
            for i in range(len(source_tokens)):
                token = source_tokens[i]
                if token not in tree_obj:
                    if i == len(source_tokens) - 1:
                        tree_obj[token] = entry.source_value
                    else:
                        tree_obj[token] = {}
                tree_obj = tree_obj[token]
        return tree_dict

    def to_json_file(self, file_path: str, indent: int = 4):
        json_string = self.to_json_string(indent=indent)
        with open(file_path, 'w') as outfile:
            outfile.write(json_string)

    def to_json_string(self, indent: int = 4):
        return self.to_json(indent=indent)

    def size(self) -> int:
        return len(self.entries)

    def enabled_count(self) -> int:
        count = 0
        for entry in self.entries:
            if entry.enabled is True:
                count = count + 1
        return count

    @staticmethod
    def from_json_file(file_path: str) -> EzMetadataModel:
        with open(file_path) as json_file:
            json_string = json.load(json_file)
            return EzMetadataModel.from_json_dict(json_string)

    @staticmethod
    def from_json_string(json_string: str) -> EzMetadataModel:
        return EzMetadataModel.from_json(json_string)

    @staticmethod
    def from_json_dict(json: dict) -> EzMetadataModel:
        return EzMetadataModel.from_dict(json)

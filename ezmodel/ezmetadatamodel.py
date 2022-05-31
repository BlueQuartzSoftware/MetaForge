from __future__ import annotations
from ast import parse
from dataclasses import dataclass, field
from email import parser
from dataclasses_json import dataclass_json
import json
from pathlib import Path
from typing import List, Tuple
from uuid import UUID

from ezmodel.ezmetadataentry import EzMetadataEntry

# K_TEMPLATE_VERSION_KEY = 'template_version'
# K_DATA_FILE_KEY = 'data_file_path'
# K_PARSER_UUID_KEY = 'parser_uuid'
# K_MODEL_ENTRIES_KEY = 'entries'

@dataclass_json
@dataclass
class TemplateModel_V1:
    data_file_path: str
    entries: List[EzMetadataEntry] = field(default_factory=list)
    template_version: str = '1.0'
    
    def extract_data(self) -> Tuple[Path, EzMetadataModel]:
        data_file_path = self.data_file_path
        if data_file_path is not None:
            data_file_path = Path(self.data_file_path)

        return data_file_path, EzMetadataModel(entries=self.entries)
    
    @staticmethod
    def from_json_file(file_path: str) -> TemplateModel_V1:
        with open(file_path) as json_file:
            json_string = json.load(json_file)
            return TemplateModel_V1.from_dict(json_string)

@dataclass_json
@dataclass
class TemplateModel_V2:
    data_file_path: str
    parser_uuid: str
    entries: List[EzMetadataEntry] = field(default_factory=list)
    template_version: str = '2.0'

    @staticmethod
    def create_model(data_file_path: str, parser_uuid: UUID, entries: List[EzMetadataEntry]) -> TemplateModel_V2:
        return TemplateModel_V2(data_file_path=data_file_path, parser_uuid=parser_uuid, entries=entries)
    
    def extract_data(self) -> Tuple[Path, UUID, EzMetadataModel]:
        data_file_path = self.data_file_path
        if data_file_path is not None:
            data_file_path = Path(self.data_file_path)
        
        parser_uuid = self.parser_uuid
        if parser_uuid is not None:
            parser_uuid = UUID(self.parser_uuid)
        return data_file_path, parser_uuid, EzMetadataModel(entries=self.entries)
    
    def to_json_file(self, file_path: str, indent: int = 4):
        json_string = self.to_json(indent=indent)
        with open(file_path, 'w') as outfile:
            outfile.write(json_string)
    
    @staticmethod
    def from_json_file(file_path: str) -> TemplateModel_V2:
        with open(file_path) as json_file:
            json_string = json.load(json_file)
            return TemplateModel_V2.from_dict(json_string)

# This is an alias used throughout the project to access the current EzMetadataModelIO class
TemplateModel = TemplateModel_V2

@dataclass_json
@dataclass
class EzMetadataModel:
    entries: List[EzMetadataEntry] = field(default_factory=list)

    @staticmethod
    def create_model_from_dict(model_dict: dict, source_type: EzMetadataEntry.SourceType) -> EzMetadataModel:
        model = EzMetadataModel()
        if model_dict is not None:
            model.add_model_entry(item=model_dict, parent_path='', source_type=source_type)
        return model

    def add_model_entry(self, item, parent_path: str, source_type: EzMetadataEntry.SourceType):
        for key, value in item.items():
            if type(value) is dict:
                new_parent_path = parent_path + key + '/'
                self.add_model_entry(item=value, parent_path=new_parent_path, source_type=source_type)
            else:
                item_path = parent_path + key
                if value is None:
                    value = ''
                metadata_entry = EzMetadataEntry(source_path=item_path,
                                                 source_value=value,
                                                 source_type=source_type,
                                                 ht_name=key,
                                                 ht_value=value,
                                                 ht_annotation='',
                                                 ht_units='')
                self.entries.append(metadata_entry)

    def update_model_values_from_dict(self, item: dict, parent_path: str = "") -> List[EzMetadataEntry]:
        visited = [False for _ in range (self.size())]
        self._update_model_values_from_dict(item, parent_path, visited)

        missing_entries: List[EzMetadataEntry] = []
        for i in range(len(visited)):
            metadata_entry: EzMetadataEntry = self.entries[i]
            if visited[i] == False and metadata_entry.source_type == EzMetadataEntry.SourceType.FILE and metadata_entry.enabled:
                missing_entries.append(metadata_entry)
            
        return missing_entries
    
    def _update_model_values_from_dict(self, item: dict, parent_path: str = "", visited: list = []):
        for key, value in item.items():
            if type(value) is dict:
                new_parent_path = parent_path + key + '/'
                self._update_model_values_from_dict(value, new_parent_path, visited)
            else:
                item_path = parent_path + key
                entry = self.entry_by_source(item_path)
                
                idx = self.index_from_source(item_path)
                if idx >= 0:
                    visited[idx] = True

                if entry is not None and entry.override_source_value is False:
                    entry.ht_value = value


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
        if index < 0 or index >= len(self.entries):
            return None
        return self.entries[index]

    def entry_by_source(self, source: str) -> EzMetadataEntry:
        for e in self.entries:
            if e.source_path == source:
                return e
        return None

    def index_from_source(self, source: str) -> int:
        for i in range(len(self.entries)):
            e = self.entries[i]
            if e.source_path == source:
                return i
        return -1

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

    def size(self) -> int:
        return len(self.entries)

    def enabled_count(self) -> int:
        count = 0
        for entry in self.entries:
            if entry.enabled is True:
                count = count + 1
        return count
    
    def to_json_file(self, file_path: str, indent: int = 4):
            json_string = self.to_json(indent=indent)
            with open(file_path, 'w') as outfile:
                outfile.write(json_string)

    @staticmethod
    def from_json_file(file_path: str) -> EzMetadataModel:
        with open(file_path) as json_file:
            json_string = json.load(json_file)
            return EzMetadataModel.from_dict(json_string)

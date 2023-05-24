from __future__ import annotations
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
import json
from pathlib import Path
from typing import List, Tuple, Optional
from uuid import UUID

from metaforge.parsers.metaforgeparser import MetaForgeMetadata
from metaforge.models.metadataentry import MetadataEntry

@dataclass_json
@dataclass
class TemplateModel_V1:
    data_file_path: str
    entries: List[MetadataEntry] = field(default_factory=list)
    template_version: str = '1.0'
    
    def extract_data(self) -> Tuple[Path, MetadataModel]:
        data_file_path = self.data_file_path
        if data_file_path is not None:
            data_file_path = Path(self.data_file_path)

        return data_file_path, MetadataModel(entries=self.entries)
    
    @staticmethod
    def from_json_file(file_path: str) -> TemplateModel_V1:
        with open(file_path) as json_file:
            json_string = json.load(json_file)
            return TemplateModel_V1.from_dict(json_string)

@dataclass_json
@dataclass
class TemplateModel_V2:
    data_file_path: str
    parser_uuid: Optional[str]
    entries: List[MetadataEntry] = field(default_factory=list)
    template_version: str = '2.0'

    @staticmethod
    def create_model(data_file_path: str, parser_uuid: UUID, entries: List[MetadataEntry]) -> TemplateModel_V2:
        return TemplateModel_V2(data_file_path=data_file_path, parser_uuid=parser_uuid, entries=entries)
    
    def extract_data(self) -> Tuple[Path, UUID, MetadataModel]:
        data_file_path = self.data_file_path
        if data_file_path is not None:
            data_file_path = Path(self.data_file_path)
        
        parser_uuid = self.parser_uuid
        if parser_uuid is not None:
            parser_uuid = UUID(self.parser_uuid)
        return data_file_path, parser_uuid, MetadataModel(entries=self.entries)
    
    def to_json_file(self, file_path: str, indent: int = 4):
        json_string = self.to_json(indent=indent)
        with open(file_path, 'w') as outfile:
            outfile.write(json_string)
    
    @staticmethod
    def from_json_file(file_path: str) -> TemplateModel_V2:
        with open(file_path) as json_file:
            json_string = json.load(json_file)
            return TemplateModel_V2.from_dict(json_string)

# This is an alias used throughout the project to access the current MetadataModelIO class
TemplateModel = TemplateModel_V2

@dataclass_json
@dataclass
class MetadataModel:
    entries: List[MetadataEntry] = field(default_factory=list)

    @staticmethod
    def create_model(model_list: List[MetaForgeMetadata], source_type: MetadataEntry.SourceType) -> MetadataModel:
        model = MetadataModel()
        if model_list is not None:
            for metadata in model_list:
                if metadata.value is None:
                    metadata.value = ''
                metadata_entry = MetadataEntry(source_path=metadata.source_path,
                                                    source_value=metadata.value,
                                                    source_type=source_type,
                                                    ht_name=Path(metadata.source_path).stem,
                                                    ht_value=metadata.value,
                                                    ht_annotation=metadata.annotations,
                                                    ht_units=metadata.units)
                model.entries.append(metadata_entry)
        return model

    def update_model_values(self, metadata_list: List[MetaForgeMetadata]) -> List[MetadataEntry]:
        visited = [False for _ in range (self.size())]
        self._update_model_values(metadata_list, visited)

        missing_entries: List[MetadataEntry] = []
        for i in range(len(visited)):
            metadata_entry: MetadataEntry = self.entries[i]
            if visited[i] == False and metadata_entry.source_type == MetadataEntry.SourceType.FILE and metadata_entry.enabled:
                missing_entries.append(metadata_entry)
            
        return missing_entries
    
    def _update_model_values(self, metadata_list: List[MetaForgeMetadata], visited: list = []):
        for metadata in metadata_list:            
            idx = self.index_from_source(metadata.source_path)
            if idx >= 0:
                visited[idx] = True

            entry = self.entry_by_source(metadata.source_path)
            if entry is not None:
                if entry.override_source_value is False:
                    entry.ht_value = metadata.value
                    entry.ht_annotation = metadata.annotations
                    entry.ht_units = metadata.units


    def append(self, entry: MetadataEntry):
        self.entries.append(entry)

    def insert(self, entry: MetadataEntry, index: int):
        self.entries.insert(index, entry)

    def remove(self, entry: MetadataEntry):
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

    def entry(self, index: int) -> MetadataEntry:
        if index < 0 or index >= len(self.entries):
            return None
        return self.entries[index]

    def entry_by_source(self, source: str) -> MetadataEntry:
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
    def from_json_file(file_path: str) -> MetadataModel:
        with open(file_path) as json_file:
            json_string = json.load(json_file)
            return MetadataModel.from_dict(json_string)

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
import json
from pathlib import Path
from typing import List

from metaforge.ez_models.ezparserdirectory import EzParserDirectory
from metaforge.utilities.parser_utilities import create_parser_directory

@dataclass_json
@dataclass
class EzParserDirectoriesModel:
    parser_directories: List[EzParserDirectory] = field(default_factory=list)

    def append(self, parser_dir_path: Path):
        parser_directory = create_parser_directory(parser_dir_path)
        self.parser_directories.append(parser_directory)
    
    def append_directory(self, parser_dir: EzParserDirectory):
        self.parser_directories.append(parser_dir)

    def insert(self, index: int, parser_dir_path: Path):
        parser_directory = create_parser_directory(parser_dir_path)
        self.parser_directories.insert(index, parser_directory)
    
    def insert_directory(self, index: int, parser_dir: EzParserDirectory):
        self.parser_directories.insert(index, parser_dir)

    def remove(self, parser_dir: Path):
        for parser_directory in self.parser_directories:
            if parser_directory.directory_path == parser_dir:
                self.parser_directories.remove(parser_directory)
                return True
        return False

    def remove_by_index(self, index: int):
        if len(self.parser_directories) > 0:
            del self.parser_directories[index]
            return True
        return False

    def remove_last(self) -> bool:
        if len(self.parser_directories) > 0:
            del self.parser_directories[-1]
            return True
        return False

    def remove_first(self) -> bool:
        if len(self.parser_directories) > 0:
            del self.parser_directories[0]
            return True
        return False

    def directory(self, index: int) -> EzParserDirectory:
        if index < 0 or index >= len(self.parser_directories):
            return None
        return self.parser_directories[index]
    
    def directory_from_path(self, path: Path) -> EzParserDirectory:
        return next((parser_directory for parser_directory in self.parser_directories if parser_directory.directory_path == path), None)

    def index_from_directory(self, directory: EzParserDirectory) -> int:
        for i in range(len(self.parser_directories)):
            dir = self.parser_directories[i]
            if self.parser_directories[i] == directory:
                return i
        return -1

    def size(self) -> int:
        return len(self.parser_directories)
    
    def to_json_file(self, file_path: str, indent: int = 4):
            json_string = self.to_json(indent=indent)
            with open(file_path, 'w') as outfile:
                outfile.write(json_string)

    @staticmethod
    def from_json_file(file_path: str) -> "EzParserDirectoriesModel":
        with open(file_path) as json_file:
            json_string = json.load(json_file)
            return EzParserDirectoriesModel.from_dict(json_string)

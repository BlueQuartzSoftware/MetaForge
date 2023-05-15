import json
from pathlib import Path
from typing import List, Tuple
from uuid import UUID

from metaforge.parsers.metaforgeparser import MetaForgeParser
from metaforge.models.parsermodelitem import ParserModelItem
from metaforge.utilities.parser_utilities import load_parser_module
from metaforge.parsers.default_parser_paths import K_DEFAULT_PARSER_PATHS

class ParserModel:
    def __init__(self):
      super().__init__()
      self.parser_metadata_list: List[ParserModelItem] = []
      self.parsers: List[MetaForgeParser] = []
      self.messages: List[str] = []

      # Load the default parsers
      for default_parser_path in K_DEFAULT_PARSER_PATHS:
          self.append(ParserModelItem(default_parser_path, True, True))

    def append(self, parser_metadata: ParserModelItem):
        result = load_parser_module(parser_metadata.parser_path)
        self.parser_metadata_list.append(parser_metadata)
        self.parsers.append(result[1])
        self.messages.append(result[0])

    def insert(self, index: int, parser_metadata: ParserModelItem) -> str:
        result = load_parser_module(parser_metadata.parser_path)
        self.parser_metadata_list.insert(index, parser_metadata)
        self.parsers.append(result[1])
        self.messages.append(result[0])

    def remove_by_parser(self, parser: MetaForgeParser):
        for idx in range(len(self.parsers)):
            if self.parsers[idx] is not None and self.parsers[idx] == parser:
                del self.parser_metadata_list[idx]
                del self.parsers[idx]
                del self.messages[idx]
                return True
        return False

    def remove_by_file_path(self, parser_file_path: Path) -> bool:
        for idx in range(len(self.parser_metadata_list)):
            if self.parser_metadata_list[idx] is not None and self.parser_metadata_list[idx].parser_path == parser_file_path:
                del self.parser_metadata_list[idx]
                del self.parsers[idx]
                del self.messages[idx]
                return True
        return False

    def remove_by_uuid(self, uuid: UUID):
        for idx in range(len(self.parsers)):
            if self.parsers[idx] is not None and self.parsers[idx].uuid() == uuid:
                del self.parser_metadata_list[idx]
                del self.parsers[idx]
                del self.messages[idx]
                return True
        return False

    def remove_by_index(self, index: int):
        if len(self.parser_metadata_list) > 0:
            del self.parser_metadata_list[index]
            del self.parsers[index]
            del self.messages[index]
            return True
        return False

    def remove_last(self) -> bool:
        if len(self.parser_metadata_list) > 0:
            del self.parser_metadata_list[-1]
            del self.parsers[-1]
            del self.messages[-1]
            return True
        return False

    def remove_first(self) -> bool:
        if len(self.parser_metadata_list) > 0:
            del self.parser_metadata_list[0]
            del self.parsers[0]
            del self.messages[0]
            return True
        return False

    def reload_parser(self, index: int):
        metadata = self.parser_metadata_list[index]
        result = load_parser_module(metadata.parser_path)
        self.parsers[index] = result[1]
        self.messages[index] = result[0]
    
    def clear(self):
        self.parser_metadata_list.clear()
        self.parsers.clear()
        self.messages.clear()

    def parser_path(self, index: int) -> Path:
        if index < 0 or index >= len(self.parser_metadata_list):
            return None
        return self.parser_metadata_list[index].parser_path

    def parser(self, index: int) -> MetaForgeParser:
        if index < 0 or index >= len(self.parser_metadata_list):
            return None
        return self.parsers[index]
    
    def is_default(self, index: int) -> bool:
        if index < 0 or index >= len(self.parser_metadata_list):
            return None
        return self.parser_metadata_list[index].default
    
    def set_default(self, index: int, default: bool) -> bool:
        if index < 0 or index >= len(self.parser_metadata_list):
            return False
        self.parser_metadata_list[index].default = default
        return True

    def is_enabled(self, index: int) -> bool:
        if index < 0 or index >= len(self.parser_metadata_list):
            return None
        return self.parser_metadata_list[index].enabled
    
    def set_enabled(self, index: int, enabled: bool) -> bool:
        if index < 0 or index >= len(self.parser_metadata_list):
            return False
        self.parser_metadata_list[index].enabled = enabled
        return True
    
    def message(self, index: int) -> str:
        if index < 0 or index >= len(self.parser_metadata_list):
            return None
        return self.messages[index]

    def find_parser_from_uuid(self, uuid: UUID) -> Tuple[MetaForgeParser, str]:
      if uuid is None:
        return None, f"Unable to find a parser using UUID - The given UUID is set to None!"

      if self.size() == 0:
        return None, f"Unable to find a parser using UUID '{str(uuid)}' - No parsers are loaded!"

      for parser in self.parsers:
        if parser is not None and parser.uuid() == uuid:
            return parser, None

      return None, f"Unable to find a parser using UUID - The UUID '{str(uuid)}' does not match any of the currently loaded parsers!"
        
    def find_parser_from_data_path(self, file_path: Path) -> Tuple[MetaForgeParser, str]: 
      if file_path == None:
        return None, "Unable to find a compatible parser - The given file path is set to None!"
      
      if self.size() == 0:
        return None, f"Unable to find a compatible parser for data file '{str(file_path)}' - No parsers are loaded!"

      for parser in self.parsers:
        if parser is not None and parser.accepts_extension(file_path.suffix):
          return parser, None
      
      return None, f"Unable to find a compatible parser for data file '{str(file_path)}' - The file path is not compatible with any of the currently loaded parsers!"

    def index_from_parser_path(self, parser_path: Path) -> int:
        for i in range(len(self.parser_metadata_list)):
            ez_parser = self.parser_metadata_list[i]
            if ez_parser.parser_path == parser_path:
                return i
        return -1

    def index_from_parser(self, parser: MetaForgeParser) -> int:
        if parser is None:
            return -1

        for i in range(len(self.parsers)):
            internal_parser = self.parsers[i]
            if internal_parser == parser:
                return i
        return -1
    
    def index_from_parser_uuid(self, parser_uuid: UUID) -> int:
        for i in range(len(self.parsers)):
            parser = self.parsers[i]
            if parser is not None and parser.uuid() == parser_uuid:
                return i
        return -1

    def size(self) -> int:
        return len(self.parser_metadata_list)
    
    def to_json(self, indent: int = 4):
        metadata_dict = [metadata.to_dict() for metadata in self.parser_metadata_list]
        return json.dumps(metadata_dict)

    @staticmethod
    def from_json(json_string: str):
        model = ParserModel()
        metadata_dict = json.loads(json_string)
        json_parser_metadata_list: List[ParserModelItem] = [ParserModelItem.from_dict(mc_dict) for mc_dict in metadata_dict]

        for json_parser_metadata in json_parser_metadata_list:
            if json_parser_metadata.default == True:
                ParserModel._load_default_json_parser(json_parser_metadata, model.parser_metadata_list)
            else:
                # This is not a default parser, add it to the model
                model.append(json_parser_metadata)

        return model
    
    @staticmethod
    def _load_default_json_parser(json_parser_metadata: ParserModelItem, current_metadata_list: List[ParserModelItem]):
        for current_parser_metadata in current_metadata_list:
            if current_parser_metadata.default == False:
                # This isn't a default parser, so skip
                continue
            
            # Compare relative paths to make sure that we have the right default parser from the json
            json_relative_path = json_parser_metadata.parser_path.relative_to(json_parser_metadata.parser_path.parent.parent.parent)
            current_relative_path = current_parser_metadata.parser_path.relative_to(current_parser_metadata.parser_path.parent.parent.parent)
            if json_relative_path == current_relative_path:
                # Update the default parser
                current_parser_metadata.enabled = json_parser_metadata.enabled
                return
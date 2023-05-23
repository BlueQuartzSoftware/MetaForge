from typing import List
from pathlib import Path
from uuid import UUID

import os
import json

from metaforge.parsers.metaforgeparser import MetaForgeParser, MetaForgeMetadata

class JsonParser(MetaForgeParser):
  def __init__(self) -> None:
    self.ext_list: list = ['.json']
    self.file_dict: object = {}

  def human_label(self) -> str:
    return "JSON Parser"

  def version(self) -> str:
    return '1.0'

  def uuid(self) -> UUID:
    return UUID('{7420a76b-f0de-4fb1-a932-b6cb969fa666}')

  def supported_file_extensions(self) -> list:
    return self.ext_list
  
  def accepts_extension(self, extension: str) -> bool:
    return extension in self.ext_list

  def visit_entry(self, prefix: str, data: dict) -> None:
    # Do the right thing depending on the type we see, recursion for dicts.
    if isinstance(data, dict):
      for v in data:
        self.visit_entry(f'{prefix}/{v}', data[v])
    elif isinstance(data, str):
      self.file_dict[prefix] = data
    elif isinstance(data, int):
      self.file_dict[prefix] = str(data)
    elif isinstance(data, float):
      self.file_dict[prefix] = str(data)
    elif isinstance(data, list):
      # Magic number of 16, don't include long lists.
      if len(data) <= 16:
        self.file_dict[prefix] = str(data)

  def parse_header(self, filepath: Path) -> List[MetaForgeMetadata]:
    """
    Description:

    Parameters
    ----------
    filepath
        The path to the JSON file to be parsed

    Returns
    -------
    Dictionary
        A dictionary containing the JSON information
    
    Example
    -------
    ```
    parser = JsonParser()
    parser.parse_header('/some/path/to/a/file.json')
    ```
    """
    # Check our file exists before trying to open it!
    if not os.path.isfile(filepath):
      return self.file_dict
    
    with open(filepath, 'r') as json_file:
      data = json.load(json_file)
      for v in data:
        self.current_path = v
        self.visit_entry(v, data[v])

    return [MetaForgeMetadata(source_path, value) for source_path, value in self.file_dict.items()]
from parsers.metaforgeparser import MetaForgeParser
from typing import List
from pathlib import Path
from uuid import UUID

import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

from parsers.metaforgeparser import MetaForgeParser

class XmlParser(MetaForgeParser):
  def __init__(self) -> None:
    self.ext_list: list = ('.xml')
    self.count: int = 0
    self.file_dict: object = {}
    self.json_data: object = {}
    self.current_path: str = ''

  def human_label(self) -> str:
    return "XML Parser"

  def version(self) -> str:
    return '1.0'

  def uuid(self) -> UUID:
    return UUID('{7420a76b-f0de-4fb1-a932-b6cd969fa666}')

  def supported_file_extensions(self) -> list:
    return self.ext_list

  def accepts_extension(self, extension: str) -> bool:
    return extension in self.ext_list

  def visit_dict(self, prefix: str, data: dict) -> None:
    # Do the right thing depending on the type we see, recursion for dicts.
    if isinstance(data, dict):
      # Skip keys that already exist
      for v in data:
        self.visit_dict(f'{prefix}/{v}', data[v])
    elif isinstance(data, str):
      self.file_dict[f'{prefix}*'] = data
    elif isinstance(data, int):
      self.file_dict[f'{prefix}*'] = str(data)
    elif isinstance(data, float):
      self.file_dict[f'{prefix}*'] = str(data)
    elif isinstance(data, list):
      # Magic number of 16, don't include long lists.
      if len(data) <= 16:
        self.file_dict[f'{prefix}*'] = str(data)

  def visit_entry(self, prefix: str, data: Element) -> None:
    # Do the right thing depending on the type we see, recursion for dicts.
    if isinstance(data, Element):
      for v in data:
        self.visit_entry(f'{prefix}/{v.tag}', v)

    if prefix in self.file_dict:
      return
    self.file_dict[prefix] = data.text
    if len(data.attrib) > 0:
      self.visit_dict(prefix, data.attrib)

  def parse_header_as_dict(self, filepath: Path) -> dict:
    """
    Description:

    Parameters
    ----------
    filepath
        The path to the XML file to be parsed

    Returns
    -------
    Dictionary
        A dictionary containing the XML information

    Example
    -------
    ```
    parser = XmlParser()
    parser.parse_header_as_dict('/some/path/to/a/file.xml')
    ```
    """
    # Check our file exists before trying to open it!
    if not os.path.isfile(filepath):
      return self.file_dict

    tree = ET.parse(str(filepath))
    root = tree.getroot()
    self.visit_entry(root.tag, root)

    return self.file_dict


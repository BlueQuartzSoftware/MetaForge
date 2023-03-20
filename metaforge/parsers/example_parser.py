
from typing import List
from uuid import UUID

from metaforge.parsers.metaforgeparser import MetaForgeParser

class ExampleParser(MetaForgeParser):
  def __init__(self) -> None:
    self.ext_list: list = ()

  def human_label(self) -> str:
    return "WHAT YOUR PARSER SHOWS TO THE GUI AS."

  def version(self) -> str:
    return 'PICK A VERSION FOR YOUR PARSER'
  
  def uuid(self) -> UUID:
    return 'GENERATE A UUID FOR YOUR PARSER'

  def supported_file_extensions(self) -> list:
    return self.ext_list
  
  def accepts_extension(self, extension: str) -> bool:
    if extension in self.ext_list:
      return True
    return False

  def parse_header_as_dict(self, filepath: str) -> dict:
    """
    Description:

    Parameters
    ----------
    filepath
        The path to the ini file to be parsed

    Returns
    -------
    Dictionary
        A dictionary containing the header information
    
    Example
    -------
    ```
    parser = ExampleParser()
    parser.parse_header_as_dict('/some/path/to/a/file.ini')
    ```
    This code returns:
    ```
    
    ```

    """
    header = {}
    file_dict = {"SOURCE": header}

    return file_dict


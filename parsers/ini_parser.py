import configparser
from parsers.metaforgeparser import MetaForgeParser
from typing import List

from parsers.metaforgeparser import MetaForgeParser

from PIL import Image
from PIL.TiffTags import TAGS

class IniParser(MetaForgeParser):
  def __init__(self) -> None:
    self.ext_list: list = ('.ini', '.config', '.txt', '.hdr')

  def human_label(self) -> str:
    return "Ini Parser"

  def version(self) -> str:
    return '1.0'

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
    parser = IniParser()
    parser.parse_header_as_dict('/some/path/to/a/file.ini')
    ```
    This code returns:
    ```
    
    ```

    """
    config = configparser.ConfigParser()
    header = config._sections
    try:
      config.read(filepath)
      header = config._sections
    except (configparser.NoSectionError, configparser.MissingSectionHeaderError):
        pass
    finally:
      file_dict = {"SOURCE": header}

    return file_dict


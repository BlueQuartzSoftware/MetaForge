import configparser

from requests.api import head
from parsers.metaforgeparser import MetaForgeParser
from typing import List

from parsers.metaforgeparser import MetaForgeParser

from PIL import Image
from PIL.TiffTags import TAGS

class FeiTiffParser(MetaForgeParser):
  def __init__(self) -> None:
    self.ext_list: list = ('.tif', '.tiff')

  def human_label(self) -> str:
    return "FEI Tiff Parser"

  def version(self) -> str:
    return '1.0'

  def supported_file_extensions(self) -> list:
    return self.ext_list
  
  def accepts_extension(self, extension: str) -> bool:
    if extension in self.ext_list:
      return True
    return False

  def parse_tiff_tag_34681(self, filepath: str) -> dict:
    """
    This function parses out the FEI Tiff Tag 34681 which is stored as an INI formatted string.

    This Tiff Tag appears in older FEI Tiff Files

    Parameters
    ----------
    filepath
        The path to the tiff image to be parsed

    Returns
    -------
    Dictionary
        A dictionary containing the header information
    """
    config = configparser.ConfigParser()
    try:
      with Image.open(filepath) as img:
        fei_offset = img.tag_v2.get(34681)
        if fei_offset:
          feiTag = img.tag[34681]
          if feiTag[0] is not None:
            feiTagStr = feiTag[0]
            if len(feiTagStr) > 0:
              config.read_string(feiTagStr)
    finally:
      return config._sections

  def parse_tiff_tag_34682(self, filepath: str) -> dict:
    """
    This function parses out the FEI Tiff Tag 34682 which is stored as an INI formatted string

    Parameters
    ----------
    filepath
        The path to the tiff image to be parsed

    Returns
    -------
    Dictionary
        A dictionary containing the header information
    """
    config = configparser.ConfigParser()
    try:
      with Image.open(filepath) as img:
        fei_offset = img.tag_v2.get(34682)
        if fei_offset:
          feiTag = img.tag[34682]
          if feiTag[0] is not None:
            feiTagStr = feiTag[0]
            if len(feiTagStr) > 0:
              config.read_string(feiTagStr)
    finally:
      return config._sections

  def parse_tiff_tag_50431(self, filepath: str) -> dict:
    """
    This function parses out the TESCAN Tiff Tag 50431. Part of the tag is a binary file probably of
    the Jasper Format. There is some ASCII text towards the end of the array which is duplicated in the
    sidecar file.

    Parameters
    ----------
    filepath
        The path to the tiff image to be parsed

    Returns
    -------
    Dictionary
        A dictionary containing the header information
    """
    config = configparser.ConfigParser()
    return config._sections

    # try:
    #   with Image.open(filepath) as img:
        
    #     fei_offset = img.tag_v2[50431]
    #     if fei_offset:
    #       feiTag = img.tag[50431]
    #       if feiTag[0] is not None:
    #         feiTagStr = feiTag
    #         if len(feiTagStr) > 0:
    #           print(feiTagStr)
    # finally:
    #   return config._sections


  def parse_header_as_dict(self, filepath: str) -> dict:
    """
    Description:

    Parameters
    ----------
    filepath
        The path to the tiff image to be parsed

    Returns
    -------
    Dictionary
        A dictionary containing the header information
    
    Example
    -------
    ```
    
    ```
    This code returns:
    ```
    
    ```

    """

    header = self.parse_tiff_tag_34681(filepath)
    if len(header) > 0:
      file_dict = {"SOURCE": header}
      return file_dict

    header = self.parse_tiff_tag_34682(filepath)
    if len(header) > 0:
      file_dict = {"SOURCE": header}
      return file_dict

    header = self.parse_tiff_tag_50431(filepath)
    if len(header) > 0:
      file_dict = {"SOURCE": header}
      return file_dict

    file_dict = {"SOURCE": header}
    return file_dict
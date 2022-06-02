import configparser

from requests.api import head
from parsers.metaforgeparser import MetaForgeParser
from typing import List
from pathlib import Path
from uuid import UUID

from parsers.metaforgeparser import MetaForgeParser

from PIL import Image
from PIL.TiffTags import TAGS

class FeiTiffParser(MetaForgeParser):
  K_FEI_TAGS = [34681, 34682, 50431]

  def __init__(self) -> None:
    self.ext_list: list = ('.tif', '.tiff')

  def human_label(self) -> str:
    return "FEI Tiff Parser"

  def version(self) -> str:
    return '1.0'

  def uuid(self) -> UUID:
    return UUID('{efa0897c-1900-4ce7-854f-61b97722f718}')

  def supported_file_extensions(self) -> list:
    return self.ext_list
  
  def accepts_extension(self, extension: str) -> bool:
    if extension in self.ext_list:
      return True
    return False

  def parse_tiff_tag_34681(self, filepath: Path) -> dict:
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
      with Image.open(str(filepath)) as img:
        fei_offset = img.tag_v2.get(self.K_FEI_TAGS[0])
        if fei_offset:
          feiTag = img.tag[self.K_FEI_TAGS[0]]
          if feiTag[0] is not None:
            feiTagStr = feiTag[0]
            if len(feiTagStr) > 0:
              config.read_string(feiTagStr)
    finally:
      return config._sections

  def parse_tiff_tag_34682(self, filepath: Path) -> dict:
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
      with Image.open(str(filepath)) as img:
        fei_offset = img.tag_v2.get(self.K_FEI_TAGS[1])
        if fei_offset:
          feiTag = img.tag[self.K_FEI_TAGS[1]]
          if feiTag[0] is not None:
            feiTagStr = feiTag[0]
            if len(feiTagStr) > 0:
              config.read_string(feiTagStr)
    finally:
      return config._sections

  def parse_tiff_tag_50431(self, filepath: Path) -> dict:
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
    #   with Image.open(str(filepath)) as img:
        
    #     fei_offset = img.tag_v2[50431]
    #     if fei_offset:
    #       feiTag = img.tag[50431]
    #       if feiTag[0] is not None:
    #         feiTagStr = feiTag
    #         if len(feiTagStr) > 0:
    #           print(feiTagStr)
    # finally:
    #   return config._sections

  def parse_standard_tags(self, filepath: Path) -> dict:
    """
    This function parses out all tags that are not FEI tags

    Parameters
    ----------
    filepath
        The path to the tiff image to be parsed

    Returns
    -------
    Dictionary
        A dictionary containing the header information
    """

    with Image.open(str(filepath)) as img:
      meta_dict = {}
      for tag_key in img.tag.keys():
        if tag_key not in self.K_FEI_TAGS:
          metadata_key = TAGS[tag_key]
          tag = img.tag[tag_key]
          if tag[0] is not None:
              metadata_value = tag[0]
              meta_dict[metadata_key] = metadata_value
      return meta_dict


  def parse_header_as_dict(self, filepath: Path) -> dict:
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

    file_dict = {}

    header = self.parse_tiff_tag_34681(filepath)
    if len(header) > 0:
      file_dict["FEI Tag #34681"] = header

    header = self.parse_tiff_tag_34682(filepath)
    if len(header) > 0:
      file_dict["FEI Tag #34682"] = header

    header = self.parse_tiff_tag_50431(filepath)
    if len(header) > 0:
      file_dict["FEI Tag #50431"] = header

    header = self.parse_standard_tags(filepath)
    if len(header) > 0:
      file_dict["Standard"] = header

    return file_dict

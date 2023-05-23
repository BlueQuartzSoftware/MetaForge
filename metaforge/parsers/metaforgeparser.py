from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Any
from pathlib import Path
from uuid import UUID

class MetaForgeMetadata:
  def __init__(self, source_path: str, value: Any, annotations: str = '', units: str = '') -> None:
      self.source_path = source_path
      self.value = value
      self.annotations = annotations
      self.units = units

class MetaForgeParser(ABC):
  @abstractmethod
  def human_label(self) -> str:
    """
    Returns a label for the parser suitable to place into a user interface
    """
    raise NotImplementedError

  @abstractmethod
  def version(self) -> str:
    """
    Returns the version of this parser. It is up to the developer to version their own parsers
    """
    raise NotImplementedError

  @abstractmethod
  def uuid(self) -> UUID:
    """
    Returns the uuid of this parser. It is up to the developer to set uuids for their own parsers
    """
    raise NotImplementedError

  @abstractmethod
  def supported_file_extensions(self) -> list:
    """
    This function returns a list of the file extensions that are understood by this parser
    """
    raise NotImplementedError

  @abstractmethod
  def accepts_extension(self, extension: str) -> bool:
    """
    This fuction returns whether or not this parser understands the given file extension

    Parameters
    ----------
    extension
        The file extension to check including the '.' character

    """
    raise NotImplementedError

  @abstractmethod
  def parse_header(self, filepath: Path) -> List[MetaForgeMetadata]:
    """
    This function returns a list of the 'header' information, i.e., the metadata from the file

    Parameters
    ----------
    filepath
        The path to the tiff image to be parsed

    Returns
    -------
    Dictionary
        A dictionary containing the header information with the top level of the dictionary being:
    
    Example Implementation 
    -------
      ```
      ....
      file_dict = {"SOURCE": header}
      return file_dict
      ```
    """
    raise NotImplementedError
from typing import List, Tuple
from pathlib import Path
from uuid import UUID

from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt

from parsers.metaforgeparser import MetaForgeParser
from parsers.ctf_parser import CtfParser
from parsers.ang_parser import AngParser
from parsers.fei_tiff_parser import FeiTiffParser
from parsers.ini_parser import IniParser

class AvailableParsersModel(QAbstractListModel):
  HumanLabel = Qt.DisplayRole
  Parser = Qt.UserRole + 1

  def __init__(self, parent=None):
    super().__init__(parent)
    self._available_parsers: List[MetaForgeParser] = (AngParser(), CtfParser(), IniParser(), FeiTiffParser())

  def data(self, index: QModelIndex, role: int):
    if role == AvailableParsersModel.HumanLabel:
      return self._available_parsers[index.row()].human_label()
    elif role == AvailableParsersModel.Parser:
      return self._available_parsers[index.row()]

  def rowCount(self, parent=None):
    return len(self._available_parsers)
  
  def find_parser_from_uuid(self, uuid: UUID) -> Tuple[int, MetaForgeParser]: 
    if uuid is not None:
      for row in range(self.rowCount()):
        model_index = self.index(row, 0)
        parser = self.data(model_index, AvailableParsersModel.Parser)
        if parser.uuid() == uuid:
            return row, parser

    return None, None

  def find_compatible_parser(self, file_path: Path) -> Tuple[int, MetaForgeParser]: 
    if file_path == None:
          return None, None

    for row in range(self.rowCount()):
      model_index = self.index(row, 0)
      parser = self.data(model_index, AvailableParsersModel.Parser)
      if parser.accepts_extension(file_path.suffix):
          return row, parser
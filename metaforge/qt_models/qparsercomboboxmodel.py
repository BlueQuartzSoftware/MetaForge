from pathlib import Path
from typing import Tuple
from uuid import UUID

from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt

from metaforge.models.parsermodel import ParserModel
from metaforge.parsers.metaforgeparser import MetaForgeParser

class QParserComboBoxModel(QAbstractListModel):
  HumanLabel = Qt.DisplayRole
  Parser = Qt.UserRole + 1
  ParserPath = Qt.UserRole + 2
  Default = Qt.UserRole + 3
  Enabled = Qt.UserRole + 4

  def __init__(self, ez_parser_model: ParserModel, parent=None):
    super().__init__(parent)
    self._ez_parser_model: ParserModel = ez_parser_model

  def data(self, index: QModelIndex, role: int):
    if role == QParserComboBoxModel.HumanLabel:
      return self._ez_parser_model.parser(index.row()).human_label()
    elif role == QParserComboBoxModel.Parser:
      return self._ez_parser_model.parser(index.row())
    elif role == QParserComboBoxModel.ParserPath:
      return self._ez_parser_model.parser_path(index.row())
    elif role == QParserComboBoxModel.Default:
      return self._ez_parser_model.is_default(index.row())
    elif role == QParserComboBoxModel.Enabled:
      return self._ez_parser_model.is_enabled(index.row())
  
  def index_from_parser(self, parser: MetaForgeParser) -> int:
    return self._ez_parser_model.index_from_parser(parser)
  
  def index_from_parser_path(self, parser_path: Path) -> int:
    return self._ez_parser_model.index_from_parser_path(parser_path)
  
  def find_parser_from_uuid(self, uuid: UUID) -> Tuple[MetaForgeParser, str]:
    return self._ez_parser_model.find_parser_from_uuid(uuid)

  def find_parser_from_data_path(self, file_path: Path) -> Tuple[MetaForgeParser, str]: 
    return self._ez_parser_model.find_parser_from_data_path(file_path)

  def rowCount(self, parent=None):
    return self._ez_parser_model.size()
from typing import List, Tuple
from pathlib import Path
from uuid import UUID

import re
import os
import importlib

from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt

from metaforge.utilities.parser_utilities import load_parser_module
from metaforge.parsers.metaforgeparser import MetaForgeParser
from metaforge.ez_models.ezparser import EzParser

class QParsersModel(QAbstractListModel):
  HumanLabel = Qt.DisplayRole
  Parser = Qt.UserRole + 1
  ParserPath = Qt.UserRole + 2

  def __init__(self, parent=None):
    super().__init__(parent)
    self._parsers: List[EzParser] = []
  
  def _insert_parser(self, parser: EzParser, index: int):
    self.beginInsertRows(QModelIndex(), index, index)
    self._parsers.insert(index, parser)
    self.endInsertRows()
  
  def _add_parser(self, parser: EzParser):
    self._insert_parser(parser, len(self._parsers))

  def _add_parsers(self, parsers: List[EzParser]):
    [self._add_parser(parser) for parser in parsers]
  
  def _search_dynamic(self):
    # Look for files ending in _parser.py on the parsers directory.
    plugin_re = re.compile('_parser.py$')
    plugin_files = filter(plugin_re.search,
                          os.listdir(os.path.join(os.path.dirname(__file__),
                                                  'parsers')))
    form_module = lambda fp: '.' + os.path.splitext(fp)[0]
    plugins = map(form_module, plugin_files)
    parsers = []
    for plugin in plugins:
      if not plugin.startswith('.example'):
        parsers.append(importlib.import_module(plugin, package="parsers"))

    # Now check that they contain a MetaForgeParser subclass and add them if so.
    self._add_parsers(parsers)

  def clear_parsers(self):
    self.beginRemoveRows(QModelIndex(), 0, self.rowCount() - 1)
    self._parsers.clear()
    self.endRemoveRows()

  def load_parsers(self, parser_file_paths: List[Path]):
    # This method dynamically loads parsers from the plugins directory.
    for path in parser_file_paths:
      parser: MetaForgeParser = load_parser_module(path)
      new_ez_parser = EzParser(path, parser)
      matching_ez_parser: EzParser = None
      for current_ez_parser in self._parsers:
        if current_ez_parser.parser.uuid() == new_ez_parser.parser.uuid():
          matching_ez_parser = current_ez_parser

      if matching_ez_parser is None:
        # Parser is not loaded, so load it
        self._add_parser(new_ez_parser)
      else:
        # Parser is loaded already so replace it with the new one
        self._replace_parser(matching_ez_parser, new_ez_parser)
  
  def _replace_parser(self, old_parser: EzParser, new_parser: EzParser):
    index = self._parsers.index(old_parser)
    self.beginRemoveRows(QModelIndex(), index, index)
    self._parsers.remove(old_parser)
    self.endRemoveRows()
    self._insert_parser(new_parser, index)

  def data(self, index: QModelIndex, role: int):
    if role == QParsersModel.HumanLabel:
      return self._parsers[index.row()].parser.human_label()
    elif role == QParsersModel.Parser:
      return self._parsers[index.row()].parser
    elif role == QParsersModel.ParserPath:
      return self._parsers[index.row()].parser_path

  def rowCount(self, parent=None):
    return len(self._parsers)
  
  def find_parser_from_uuid(self, uuid: UUID, error_callback=None) -> Tuple[int, MetaForgeParser]:
    if uuid is None:
      if error_callback is not None:
        error_callback(f"Unable to find a parser using UUID - The given UUID is set to None!")
      return None, None

    if self.rowCount() == 0:
      if error_callback is not None:
        error_callback(f"Unable to find a parser using UUID - No parsers are loaded!  Please open the Preferences menu to add parser locations.")
      return None, None

    for row in range(self.rowCount()):
      model_index = self.index(row, 0)
      parser = self.data(model_index, QParsersModel.Parser)
      if parser.uuid() == uuid:
          return row, parser

    if error_callback is not None:
      error_callback(f"Unable to find a parser using UUID - The UUID '{str(uuid)}' does not match any of the currently loaded parsers!")
    return None, None

  def find_compatible_parser(self, file_path: Path, error_callback=None) -> Tuple[int, MetaForgeParser]: 
    if file_path == None:
      if error_callback is not None:
        error_callback(f"Unable to find a compatible parser - The given file path is set to None!")
      return None, None
    
    if self.rowCount() == 0:
      if error_callback is not None:
        error_callback(f"Unable to find a compatible parser - No parsers are loaded!  Please open the Preferences menu to add parser locations.")
      return None, None

    for row in range(self.rowCount()):
      model_index = self.index(row, 0)
      parser = self.data(model_index, QParsersModel.Parser)
      if parser.accepts_extension(file_path.suffix):
        return row, parser
    
    if error_callback is not None:
      error_callback(f"Unable to find a compatible parser - The file path '{file_path}' is not compatible with any of the currently loaded parsers!  Please open the Preferences menu to add additional parser locations.")
    return None, None
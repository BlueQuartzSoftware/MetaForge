from typing import List, Tuple
from pathlib import Path
from uuid import UUID

import re
import os
import importlib
from inspect import isclass

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
    self._available_parsers: List[MetaForgeParser] = []
  
  def _add_plugins(self, plugin_modules):
    # Add the supplied plugins if they are of the correct type.
    for mod in plugin_modules:
      for attribute_name in dir(mod):
        attribute = getattr(mod, attribute_name)
        if isclass(attribute) and issubclass(attribute, MetaForgeParser) \
           and attribute_name != 'MetaForgeParser':
          # This adds an instance of the class to the parsers.
          self._available_parsers.append(attribute())
  
  def _search_dynamic(self):
    # Look for files ending in _parser.py on the parsers directory.
    plugin_re = re.compile('_parser.py$')
    plugin_files = filter(plugin_re.search,
                          os.listdir(os.path.join(os.path.dirname(__file__),
                                                  'parsers')))
    form_module = lambda fp: '.' + os.path.splitext(fp)[0]
    plugins = map(form_module, plugin_files)
    plugin_modules = []
    for plugin in plugins:
      if not plugin.startswith('.example'):
        plugin_modules.append(importlib.import_module(plugin, package="parsers"))

    # Now check that they copntain a MetaForgeParser subclass and add them if so.
    self._add_plugins(plugin_modules)

  def clear_parsers(self):
    self._available_parsers.clear()

  def load_parsers(self, parser_file_paths: List[Path]):
    # This method dynamically loads parsers from the plugins directory.
    plugin_modules = []
    for path in parser_file_paths:
      spec =importlib.util.spec_from_file_location("parsers", path)
      mod = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(mod)
      plugin_modules.append(mod)
    self._add_plugins(plugin_modules)


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
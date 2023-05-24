from PySide2.QtWidgets import QUndoCommand
from PySide2.QtCore import QModelIndex

from typing import List
from pathlib import Path

from metaforge.qt_models.qparsertablemodel import QParserTableModel
from metaforge.models.parsermodelitem import ParserModelItem

class LoadParsersCommand(QUndoCommand):
    def __init__(self, parser_model: QParserTableModel, parser_file_paths: List[Path], parent=None):
        super(LoadParsersCommand, self).__init__(parent)
        self.parser_file_paths = parser_file_paths
        self.indexes_loaded: List[int] = []
        self._parser_model = parser_model

    def redo(self):
        # This method dynamically loads parsers from the plugins directory.
        for parser_file_path in self.parser_file_paths:
            index = self._parser_model._ez_parser_model.index_from_parser_path(parser_file_path)
            if index < 0:
                # Parser is not loaded, so load it
                self.indexes_loaded.append(self._parser_model.rowCount())
                self._parser_model.append(ParserModelItem(parser_file_path))
    
    def undo(self):
        if len(self.indexes_loaded) > 0:
            self._parser_model.removeRows(self.indexes_loaded[0], len(self.indexes_loaded), QModelIndex())

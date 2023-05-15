from PySide2.QtWidgets import QUndoCommand
from PySide2.QtCore import QModelIndex, QPersistentModelIndex

from typing import List
from pathlib import Path

from metaforge.qt_models.qparsertablemodel import QParserTableModel
from metaforge.models.parsermodelitem import ParserModelItem

class RemoveParsersCommand(QUndoCommand):
    def __init__(self, parser_model: QParserTableModel, rows: List[int], parent=None):
        super(RemoveParsersCommand, self).__init__(parent)
        self.rows = rows
        self.parser_paths_removed: List[Path] = []
        self._parser_model = parser_model

    def redo(self):
        persistent_rows = [QPersistentModelIndex(self._parser_model.index(row, 0)) for row in self.rows]
        for persistent_row in persistent_rows:
            parser_path = self._parser_model._ez_parser_model.parser_path(persistent_row.row())
            self.parser_paths_removed.append(parser_path)
            self._parser_model.removeRow(persistent_row.row())
    
    def undo(self):
        for idx in range(len(self.parser_paths_removed)):
            parser_file_path = self.parser_paths_removed[idx]
            index = self.rows[idx]

            self._parser_model.beginInsertRows(QModelIndex(), index, index)
            self._parser_model._ez_parser_model.insert(index, ParserModelItem(parser_file_path))
            self._parser_model.endInsertRows()

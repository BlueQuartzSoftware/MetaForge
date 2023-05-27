from PySide6.QtGui import QUndoCommand
from PySide6.QtCore import QModelIndex, Qt

from metaforge.qt_models.qparsertablemodel import QParserTableModel

class ToggleParserCommand(QUndoCommand):
    def __init__(self, parser_model: QParserTableModel, index: QModelIndex, value: Qt.CheckState, parent=None):
        super(ToggleParserCommand, self).__init__(parent)
        self._parser_model = parser_model
        self._index = index
        self._value = value

    def redo(self):
        self._parser_model.setData(self._index, (Qt.Checked if self._value == Qt.Checked else Qt.Unchecked), Qt.CheckStateRole)
    def undo(self):
        self._parser_model.setData(self._index, (Qt.Unchecked if self._value == Qt.Checked else Qt.Checked), Qt.CheckStateRole)

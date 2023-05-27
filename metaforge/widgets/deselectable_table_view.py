
from PySide6.QtWidgets import QTableView
from PySide6.QtCore import QObject, Signal   


class DeselectableTableView(QTableView):
    
    selectionCleared = Signal()

    def mousePressEvent(self, event):
        self.clearSelection()
        QTableView.mousePressEvent(self, event)
        self.selectionCleared.emit()

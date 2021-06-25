
from PySide2.QtWidgets import QTableView
from PySide2.QtCore import QObject, Signal   


class DeselectableTableView(QTableView):
    
    selectionCleared = Signal()

    def mousePressEvent(self, event):
        self.clearSelection()
        QTableView.mousePressEvent(self, event)
        self.selectionCleared.emit()

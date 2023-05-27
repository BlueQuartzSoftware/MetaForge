
from PySide6.QtWidgets import QTreeView
from PySide6.QtCore import QObject, Signal   


class DeselectableTreeView(QTreeView):
    
    selectionCleared = Signal()

    def mousePressEvent(self, event):
        self.clearSelection()
        QTreeView.mousePressEvent(self, event)
        self.selectionCleared.emit()

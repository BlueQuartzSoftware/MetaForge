
from PySide6.QtWidgets import QListView
from PySide6.QtCore import QObject, Signal   


class DeselectableListView(QListView):
    
    selectionCleared = Signal()

    def mousePressEvent(self, event):
        self.clearSelection()
        QListView.mousePressEvent(self, event)
        self.selectionCleared.emit()

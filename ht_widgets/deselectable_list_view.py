
from PySide2.QtWidgets import QListView
from PySide2.QtCore import QObject, Signal   


class DeselectableListView(QListView):
    
    selectionCleared = Signal()

    def mousePressEvent(self, event):
        self.clearSelection()
        QListView.mousePressEvent(self, event)
        self.selectionCleared.emit()

# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets
from PySide2.QtWidgets import QStyledItemDelegate
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class TrashDelegate(QItemDelegate):
    pressed = Signal(str)
    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        if index.column() != 7:
            QStyledItemDelegate.createEditor(self,parent,option,index)
        else:

            sourceModelIndex = (index.model().mapToSource(index)).row()
            #The index goes from the Proxy Model to the Table Model to look into the masterlist.
            self.pressed.emit(index.model().sourceModel().metadataList[sourceModelIndex]["Source"])


    def paint(self, painter, option, index):
        if index.column() == 7:
            icon = QApplication.style().standardIcon(QStyle.SP_TrashIcon)
            painter.save()
            line_1x = icon.pixmap(16,16)
            painter.drawPixmap(option.rect.x()+option.rect.width()/2 - 8 ,
            option.rect.y()+option.rect.height()/2 - 8,
            16,
            16,
            line_1x)
            painter.restore()
        else:
            QStyledItemDelegate.paint(self, painter, option, index)



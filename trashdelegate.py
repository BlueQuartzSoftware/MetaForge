# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets
from PySide2.QtWidgets import QStyledItemDelegate
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from resources_rc import *

import usetablemodel

class TrashDelegate(QItemDelegate):
    pressed = Signal(str)
    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        sourceModelIndex = (index.model().mapToSource(index))
        realSourceModelIndex = sourceModelIndex.model().mapToSource(sourceModelIndex).row()
        #The index goes from the Proxy Model to the Table Model to look into the masterlist.
        self.pressed.emit(index.model().sourceModel().sourceModel().metadataList[realSourceModelIndex]["Source"])


    def paint(self, painter, option, index):
        icon = QIcon(QPixmap(':/resources/close-pushed@2x.png'))
        painter.save()
        line_1x = icon.pixmap(16,16)
        painter.drawPixmap(option.rect.x()+option.rect.width()/2 - 8 ,
        option.rect.y()+option.rect.height()/2 - 8,
        16,
        16,
        line_1x)
        painter.restore()



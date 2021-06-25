# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets
from PySide2.QtWidgets import QStyledItemDelegate
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from resources_rc import *


class CheckBoxDelegate(QItemDelegate):
    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        option.rect = option.rect.adjusted((option.rect.width()/2) - 8,0,0,0)
        QItemDelegate.paint(self, painter, option, index)

#    def drawCheck(self, painter, option, rect, index):
#        rect = rect.adjusted((rect.width()/2)-8,0,0,0)
#        option.rect = option.rect.adjusted((option.rect.width()/2) - 8,0,0,0)
#        QItemDelegate.drawCheck(self, painter, option, rect, index)

    def editorEvent(self, event, model, option, index):
        flags = model.flags(index)
#        if ! (flags & Qt.ItemIsUserCheckable) ||  ! (flags & Qt.ItemIsEnabled):
#            return False
        value = index.data(Qt.CheckStateRole)
        if (event.type() == QEvent.MouseButtonRelease):
             checkRect = option.rect.adjusted((option.rect.width()/2)+ 20,(option.rect.height()/2),0,0)
             if not checkRect.contains(event.pos()):
                print("ouch")
             else:
                print("not ouch")
                return False
        else:
            return False
        if value == Qt.Checked:
            value = Qt.Unchecked
        elif value == Qt.Unchecked:
            value = Qt.Checked

        return model.setData(index,value, Qt.CheckStateRole)



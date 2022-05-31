# This Python file uses the following encoding: utf-8
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import PySide2.QtCore

qt_version = PySide2.QtCore.__version_info__

if qt_version[1] == 12:
    from generated_5_12.resources_rc import *
elif qt_version[1] == 15:
    from generated_5_15.resources_rc import *


class CheckBoxDelegate(QItemDelegate):
    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        option.rect = option.rect.adjusted((option.rect.width()/2) - 8,0,0,0)
        QItemDelegate.paint(self, painter, option, index)

    def editorEvent(self, event, model, option, index):
        flags = index.flags()
        if int(flags & Qt.ItemIsEnabled) == 0:
            return False
        value = index.data(Qt.CheckStateRole)
        if (event.type() == QEvent.MouseButtonRelease):
             checkRect = option.rect.adjusted((option.rect.width()/2)+ 20,(option.rect.height()/2),0,0)
             if checkRect.contains(event.pos()):
                return False
        else:
            return False
        if value == Qt.Checked:
            value = Qt.Unchecked
        elif value == Qt.Unchecked:
            value = Qt.Checked

        return model.setData(index,value, Qt.CheckStateRole)



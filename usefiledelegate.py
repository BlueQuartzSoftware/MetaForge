# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets
from PySide2.QtWidgets import QStyledItemDelegate
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from resources_rc import *


class UseFileDelegate(QItemDelegate):
    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):        
            icon = QIcon(QPixmap(':/resources/close-pushed@2x.png'))
            painter.save()            
            line_1x = icon.pixmap(12,12)
            painter.drawText( option.rect.adjusted(5,option.rect.height()/2 - 8 , 0, 0), Qt.AlignLeft, index.data())
            painter.drawPixmap(option.rect.x()+option.rect.width() - 25,
            option.rect.y()+option.rect.height()/2 - 4,
            12,
            12,
            line_1x)
            painter.restore()


    def sizeHint(self, option, index):
        return QSize( option.rect.width(), 24)


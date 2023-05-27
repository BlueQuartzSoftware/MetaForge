# This Python file uses the following encoding: utf-8
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import PySide6.QtCore

qt_version = PySide6.QtCore.__version_info__

from metaforge.widgets.generated_6_5.resources_rc import *
from metaforge.common.metaforgestyledatahelper import MetaForgeStyleDataHelper

class TrashDelegate(QStyledItemDelegate):
    pressed = Signal(QModelIndex)

    def __init__(self, parent=None, stylehelper: MetaForgeStyleDataHelper=None):
        QStyledItemDelegate.__init__(self, parent)
        self.style_helper = stylehelper

    def createEditor(self, parent, option, index):
        source_index = index.model().mapToSource(index)

        if source_index.isValid():
            self.pressed.emit(source_index)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        if self.style_helper == None:
            icon = QIcon(QPixmap(':/resources/Images/close-pushed@2x.png'))
        elif self.style_helper.css_file_path == "resources/StyleSheets/light.css":
            icon = QIcon(QPixmap(':/resources/Images/close-pushed@2x.png'))
        elif self.style_helper.css_file_path == "resources/StyleSheets/dark.css":
            icon = QIcon(QPixmap(':/resources/Images/dark/close-pushed@2x.png'))
        else:
            icon = QIcon(QPixmap(':/resources/Images/close-pushed@2x.png'))

        painter.save()
        line_1x = icon.pixmap(16,16)
        painter.drawPixmap(option.rect.x()+option.rect.width()/2 - 8 ,
        option.rect.y()+option.rect.height()/2 - 8,
        16,
        16,
        line_1x)
        painter.restore()



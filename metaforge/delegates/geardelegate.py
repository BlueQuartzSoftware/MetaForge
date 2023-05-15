# This Python file uses the following encoding: utf-8
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import PySide2.QtCore

qt_version = PySide2.QtCore.__version_info__

if qt_version[1] == 12:
    from metaforge.widgets.generated_5_12.resources_rc import *
elif qt_version[1] == 15:
    from metaforge.widgets.generated_5_15.resources_rc import *
from metaforge.common.metaforgestyledatahelper import MetaForgeStyleDataHelper

class GearDelegate(QStyledItemDelegate):
    pressed = Signal(QModelIndex)

    def __init__(self, parent=None, stylehelper: MetaForgeStyleDataHelper=None):
        QStyledItemDelegate.__init__(self, parent)
        self.style_helper = stylehelper

    def createEditor(self, parent, option, index):
        if index.isValid():
            self.pressed.emit(index)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        # if self.style_helper == None:
        #     icon = QIcon(QPixmap(':/resources/Images/close-pushed@2x.png'))
        # elif self.style_helper.css_file_path == "resources/StyleSheets/light.css":
        #     icon = QIcon(QPixmap(':/resources/Images/close-pushed@2x.png'))
        # elif self.style_helper.css_file_path == "resources/StyleSheets/dark.css":
        #     icon = QIcon(QPixmap(':/resources/Images/dark/close-pushed@2x.png'))
        # else:
        #     icon = QIcon(QPixmap(':/resources/Images/close-pushed@2x.png'))
        icon = QIcon(QPixmap(':/resources/Images/gear@2x.png'))

        painter.save()
        line_1x = icon.pixmap(18,18)
        painter.drawPixmap(option.rect.x()+option.rect.width()/2 - 8 ,
        option.rect.y()+option.rect.height()/2 - 8,
        18,
        18,
        line_1x)
        painter.restore()



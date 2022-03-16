# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets
from PySide2.QtWidgets import QStyledItemDelegate
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import PySide2.QtCore

qt_version = PySide2.QtCore.__version_info__

if qt_version[1] == 12:
    from generated_5_12.ui_mainwindow import Ui_MainWindow
    from generated_5_12.resources_rc import *
elif qt_version[1] == 15:
    from generated_5_15.ui_mainwindow import Ui_MainWindow
    from generated_5_15.resources_rc import *
from metaforgestyledatahelper import MetaForgeStyleDataHelper


class UseFileDelegate(QItemDelegate):
    def __init__(self, parent=None, stylehelper: MetaForgeStyleDataHelper=None):
        QItemDelegate.__init__(self, parent)
        self.style_helper = stylehelper

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
        line_1x = icon.pixmap(12,12)
       # painter.drawText( option.rect.adjusted(5,option.rect.height()/2 - 8 , 0, 0), Qt.AlignLeft, index.data())
        painter.drawPixmap(option.rect.x()+option.rect.width() - 25,
        option.rect.y()+option.rect.height()/2 - 4,
        12,
        12,
        line_1x)
        painter.restore()


    # def sizeHint(self, option, index):
    #     return QSize( option.rect.width(), 24)


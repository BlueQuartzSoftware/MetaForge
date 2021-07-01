# This Python file uses the following encoding: utf-8
#!/usr/bin/env python3
import sys
import os
import platform

# This is necessary for MacOS 11.0 (10.16) and up to launch the application properly
if platform.system() == 'Darwin':
    v, _, _ = platform.mac_ver()
    v = float('.'.join(v.split('.')[:2]))
    if v >= 10.16:
        os.environ["QT_MAC_WANTS_LAYER"] = "1"

from PySide2.QtWidgets import QApplication, QWidget, QMainWindow
from PySide2.QtCore import QFile, QIODevice, QObject, QFileSystemWatcher, Qt, Signal, Slot
from PySide2.QtGui import QIcon, QFontDatabase
from ui_mainwindow import Ui_MainWindow
from mainwindowimpl import MainWindow
from resources_rc import *


class MetaForgeHelper(QObject):

    def __init__(self, application: QApplication):
        self.app = application
        self.watcher = QFileSystemWatcher()
        self.css_file_path = "resources/StyleSheets/dark.css"
        self.watcher.addPath(self.css_file_path)
        self.watcher.fileChanged.connect(self.fileChanged)

    def initFonts(self):
        fontList = ["resources/fonts/FiraSans-Regular.ttf", 
                    "resources/fonts/Lato-Regular.ttf",
                    "resources/fonts/Lato-Black.ttf", 
                    "resources/fonts/Lato-BlackItalic.ttf",
                    "resources/fonts/Lato-Bold.ttf", 
                    "resources/fonts/Lato-BoldItalic.ttf", 
                    "resources/fonts/Lato-Hairline.ttf", 
                    "resources/fonts/Lato-HairlineItalic.ttf",
                    "resources/fonts/Lato-Italic.ttf", 
                    "resources/fonts/Lato-Light.ttf", 
                    "resources/fonts/Lato-LightItalic.ttf"]
        for f in fontList:
            fontID = QFontDatabase.addApplicationFont(f)

    def initStyleSheet(self):
        css_file = open(self.css_file_path)
        cssContent = css_file.read()
        css_file.close()
        app.setStyleSheet(cssContent)

    @Slot(None)
    def fileChanged(self):
        print('css file changed.....')
        css_file = open(self.css_file_path)
        cssContent = css_file.read()
        css_file.close()
        self.app.setStyleSheet(cssContent)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("MetaForge")
    app.setApplicationDisplayName("MetaForge")
    app.setOrganizationName("BlueQuartz Software")
    app.setWindowIcon(QIcon(':/resources/Images/applicationIcon.png'))
    app.setApplicationVersion("1.0.0 RC-6")

    # helper = MetaForgeHelper(app)
    # helper.initFonts()
    # helper.initStyleSheet()

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


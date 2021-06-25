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
from PySide2.QtCore import QFile, QIODevice, QObject
from PySide2.QtGui import QIcon
from ui_mainwindow import Ui_MainWindow
from mainwindowimpl import MainWindow
from resources_rc import *



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("MetaForge")
    app.setOrganizationName("BlueQuartz Software")
    app.setWindowIcon(QIcon(':/resources/applicationIcon.png'))
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


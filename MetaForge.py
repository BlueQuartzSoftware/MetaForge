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
from PySide2.QtCore import QFile, QIODevice, QObject, Qt
from PySide2.QtGui import QIcon
import PySide2.QtCore


qt_version = PySide2.QtCore.__version_info__

if qt_version[1] == 12:
    from generated_5_12.ui_mainwindow import Ui_MainWindow
    from generated_5_12.resources_rc import *
elif qt_version[1] == 15:
    from generated_5_15.ui_mainwindow import Ui_MainWindow
    from generated_5_15.resources_rc import *

from mainwindowimpl import MainWindow
from metaforgestyledatahelper import MetaForgeStyleDataHelper

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("MetaForge")
    app.setApplicationDisplayName("MetaForge")
    app.setOrganizationName("BlueQuartz Software")
    app.setApplicationVersion("1.0.0 RC-10")

    if platform.system() == 'Darwin':
        # Set the Application Icon
        app.setWindowIcon(QIcon(':/resources/Images/MetaForge.icns'))
    else:
        # Set the Application Icon
        app.setWindowIcon(QIcon(':/resources/Images/MetaForge.png'))        


    window = MainWindow(app)
    window.show()

    sys.exit(app.exec_())


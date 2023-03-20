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

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon

from metaforge.mainwindowimpl import MainWindow

def main():
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

    app.exec_()

if __name__ == "__main__":
    sys.exit(main())

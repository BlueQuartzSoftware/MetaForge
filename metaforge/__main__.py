# This Python file uses the following encoding: utf-8
#!/usr/bin/env python3
import sys
import os
import platform
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from metaforge.widgets.mainwindowimpl import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("MetaForge")
    app.setApplicationDisplayName("MetaForge")
    app.setOrganizationName("BlueQuartz Software")

    parent_path = Path(__file__).resolve().parent
    version_filepath = parent_path / 'VERSION'
    with open(str(version_filepath)) as version_file:
        version = version_file.read().strip()
    app.setApplicationVersion(version)

    if platform.system() == 'Darwin':
        # Set the Application Icon
        app.setWindowIcon(QIcon(':/resources/Images/MetaForge.icns'))
    else:
        # Set the Application Icon
        app.setWindowIcon(QIcon(':/resources/Images/MetaForge.png'))        


    window = MainWindow(app)
    window.show()

    app.exec()

if __name__ == "__main__":
    sys.exit(main())

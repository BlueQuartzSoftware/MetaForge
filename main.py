# This Python file uses the following encoding: utf-8
#!/usr/bin/env python3
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget, QMainWindow
from PySide2.QtCore import QFile, QIODevice, QObject
from PySide2.QtGui import QIcon
from ui_mainwindow import Ui_MainWindow
from mainwindowimpl import MainWindow




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("MetaForge")
    app.setWindowIcon(QIcon('applicationIcon.png'));
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


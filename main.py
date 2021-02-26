# This Python file uses the following encoding: utf-8
#!/usr/bin/env python3
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget, QMainWindow
from PySide2.QtCore import QFile, QIODevice
from ui_mainwindow import Ui_MainWindow
from mainwindowimpl import MainWindow




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


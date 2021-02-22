# This Python file uses the following encoding: utf-8

from PySide2.QtWidgets import QApplication, QWidget, QMainWindow
from PySide2.QtCore import QFile, QIODevice
from PySide2.QtUiTools import QUiLoader

class MainWindowImpl(QWidget):
    def __init__(self, parent=None):
        super(MainWindowImpl, self).__init__(parent)

        ui_file_name = "mainwindow.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        window = loader.load(ui_file)
        ui_file.close()
        if not window:
            print(loader.errorString())
            sys.exit(-1)

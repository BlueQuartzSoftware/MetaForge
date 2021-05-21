from PySide2.QtWidgets import QDialog, QMessageBox, QApplication, QStyle
from PySide2.QtCore import Signal, QStringListModel
from newfolderdialog import Ui_NewFolderDialog

class NewFolderDialogImpl(QDialog):
    nameSubmitted = Signal(str)
    def __init__(self, parent=None):
        super(NewFolderDialogImpl, self).__init__(parent)
        self.promptui = Ui_NewFolderDialog()
        self.promptui.setupUi(self)
        self.finished.connect(self.sendName)

    def sendName(self):
        self.nameSubmitted.emit(self.promptui.folderNameLineEdit.text())

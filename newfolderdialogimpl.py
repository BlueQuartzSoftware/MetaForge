from PySide2.QtWidgets import QDialog, QMessageBox, QApplication, QStyle
from PySide2.QtCore import Signal, QStringListModel
import PySide2.QtCore

qt_version = PySide2.QtCore.__version_info__
if qt_version[1] == 12:
    from generated_5_12.ui_newfolderdialog import Ui_NewFolderDialog
elif qt_version[1] == 15:
    from generated_5_15.ui_newfolderdialog import Ui_NewFolderDialog



class NewFolderDialogImpl(QDialog):
    nameSubmitted = Signal(str)
    def __init__(self, parent=None):
        super(NewFolderDialogImpl, self).__init__(parent)
        self.promptui = Ui_NewFolderDialog()
        self.promptui.setupUi(self)
        self.finished.connect(self.sendName)

    def sendName(self):
        self.nameSubmitted.emit(self.promptui.folderNameLineEdit.text())

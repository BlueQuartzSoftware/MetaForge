from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Signal

from metaforge.widgets.generated_6_5.ui_newfolderdialog import Ui_NewFolderDialog

class NewFolderDialogImpl(QDialog):
    nameSubmitted = Signal(str)
    def __init__(self, parent=None):
        super(NewFolderDialogImpl, self).__init__(parent)
        self.promptui = Ui_NewFolderDialog()
        self.promptui.setupUi(self)
        self.accepted.connect(self.sendName)

    def sendName(self):
        self.nameSubmitted.emit(self.promptui.folderNameLineEdit.text())

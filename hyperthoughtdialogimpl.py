from PySide2.QtWidgets import QDialog
from PySide2.QtCore import Signal, QStringListModel
from ht_requests.ht_requests import ht_utilities
from ht_requests.ht_requests import htauthcontroller
from ht_requests.ht_requests import ht_requests
from hyperthoughtdialog import Ui_HyperthoughtDialog

class HyperthoughtDialogImpl(QDialog):
    apiSubmitted = Signal(str)
    def __init__(self, parent=None):
        super(HyperthoughtDialogImpl, self).__init__(parent)
        self.promptui = Ui_HyperthoughtDialog()
        self.accessKey = ""
        self.promptui.setupUi(self)
        self.promptui.apiKeyButton.clicked.connect(self.acceptApiKey)
        self.stringlistmodel = QStringListModel()
        self.uuidlist = []

    def acceptApiKey(self):
        self.accessKey = self.promptui.apiKeyLineEdit.text()
        self.apiSubmitted.emit(self.accessKey)
        authcontrol = htauthcontroller.HTAuthorizationController(self.accessKey)
        projectlist = ht_requests.list_projects(authcontrol)
        stringlist = []
        for i in range(len(projectlist)):
            stringlist.append(projectlist[i]["content"]["title"])
            self.uuidlist.append(projectlist[i]["content"]["pk"])
        self.stringlistmodel.setStringList(stringlist)
        self.promptui.listView.setModel(self.stringlistmodel)

from PySide2.QtWidgets import QDialog, QMessageBox, QApplication, QStyle
from PySide2.QtCore import Signal, QStringListModel
from ht_requests.ht_requests import ht_utilities
from ht_requests.ht_requests import htauthcontroller
from ht_requests.ht_requests import ht_requests
from hyperthoughtdialog import Ui_HyperthoughtDialog
from newfolderdialogimpl import NewFolderDialogImpl
from stringlistmodel import StringListModel

class HyperthoughtDialogImpl(QDialog):
    apiSubmitted = Signal(str)
    def __init__(self, parent=None):
        super(HyperthoughtDialogImpl, self).__init__(parent)
        self.promptui = Ui_HyperthoughtDialog()
        self.accessKey = ""
        self.authcontrol = None
        self.promptui.setupUi(self)
        self.promptui.apiKeyButton.clicked.connect(self.acceptApiKey)
        self.stringlistmodel = StringListModel(self)
        self.promptui.listView.clicked.connect(self.changeLocationText)
        self.promptui.listView.doubleClicked.connect(self.ascendingDirectories)
        self.path = ","
        self.parentName = "/"
        self.promptui.directoryLabel.setText(self.parentName)
        icon = QApplication.style().standardIcon(QStyle.SP_FileDialogNewFolder)
        self.promptui.newFolderButton.setIcon(icon)
        self.promptui.parentDirectoryButton.clicked.connect(self.parentDirectory)
        self.newfolderDialog = NewFolderDialogImpl()
        self.promptui.newFolderButton.clicked.connect(self.newfolderDialog.exec)
        self.newfolderDialog.nameSubmitted.connect(self.createNewFolder)




    def acceptApiKey(self):
        self.accessKey = self.promptui.apiKeyLineEdit.text()
        self.apiSubmitted.emit(self.accessKey)
        try:
            self.authcontrol = htauthcontroller.HTAuthorizationController(self.accessKey)
            folderlist = ht_requests._list_location_contents(self.authcontrol, ht_id_path = self.path)
            self.stringlistmodel.getLists(folderlist)
            self.promptui.listView.setModel(self.stringlistmodel)
        except Exception as e:
             QMessageBox.warning(None, QApplication.applicationDisplayName(), "Bad stuff happens. " + str(e))

    def ascendingDirectories(self, myIndex):
       try:
           self.parentName += myIndex.data()+"/"
           self.promptui.directoryLabel.setText(self.parentName)
           self.path += self.stringlistmodel.uuidList[self.stringlistmodel.directoryList.index(myIndex.data())]+","
           folderlist = ht_requests._list_location_contents(self.authcontrol, ht_id_path = self.path)
           self.stringlistmodel.getLists(folderlist)
       except Exception as e:
           QMessageBox.warning(None, QApplication.applicationDisplayName(), "Bad stuff happens. " + str(e))

    def changeLocationText(self,myIndex):
        self.promptui.locationLineEdit.setText(myIndex.data())

    def createNewFolder(self, name):
        try:
            ht_requests.create_folder(self.authcontrol, folder_name = name, ht_id_path= self.path)
            folderlist = ht_requests._list_location_contents(self.authcontrol, ht_id_path = self.path)
        except Exception as e:
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Bad stuff happens. " + str(e))


    def parentDirectory(self):
        try:
            self.parentName = self.parentName.split("/")
            self.parentName = "/".join(self.parentName[:-2]) + "/"
            self.promptui.directoryLabel.setText(self.parentName)
            self.path = self.path.split(",")
            self.path = ",".join(self.path[:-2]) + ","
            folderlist = ht_requests._list_location_contents(self.authcontrol, ht_id_path = self.path)
            self.stringlistmodel.getLists(folderlist)
        except Exception as e:
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Bad stuff happens. " + str(e))

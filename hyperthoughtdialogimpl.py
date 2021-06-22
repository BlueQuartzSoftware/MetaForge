import os

from PySide2.QtWidgets import QDialog, QMessageBox, QApplication, QStyle, QListView
from PySide2.QtCore import Signal, QStringListModel, Qt, Slot
from ht_requests.ht_requests import ht_utilities
from ht_requests.ht_requests import htauthcontroller
from ht_requests.ht_requests import ht_requests
from ui_hyperthoughtdialog import Ui_HyperthoughtDialog
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
        self.promptui.parentDirectoryButton.clicked.connect(self.parentDirectory)
        self.newfolderDialog = NewFolderDialogImpl()
        self.promptui.newFolderButton.clicked.connect(self.newfolderDialog.exec)
        self.newfolderDialog.nameSubmitted.connect(self.createNewFolder)

        self.promptui.listView.selectionCleared.connect(self.clearLocationLineEdit)

    @Slot()    
    def clearLocationLineEdit(self):
        self.promptui.locationLineEdit.setText("")

    def acceptApiKey(self):
        self.accessKey = self.promptui.apiKeyLineEdit.text()
        if self.accessKey == "":
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Please set the API Access key.")
            return

        self.apiSubmitted.emit(self.accessKey)
        try:
            self.authcontrol = htauthcontroller.HTAuthorizationController(self.accessKey)
            self.promptui.ht_server_url.setText(self.authcontrol.base_url)
            self.promptui.ht_username.setText(self.authcontrol.get_username())
            self.promptui.token_expiration.setText(self.authcontrol.expires_at)
            folderlist = ht_requests._list_location_contents(self.authcontrol, ht_id_path = self.path)
            self.stringlistmodel.getLists(folderlist)
            self.promptui.listView.setModel(self.stringlistmodel)
        except Exception as e:
             QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error during the authentication process.\n" + str(e))

    def ascendingDirectories(self, myIndex):
       try:
           self.parentName += myIndex.data()+"/"
           self.promptui.directoryLabel.setText(self.parentName)
           self.path += self.stringlistmodel.uuidList[self.stringlistmodel.directoryList.index(myIndex.data())]+","
           folderlist = ht_requests._list_location_contents(self.authcontrol, ht_id_path = self.path)
           self.stringlistmodel.getLists(folderlist)
           self.promptui.locationLineEdit.setText("")
       except Exception as e:
           QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error during directory traversal.\n" + str(e))

    def changeLocationText(self,myIndex):
        if myIndex.isValid():
            self.promptui.locationLineEdit.setText(myIndex.data())

    def createNewFolder(self, name):
        try:
            ht_requests.create_folder(self.authcontrol, folder_name = name, ht_id_path= self.path)
            folderlist = ht_requests._list_location_contents(self.authcontrol, ht_id_path = self.path)
            self.stringlistmodel.getLists(folderlist)
        except Exception as e:
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error creating remote directory.\n" + str(e))


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
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error getting the parent directory.\n" + str(e))

    def getUploadDirectory(self):
        return self.promptui.directoryLabel.text() + self.promptui.locationLineEdit.text()
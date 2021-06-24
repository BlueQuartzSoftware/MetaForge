import os

from PySide2.QtWidgets import QDialog, QMessageBox, QApplication, QStyle, QListView
from PySide2.QtCore import Signal, QStringListModel, Qt, Slot
from PySide2.QtGui import QClipboard, QGuiApplication

from ht_requests.ht_requests import ht_utilities
from ht_requests.ht_requests import htauthcontroller
from ht_requests.ht_requests import ht_requests
from ui_hyperthoughtdialog import Ui_HyperthoughtDialog
from newfolderdialogimpl import NewFolderDialogImpl
from stringlistmodel import StringListModel

from typing import List


class HyperthoughtDialogImpl(QDialog):
    apiSubmitted = Signal(str)
    def __init__(self, parent=None):
        super(HyperthoughtDialogImpl, self).__init__(parent)
        self.ui = Ui_HyperthoughtDialog()
        self.accessKey = ""
        self.authcontrol = None
        self.ui.setupUi(self)
        self.ui.apiKeyButton.clicked.connect(self.acceptApiKey)
        self.stringlistmodel = StringListModel(self)
        self.ui.folderListView.clicked.connect(self.changeLocationText)
        self.ui.folderListView.doubleClicked.connect(self.ascendingDirectories)
        self.path = ","
        self.parentName = "/"
        self.project_dict = {}
        self.current_project = {}
        self.bread_crumb_path = list()

        self.ui.directoryLabel.setText(self.parentName)
        self.ui.parentDirectoryButton.clicked.connect(self.parentDirectory)
        self.newfolderDialog = NewFolderDialogImpl()
        self.ui.newFolderButton.clicked.connect(self.newfolderDialog.exec)
        self.newfolderDialog.nameSubmitted.connect(self.createNewFolder)

        self.ui.folderListView.selectionCleared.connect(self.clearLocationLineEdit)
        self.ui.pasteFromClipboardBtn.clicked.connect(self.pasteAPIKey)
        self.ui.projectListView.currentRowChanged.connect(self.projectRowChanged)

    @Slot()    
    def clearLocationLineEdit(self):
        self.ui.selectedProjectFolder.setText("")

    @Slot()
    def pasteAPIKey(self):
        clipboard = QGuiApplication.clipboard()
        mimeData = clipboard.mimeData()
        if mimeData.hasText():
            self.ui.apiKeyLineEdit.setText(mimeData.text())
        
    def acceptApiKey(self):
        self.accessKey = self.ui.apiKeyLineEdit.text()
        if self.accessKey == "":
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Please set the API Access key.")
            return

        self.apiSubmitted.emit(self.accessKey)
        try:
            self.authcontrol = htauthcontroller.HTAuthorizationController(self.accessKey)
            self.ui.ht_server_url.setText(self.authcontrol.base_url)
            self.ui.ht_username.setText(self.authcontrol.get_username())
            self.ui.token_expiration.setText(self.authcontrol.expires_at)
            self.project_dict = ht_requests.list_projects(self.authcontrol)
            self.ui.projectListView.clear()
            for project in self.project_dict:
                self.ui.projectListView.addItem(project["content"]["title"])

        except Exception as e:
             QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error during the authentication process.\n" + str(e))


    @Slot()
    def projectRowChanged(self, currentRow: int):
        project_title = self.ui.projectListView.currentItem().text()

        # Find the projects uuid
        for project in self.project_dict:
            if project_title == project["content"]["title"]:
                self.current_project = project
                break
        # If the UUID is valid then get the item list from that location
        puid = self.current_project["content"]["pk"]
        if puid != "":
            folderlist = ht_requests.get_item_dict_from_ht_path(self.authcontrol, 
                ht_path = '/', 
                ht_space = 'project',
                ht_space_id=puid)
            self.stringlistmodel.getLists(folderlist)
            self.ui.selectedProjectFolder.setText("")
            self.ui.folderListView.setModel(self.stringlistmodel)
            self.bread_crumb_path = list()
            self.ui.directoryLabel.setText("")

    def ascendingDirectories(self, myIndex):
      # try:
            selected_row = myIndex.row()
            selected_type = self.stringlistmodel.typeList[selected_row]
            if selected_type is not None and selected_type != "Folder":
                return

            self.parentName += myIndex.data()+"/"
            folder_name = self.stringlistmodel.data(myIndex, Qt.DisplayRole)
            self.bread_crumb_path.append(folder_name)

            path = "/"
            for p in self.bread_crumb_path:
                path = path + p + "/"

            self.ui.directoryLabel.setText(path)
            self.path += self.stringlistmodel.uuidList[self.stringlistmodel.directoryList.index(myIndex.data())]+","

            folderlist = ht_requests.get_item_dict_from_ht_path(self.authcontrol, 
                ht_path = self.parentName, 
                ht_space = 'project',
                ht_space_id=self.current_project["content"]["pk"])

            self.stringlistmodel.getLists(folderlist)
            self.stringlistmodel
            self.ui.selectedProjectFolder.setText("")
            self.ui.folderListView.selectionModel().clearSelection()

      # except Exception as e:
       #    QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error during directory traversal.\n" + str(e))

    def changeLocationText(self, myIndex):
        selected_row = myIndex.row()
        selected_type = self.stringlistmodel.typeList[selected_row]
        
        if myIndex.isValid() and selected_type == "Folder":
            self.ui.selectedProjectFolder.setText(myIndex.data())
        

    def createNewFolder(self, name):
        try:
            ht_requests.create_folder(self.authcontrol, folder_name = name, ht_id_path= self.path)
            folderlist = ht_requests._list_location_contents(self.authcontrol, ht_id_path = self.path)
            self.stringlistmodel.getLists(folderlist)
        except Exception as e:
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error creating remote directory.\n" + str(e))


    def parentDirectory(self):
        try:
            self.bread_crumb_path.pop()
            path = "/".join(self.bread_crumb_path)
            
            if path == "":
                path = '/'

            self.ui.directoryLabel.setText(path)

            self.parentName = path
            self.path = self.path.split(",")
            self.path = ",".join(self.path[:-2]) + ","
            folderlist = ht_requests.get_item_dict_from_ht_path(self.authcontrol, 
                ht_path = self.parentName, 
                ht_space = 'project',
                ht_space_id=self.current_project["content"]["pk"])

            self.stringlistmodel.getLists(folderlist)
            self.ui.selectedProjectFolder.setText("")
            self.ui.folderListView.selectionModel().clearSelection()

        except Exception as e:
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error getting the parent directory.\n" + str(e))

    def getUploadDirectory(self):
        return self.ui.directoryLabel.text() + self.ui.selectedProjectFolder.text()
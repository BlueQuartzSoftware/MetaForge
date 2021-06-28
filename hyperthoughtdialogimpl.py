import os

from PySide2.QtWidgets import QDialog, QMessageBox, QApplication, QStyle, QListView
from PySide2.QtCore import Signal, QStringListModel, Qt, Slot
from PySide2.QtGui import QClipboard, QGuiApplication

from ht_requests.ht_requests import ht_utilities
from ht_requests.ht_requests import htauthcontroller
from ht_requests.ht_requests import ht_requests
from ui_hyperthoughtdialog import Ui_HyperthoughtDialog
from newfolderdialogimpl import NewFolderDialogImpl
from htremotefilelistmodel import HTRemoteFileListModel

from typing import List


class HyperthoughtDialogImpl(QDialog):

    apiSubmitted = Signal(str)
    
    def __init__(self, parent=None):
        super(HyperthoughtDialogImpl, self).__init__(parent)
        self.ui = Ui_HyperthoughtDialog()
        self.ui.setupUi(self)

        # initialize variables
        self.accessKey = ""
        self.authcontrol = None
        self.project_dict = {}
        self.current_project = {}
        self.bread_crumb_path = list()
        self.remote_file_list_model = HTRemoteFileListModel(self)
        self.newfolderDialog = NewFolderDialogImpl()
        self.init_col_width = False

        #Setup Signals/Slots connections
        self.ui.apiKeyButton.clicked.connect(self.acceptApiKey)
        self.ui.folderListView.clicked.connect(self.changeLocationText)
        self.ui.folderListView.doubleClicked.connect(self.ascendingDirectories)
        self.ui.parentDirectoryButton.clicked.connect(self.parentDirectory)
        self.ui.newFolderButton.clicked.connect(self.newfolderDialog.exec)
        self.newfolderDialog.nameSubmitted.connect(self.createNewFolder)
        self.ui.folderListView.selectionCleared.connect(self.clearLocationLineEdit)
        self.ui.pasteFromClipboardBtn.clicked.connect(self.pasteAPIKey)
        self.ui.projectListView.currentRowChanged.connect(self.projectRowChanged)
        self.setWindowTitle("Authenticate To HyperThought")

    @Slot()    
    def clearLocationLineEdit(self):
        self.ui.selectedFolderLabel.setText("")

    @Slot()
    def pasteAPIKey(self):
        clipboard = QGuiApplication.clipboard()
        mimeData = clipboard.mimeData()
        if mimeData.hasText():
            self.ui.apiKeyLineEdit.setText(mimeData.text())
            self.ui.apiKeyLineEdit.setVisible(False)
            self.ui.apiKeyLineEdit.setVisible(True)
            self.ui.apiKeyLineEdit.update()    

    def updateBreadCrumbLabel(self):
        path = "/"
        for p in self.bread_crumb_path:
            path = path + p + "/"

        self.ui.breadcrumbLabel.setText(path)
        self.ui.breadcrumbLabel.setVisible(False)
        self.ui.breadcrumbLabel.setVisible(True)
        self.ui.breadcrumbLabel.update()        
    
    def htPathFromBreadCrumbs(self) -> str:
        path = "/"
        for p in self.bread_crumb_path:
            path = path + p + "/"
        return path        

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
            self.setWindowTitle("Authenticated to: " + self.authcontrol.base_url + " with User: " + self.authcontrol.get_username())

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
        
        if puid == "":
            return

        folderlist = ht_requests.get_item_dict_from_ht_path(self.authcontrol, 
            ht_path = '/', 
            ht_space = 'project',
            ht_space_id=puid)

        self.remote_file_list_model.setRemoteItemList(folderlist)
        self.ui.selectedFolderLabel.setText("")
        self.ui.folderListView.setModel(self.remote_file_list_model)
        self.bread_crumb_path = list()
        self.updateBreadCrumbLabel()
            
        if self.init_col_width == False:
            self.init_col_width = True
            self.ui.folderListView.setColumnWidth(0, 250)


    def ascendingDirectories(self, myIndex):
        try:
            selected_row = myIndex.row()
            selected_type = self.remote_file_list_model.type_list[selected_row]
            if selected_type is not None and selected_type != "Folder":
                return

            folder_name = self.remote_file_list_model.data(myIndex, Qt.DisplayRole)
            self.bread_crumb_path.append(folder_name)
            self.updateBreadCrumbLabel()

            folderlist = ht_requests.get_item_dict_from_ht_path(self.authcontrol, 
                ht_path = self.htPathFromBreadCrumbs(), 
                ht_space = 'project',
                ht_space_id=self.current_project["content"]["pk"])

            self.remote_file_list_model.setRemoteItemList(folderlist)
            self.ui.selectedFolderLabel.setText("")
            self.ui.folderListView.selectionModel().clearSelection()

            if len(self.bread_crumb_path) > 0:
                self.ui.parentDirectoryButton.setEnabled(True)
            
        except Exception as e:
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error during directory traversal.\n" + str(e))

    def changeLocationText(self, myIndex):
        selected_row = myIndex.row()
        selected_type = self.remote_file_list_model.type_list[selected_row]
        
        if myIndex.isValid() and selected_type == "Folder":
            self.ui.selectedFolderLabel.setText(myIndex.data())
        

    def createNewFolder(self, name):
        try:

            ht_id_path = ht_requests.get_ht_id_path_from_ht_path(self.authcontrol, 
                                ht_path = self.htPathFromBreadCrumbs(),
                                ht_space = 'project',
                                ht_space_id=self.current_project["content"]["pk"]
                                )


            folder_id = ht_requests.create_folder(self.authcontrol,
                        folder_name = name,  
                        ht_space = 'project',
                        ht_space_id = self.current_project["content"]["pk"],
                        ht_id_path= ht_id_path)

            folderlist = ht_requests.get_item_dict_from_ht_path(self.authcontrol, 
                    ht_path = self.htPathFromBreadCrumbs(), 
                    ht_space = 'project',
                    ht_space_id=self.current_project["content"]["pk"])

            self.remote_file_list_model.setRemoteItemList(folderlist)
            self.ui.selectedFolderLabel.setText("")
            self.ui.folderListView.selectionModel().clearSelection()

            if len(self.bread_crumb_path) == 0:
                self.ui.parentDirectoryButton.setEnabled(False)

        except Exception as e:
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error creating remote directory.\n" + str(e))


    def parentDirectory(self):
        try:
            self.bread_crumb_path.pop()
            self.updateBreadCrumbLabel()

            folderlist = ht_requests.get_item_dict_from_ht_path(self.authcontrol, 
                ht_path = self.htPathFromBreadCrumbs(), 
                ht_space = 'project',
                ht_space_id=self.current_project["content"]["pk"])

            self.remote_file_list_model.setRemoteItemList(folderlist)
            self.ui.selectedFolderLabel.setText("")
            self.ui.folderListView.selectionModel().clearSelection()

            if len(self.bread_crumb_path) == 0:
                self.ui.parentDirectoryButton.setEnabled(False)

        except Exception as e:
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error getting the parent directory.\n" + str(e))

    def getUploadDirectory(self):
        return self.ui.breadcrumbLabel.text() + self.ui.selectedFolderLabel.text()
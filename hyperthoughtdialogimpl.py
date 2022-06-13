from cgitb import text
import os

from typing import List
from datetime import datetime

from PySide2.QtWidgets import QDialog, QMessageBox, QApplication, QStyle, QListView, QDialogButtonBox
from PySide2.QtCore import Signal, QStringListModel, Qt, Slot
from PySide2.QtGui import QClipboard, QGuiApplication
import PySide2.QtCore

from ht_requests.ht_requests import ht_utilities
from ht_requests.ht_requests import htauthcontroller
from ht_requests.ht_requests import ht_requests
from newfolderdialogimpl import NewFolderDialogImpl
from htremotefilelistmodel import HTRemoteFileListModel
from HyperThoughtTokenVerifier import HyperThoughtTokenVerifier

qt_version = PySide2.QtCore.__version_info__
if qt_version[1] == 12:
    from generated_5_12.ui_hyperthoughtdialog import Ui_HyperthoughtDialog
elif qt_version[1] == 15:
    from generated_5_15.ui_hyperthoughtdialog import Ui_HyperthoughtDialog


class HyperthoughtDialogImpl(QDialog):

    apiSubmitted = Signal(str)
    currentTokenExpired = Signal()

    K_EXPIRED_STR = 'Access Token Expired!'
    
    def __init__(self, parent=None):
        super(HyperthoughtDialogImpl, self).__init__(parent)
        self.ui = Ui_HyperthoughtDialog()
        self.ui.setupUi(self)

        # initialize variables
        self.accessKey = ""
        self.authcontrol = None
        self.workspace_dict = {}
        self.current_workspace = {}
        self.current_folder = {}
        self.bread_crumb_path = list()
        self.remote_file_list_model = HTRemoteFileListModel(self)
        self.newfolderDialog = NewFolderDialogImpl()
        self.init_col_width = False
        self.tokenverifier = HyperThoughtTokenVerifier()

        #Setup Signals/Slots connections
        self.ui.apiKeyButton.clicked.connect(self.acceptApiKey)
        self.ui.show_files.stateChanged.connect(self.show_files_changed)
        self.ui.folderListView.clicked.connect(self.changeLocationText)
        self.ui.folderListView.doubleClicked.connect(self.ascendingDirectories)
        self.ui.parentDirectoryButton.clicked.connect(self.parentDirectory)
        self.ui.newFolderButton.clicked.connect(self.newfolderDialog.exec)
        self.newfolderDialog.nameSubmitted.connect(self.createNewFolder)
        self.ui.folderListView.selectionCleared.connect(self.clearLocationLineEdit)
        self.ui.pasteFromClipboardBtn.clicked.connect(self.pasteAPIKey)
        self.ui.workspaceListView.currentRowChanged.connect(self.workspace_row_changed)
        self.setWindowTitle("Authenticate To HyperThought")
        self.tokenverifier.currentTokenExpired.connect(self.handle_token_expired)

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)

        self.ui.folderListView.setModel(self.remote_file_list_model)
    
    @Slot()
    def show_files_changed(self, state: int):
        self.refresh_location_contents()

    @Slot()    
    def handle_token_expired(self):
        self.ui.token_expiration.setText(self.K_EXPIRED_STR)
        self.ui.workspaceListView.setDisabled(True)
        self.ui.folderListView.setDisabled(True)
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)
        self.currentTokenExpired.emit()

    @Slot()    
    def clearLocationLineEdit(self):
        self.ui.selectedFolderLabel.setText("")

    @Slot()
    def pasteAPIKey(self):
        clipboard = QGuiApplication.clipboard()
        mimeData = clipboard.mimeData()
        if mimeData.hasText():
            self.ui.apiKeyLineEdit.setText(mimeData.text())
            # self.ui.apiKeyLineEdit.setVisible(False)
            # self.ui.apiKeyLineEdit.setVisible(True)
            # self.ui.apiKeyLineEdit.update()    

    def updateBreadCrumbLabel(self):
        path = "/"
        for p in self.bread_crumb_path:
            path = path + p + "/"

        self.ui.breadcrumbLabel.setText(path)
        # self.ui.breadcrumbLabel.setVisible(False)
        # self.ui.breadcrumbLabel.setVisible(True)
        # self.ui.breadcrumbLabel.update()        
    
    def htPathFromBreadCrumbs(self) -> str:
        if len(self.bread_crumb_path) == 0:
            return ''
        
        path = "/"
        path = path.join(self.bread_crumb_path)
        path = "/" + path + "/"
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
            try:
                datetime_obj = datetime.strptime(self.authcontrol.expires_at, '%Y-%m-%dT%X.%f%z')
            except ValueError:
                datetime_obj = datetime.strptime(self.authcontrol.expires_at, '%Y-%m-%dT%H:%M:%S%z')
            expires_at = datetime_obj.strftime("%m/%d/%Y %I:%M:%S %p")
            self.ui.token_expiration.setText(expires_at)
            self.workspace_dict = ht_requests.list_workspaces(self.authcontrol)
            self.ui.workspaceListView.clear()
            self.tokenverifier.setExpireTime(self.authcontrol.expires_in)
            self.ui.workspaceListView.setEnabled(True)
            self.ui.folderListView.setEnabled(True)
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            for workspace in self.workspace_dict:
                self.ui.workspaceListView.addItem(workspace["name"])
            self.setWindowTitle("Authenticated to: " + self.authcontrol.base_url + " with User: " + self.authcontrol.get_username())

        except Exception as e:
             QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error during the authentication process.\n" + str(e))


    @Slot()
    def workspace_row_changed(self, currentRow: int):
        workspace_title = self.ui.workspaceListView.currentItem().text()

        # Find the projects uuid
        for workspace in self.workspace_dict:
            if workspace_title == workspace["name"]:
                self.current_workspace = workspace
                self.current_folder = None
                break
        
        # If the UUID is valid then get the item list from that location
        if self.current_workspace["id"] == "":
            return
        
        self.bread_crumb_path = list()
        self.updateBreadCrumbLabel()

        self.refresh_location_contents()

        if self.init_col_width == False:
            self.init_col_width = True
            self.ui.folderListView.setColumnWidth(0, 250)

    def ascendingDirectories(self, myIndex):
        try:
            selected_row = myIndex.row()
            ht_item = self.remote_file_list_model.item_list[selected_row]
            selected_type = ht_item['ftype']
            if selected_type is not None and selected_type != "Folder":
                return

            folder_name = self.remote_file_list_model.data(myIndex, Qt.DisplayRole)
            
            for ht_item in self.current_folder_contents:
                if ht_item['ftype'] == 'Folder' and ht_item['name'] == folder_name:
                    self.current_folder = ht_item
                    break

            self.bread_crumb_path.append(folder_name)
            self.updateBreadCrumbLabel()

            self.refresh_location_contents()
            
        except Exception as e:
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error during directory traversal.\n" + str(e))

    def changeLocationText(self, myIndex):
        selected_row = myIndex.row()
        ht_item = self.remote_file_list_model.item_list[selected_row]
        selected_type = ht_item['ftype']
        
        if myIndex.isValid() and selected_type == "Folder":
            self.ui.selectedFolderLabel.setText(myIndex.data())
        

    def createNewFolder(self, name):
        try:
            current_folder_ht_id_path = self._get_current_folder_ht_id_path()

            ht_requests.create_folder(self.authcontrol,
                                      folder_name = name,  
                                      workspace_id = self.current_workspace["id"],
                                      ht_id_path = current_folder_ht_id_path)
            
            self.refresh_location_contents()

        except Exception as e:
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error creating remote directory.\n" + str(e))
    
    def refresh_location_contents(self):
        current_folder_ht_id_path = self._get_current_folder_ht_id_path()

        self.list_location_contents(current_folder_ht_id_path)

    def list_location_contents(self, ht_id_path: str):
        item_type = ht_requests.ItemType.folders
        if self.ui.show_files.isChecked():
            item_type = ht_requests.ItemType.folders_and_files

        self.current_folder_contents = ht_requests.list_location_contents(self.authcontrol, 
                    ht_path = ht_id_path, 
                    workspace_id = self.current_workspace["id"],
                    item_type=item_type)

        self.remote_file_list_model.setRemoteItemList(self.current_folder_contents)
        self.ui.selectedFolderLabel.setText("")
        self.ui.folderListView.selectionModel().clearSelection()

        self.ui.parentDirectoryButton.setEnabled(len(self.bread_crumb_path) > 0)

    def parentDirectory(self):
        try:
            self.bread_crumb_path.pop()
            self.updateBreadCrumbLabel()

            parent_ht_path_id: str = self.current_folder['path']
            if parent_ht_path_id == ',':
                self.current_folder = None
            else:
                parent_ht_path_id_parts = [x for x in parent_ht_path_id.split(',') if x != '']
                parent_ht_id = parent_ht_path_id_parts.pop()
                self.current_folder = ht_requests.get_item_info(self.authcontrol, parent_ht_id)
            
            self.refresh_location_contents()

        except Exception as e:
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error getting the parent directory.\n" + str(e))

    def get_workspace(self):
        return self.current_workspace

    def get_parent_folder(self):
        return self.current_folder

    def get_chosen_folder(self):
        for ht_item in self.current_folder_contents:
            if ht_item['ftype'] == 'Folder' and ht_item['name'] == self.ui.selectedFolderLabel.text():
                return ht_item
        
        return None
    
    def _get_current_folder_ht_id_path(self) -> str:
        if self.current_folder is not None:
            return self.current_folder['path'] + self.current_folder['pk'] + ','
        
        return ','

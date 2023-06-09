from PySide6.QtWidgets import QDialog, QMessageBox, QApplication, QDialogButtonBox
from PySide6.QtCore import Signal, Qt, Slot
from PySide6.QtGui import QGuiApplication
import PySide6.QtCore

import hyperthought as ht

from metaforge.widgets.newfolderdialogimpl import NewFolderDialogImpl
from metaforge.models.htremotefilelistmodel import HTRemoteFileListModel

from metaforge.widgets.generated_6_5.ui_hyperthoughtdialog import Ui_HyperthoughtDialog

class HyperthoughtDialogImpl(QDialog):
    
    def __init__(self, parent=None):
        super(HyperthoughtDialogImpl, self).__init__(parent)
        self.ui = Ui_HyperthoughtDialog()
        self.ui.setupUi(self)

        # initialize variables
        self.accessKey = ""
        self.authcontrol = None
        self.files_api = None
        self.workspace_dict = {}
        self.current_workspace = None
        self.current_folder = {}
        self.bread_crumb_path = list()
        self.remote_file_list_model = HTRemoteFileListModel(self)
        self.newfolderDialog = NewFolderDialogImpl()
        self.init_col_width = False

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

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setDisabled(True)

        self.ui.folderListView.setModel(self.remote_file_list_model)
    
    @Slot()
    def show_files_changed(self, state: int):
        self.refresh_current_folder()

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

        try:
            self.authcontrol = ht.auth.Authorization(self.accessKey, verify=False)
            self.files_api = ht.api.files.FilesAPI(auth=self.authcontrol)
            self.workspaces_api = ht.api.workspaces.WorkspacesAPI(auth=self.authcontrol)
            self.ui.ht_server_url.setText(self.authcontrol.get_base_url())
            self.ui.ht_username.setText(self.authcontrol.get_username())
            self.ui.workspaceListView.setEnabled(True)
            self.ui.folderListView.setEnabled(True)
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            self.refresh_workspace_list()
            self.setWindowTitle("Authenticated to: " + self.authcontrol.get_base_url() + " with User: " + self.authcontrol.get_username())

        except Exception as e:
             QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error during the authentication process.\n" + str(e))


    @Slot()
    def workspace_row_changed(self, currentRow: int):
        workspace_title = self.ui.workspaceListView.currentItem().text()

        # Find the workspace uuid
        self.current_workspace = None
        self.current_folder = None
        self.workspace_dict = self.workspaces_api.get_workspaces()
        matching_workspaces = [workspace for workspace in self.workspace_dict if workspace_title == workspace["name"]]
        if len(matching_workspaces) > 0:
            self.current_workspace = matching_workspaces[0]
        
        # If the workspace is not valid, throw up a warning dialog and refresh the workspace list
        if self.current_workspace == None:
            QMessageBox.warning(self, QApplication.applicationDisplayName(), f"The chosen workspace '{workspace_title}' no longer exists.\nThe workspace list will be refreshed.")
            self._refresh_workspace_list(self.workspace_dict)
            self.remote_file_list_model.removeRows(0, self.remote_file_list_model.rowCount() - 1)
            return
        
        self.bread_crumb_path = list()
        self.updateBreadCrumbLabel()

        self.refresh_current_folder()

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

            self.refresh_current_folder()
            
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

            self.files_api.create_folder(name=name,
                                         space_id=self.current_workspace["id"],
                                         path=current_folder_ht_id_path)
            
            self.refresh_current_folder()

        except Exception as e:
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error creating remote directory.\n" + str(e))
    
    def refresh_workspace_list(self):
        self.workspace_dict = self.workspaces_api.get_workspaces()
        self._refresh_workspace_list(self.workspace_dict)
        
    def _refresh_workspace_list(self, workspaces):
        self.ui.workspaceListView.clear()
        for workspace in workspaces:
            self.ui.workspaceListView.addItem(workspace["name"])

    def refresh_current_folder(self):
        current_folder_ht_id_path = self._get_current_folder_ht_id_path()

        self.list_location_contents(current_folder_ht_id_path)

    def list_location_contents(self, ht_id_path: str):
        file_type = ht.api.files.FilesAPI.FileType.FOLDERS_ONLY
        if self.ui.show_files.isChecked():
            file_type = ht.api.files.FilesAPI.FileType.FILES_AND_FOLDERS

        self.current_folder_contents = self.files_api.get_from_location(space_id=self.current_workspace["id"],
                                         path=ht_id_path,
                                         file_type=file_type)

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
                self.current_folder = self.files_api.get_document(id=parent_ht_id)
            
            self.refresh_current_folder()

        except Exception as e:
            QMessageBox.warning(None, QApplication.applicationDisplayName(), "Error getting the parent directory.\n" + str(e))

    def get_auth_control(self):
        return self.authcontrol

    def get_workspace(self):
        return self.current_workspace

    def get_chosen_folder(self):
        if self.authcontrol is None:
            return None

        if not self.ui.selectedFolderLabel.text():
            return self.current_folder

        for ht_item in self.current_folder_contents:
            if ht_item['ftype'] == 'Folder' and ht_item['name'] == self.ui.selectedFolderLabel.text():
                return ht_item
        
        return None
    
    def _get_current_folder_ht_id_path(self) -> str:
        if self.current_folder is not None:
            return self.files_api.get_id_path(path=self.current_folder['path_string'],
                                              space_id=self.current_workspace['id'])
            # return self.current_folder['path'] + self.current_folder['pk'] + ','
        
        return self.files_api.get_id_path(path='/', space_id=self.current_workspace['id'])

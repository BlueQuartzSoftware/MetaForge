from PySide2.QtNetwork import QNetworkReply
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide2.QtGui import QIcon, QColor
from PySide2.QtWidgets import QApplication, QStyle



class HTRemoteFileListModel(QAbstractTableModel):

    K_NAME_COL_INDEX = 0
    K_TYPE_COL_INDEX = 1

    K_NAME_COL_NAME = "Name"
    K_TYPE_COL_NAME = "Kind"

    K_COL_COUNT: int = 2

    def __init__(self,hyperthoughtimpl,parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.hyperthoughtimpl = hyperthoughtimpl
        self.item_list = []
        self.uuid_list = []
        self.type_list = []

    def setRemoteItemList(self, folderlist):
        if self.item_list != []:
            self.beginRemoveRows(self.index(0,0), len(self.item_list),len(self.item_list))
            self.item_list = []
            self.uuid_list = []
            self.type_list = []
            self.endRemoveRows()

        for i in range(len(folderlist)):
            self.beginInsertRows(self.index(len(self.item_list),0), len(self.item_list),len(self.item_list))
            self.item_list.append(folderlist[i]["Name"])
            self.uuid_list.append(folderlist[i]["UUID"])
            self.type_list.append(folderlist[i]["Type"])
            self.endInsertRows()

    def rowCount(self, parent=QModelIndex()):
        return len(self.item_list)
    
    def columnCount(self, parent: QModelIndex) -> int:
        return self.K_COL_COUNT

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == self.K_NAME_COL_INDEX:
                return self.item_list[index.row()]
            if index.column() == self.K_TYPE_COL_INDEX:
                return self.type_list[index.row()]

        return None

    def setData(self, index, value, role):
        if role == Qt.DisplayRole:
            if not index.isValid():
                return False
            return index.row()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            if section == self.K_NAME_COL_INDEX:
                return self.K_NAME_COL_NAME
            elif section == self.K_TYPE_COL_INDEX:
                return self.K_TYPE_COL_NAME    
        
        return None


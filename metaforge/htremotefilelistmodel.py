import math
from datetime import datetime

from PySide2.QtNetwork import QNetworkReply
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide2.QtGui import QIcon, QColor
from PySide2.QtWidgets import QApplication, QStyle



class HTRemoteFileListModel(QAbstractTableModel):

    K_NAME_COL_INDEX = 0
    K_SIZE_COL_INDEX = 1
    K_TYPE_COL_INDEX = 2
    K_ITEMS_COL_INDEX = 3
    K_MODDATE_COL_INDEX = 4
    K_MODBY_COL_INDEX = 5

    K_NAME_COL_NAME = "Name"
    K_SIZE_COL_NAME = "Size"
    K_TYPE_COL_NAME = "Type"
    K_ITEMS_COL_NAME = "Items"
    K_MODDATE_COL_NAME = "Modified Date"
    K_MODBY_COL_NAME = "Modified By"

    K_COL_COUNT: int = 6

    def __init__(self,hyperthoughtimpl,parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.hyperthoughtimpl = hyperthoughtimpl
        self.item_list = []

    def setRemoteItemList(self, folderlist):
        if self.item_list != []:
            self.beginRemoveRows(QModelIndex(), len(self.item_list),len(self.item_list))
            self.item_list = []
            self.endRemoveRows()

        for i in range(len(folderlist)):
            self.beginInsertRows(QModelIndex(), len(self.item_list),len(self.item_list))
            self.item_list.append(folderlist[i])
            self.endInsertRows()

    def rowCount(self, parent=QModelIndex()):
        return len(self.item_list)
    
    def columnCount(self, parent: QModelIndex) -> int:
        return self.K_COL_COUNT

    def data(self, index, role):
        if role == Qt.DisplayRole:
            ht_item = self.item_list[index.row()]
            if index.column() == self.K_NAME_COL_INDEX:
                return ht_item['name']
            if index.column() == self.K_SIZE_COL_INDEX:
                size_bytes = ht_item['size']
                size = self._convert_size(size_bytes)
                return size
            if index.column() == self.K_TYPE_COL_INDEX:
                return ht_item['ftype']
            if index.column() == self.K_ITEMS_COL_INDEX:
                if ht_item['ftype'] == 'Folder':
                    return ht_item['items']
                else:
                    return ""
            if index.column() == self.K_MODDATE_COL_INDEX:
                mod_on = ht_item['modifiedOn']
                date_time: datetime = datetime.strptime(mod_on, "%Y-%m-%dT%H:%M:%S.%f%z")
                mod_on = date_time.strftime("%b %d, %Y %-I:%M %p")
                return mod_on
            if index.column() == self.K_MODBY_COL_INDEX:
                return ht_item['modifiedBy']

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
            elif section == self.K_SIZE_COL_INDEX:
                return self.K_SIZE_COL_NAME
            elif section == self.K_TYPE_COL_INDEX:
                return self.K_TYPE_COL_NAME
            elif section == self.K_ITEMS_COL_INDEX:
                return self.K_ITEMS_COL_NAME
            elif section == self.K_MODDATE_COL_INDEX:
                return self.K_MODDATE_COL_NAME
            elif section == self.K_MODBY_COL_INDEX:
                return self.K_MODBY_COL_NAME
        
        return None
    
    def _convert_size(self, size: int):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']:
            if size < 1000.0:
                return "%3.1f %s" % (size, x)
            size /= 1000.0

        return size


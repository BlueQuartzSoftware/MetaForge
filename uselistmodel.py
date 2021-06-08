from PySide2.QtNetwork import QNetworkReply
from PySide2.QtCore import QAbstractListModel, QMimeData, Qt, QModelIndex
from PySide2.QtGui import QIcon, QColor
from PySide2.QtWidgets import QApplication, QStyle



class ListModel(QAbstractListModel):
    def __init__(self,data,tablemodel,fileList ,parent=None):
        QAbstractListModel.__init__(self, parent)
        self.metadataList = fileList
        self.tablemodel = tablemodel

    def flags(self, index):
        defaultFlags = QAbstractListModel.flags(self,index);
        return Qt.ItemIsDropEnabled | defaultFlags;

    def canDropMimeData(self, data, action, row, column, parent):
        return data.hasUrls()

    def dropMimeData(self, data, action, row, column, parent):
        for file in data.urls():
            self.addRow(file.path())
        return True


    def rowCount(self, parent=QModelIndex()):
        return len(self.metadataList)

    def columnCount(self, parent=QModelIndex()):
        return 1

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self.metadataList[index.row()].split("/")[-1]
        return None

    def setData(self,index, value, role):
        if role == Qt.EditRole:
            if not index.isValid():
                return False
            if index.column() == 0:
                self.dataChanged.emit(index, index)
                return index.row()

    def addRow(self, filename):
        self.beginInsertRows(self.index(len(self.metadataList),0), len(self.metadataList),len(self.metadataList))
        self.metadataList.append(filename)
        self.endInsertRows()




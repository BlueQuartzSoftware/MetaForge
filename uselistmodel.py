from PySide2.QtNetwork import QNetworkReply
from PySide2.QtCore import QAbstractListModel, Qt, QModelIndex
from PySide2.QtGui import QIcon, QColor
from PySide2.QtWidgets import QApplication, QStyle



class ListModel(QAbstractListModel):
    def __init__(self,data,tablemodel ,parent=None):
        QAbstractListModel.__init__(self, parent)
        self.metadataList = ["Somefile.xml","SomeFileEvilTwin.xml"]
        self.tablemodel = tablemodel



    def rowCount(self, parent=QModelIndex()):
        return len(self.metadataList)

    def columnCount(self, parent=QModelIndex()):
        return 1

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self.metadataList[index.row()]

        return None


    def setData(self,index, value, role):
        if role == Qt.EditRole:
            if not index.isValid():
                return False
            if index.column() == 0:
                return index.row()



    def addRow(self, dataDict, source, value):
        self.beginInsertRows(self.index(len(self.metadataList),0), len(self.metadataList),len(self.metadataList))
        self.metadataList.append({"Key":value,"Value":dataDict[value],"Source":source+value,"Checked":Qt.Unchecked})
        self.endInsertRows()




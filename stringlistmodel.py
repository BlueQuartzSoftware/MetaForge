from PySide2.QtNetwork import QNetworkReply
from PySide2.QtCore import QAbstractListModel, Qt, QModelIndex
from PySide2.QtGui import QIcon, QColor
from PySide2.QtWidgets import QApplication, QStyle



class StringListModel(QAbstractListModel):
    def __init__(self,hyperthoughtimpl,parent=None):
        QAbstractListModel.__init__(self, parent)
        self.hyperthoughtimpl = hyperthoughtimpl
        self.directoryList = []
        self.uuidList = []




    def getLists(self, folderlist):
        if self.directoryList != []:
            print(self.directoryList)
            self.beginRemoveRows(self.index(len(self.directoryList),0), len(self.directoryList),len(self.directoryList))
            self.directoryList = []
            self.uuidList = []
            self.endRemoveRows()
        for i in range(len(folderlist)):
            self.beginInsertRows(self.index(len(self.directoryList),0), len(self.directoryList),len(self.directoryList))
            self.directoryList.append(folderlist[i]["content"]["name"])
            self.endInsertRows()
            self.uuidList.append(folderlist[i]["content"]["pk"])

    def rowCount(self, parent=QModelIndex()):
        return len(self.directoryList)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.directoryList[index.row()]#.split("/")[-1]

        return None


    def setData(self,index, value, role):
        if role == Qt.DisplayRole:
            if not index.isValid():
                return False
            return index.row()




    def addRow(self, filename):
        self.beginInsertRows(self.index(len(self.directoryList),0), len(self.directoryList),len(self.directoryList))
        self.directoryList.append(filename)
        self.endInsertRows()


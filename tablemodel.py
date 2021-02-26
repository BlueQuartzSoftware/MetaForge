from PySide2.QtNetwork import QNetworkReply
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex



class TableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.metadataList = []
        self.metadataList.append(["Date","Tues Aug 22 03:09:35 2017","/States/SEMEColumnState/Date"])
        self.metadataList.append(["TimeStamp","1503385775.990084","/States/SEMEColumnState/TimeStamp"])


    def rowCount(self, parent=QModelIndex()):
        return len(self.metadataList)

    def columnCount(self, parent=QModelIndex()):
        return 9

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return index.row()
            elif index.column() == 1:
                return self.metadataList[index.row()][0]
            elif index.column() == 2:
                return self.metadataList[index.row()][1]
            elif index.column() == 3:
                return self.metadataList[index.row()][2]
            #elif index.column() == 4:
            #    return self.metadataList[index.row()][0]
            #elif index.column() == 5:
            #    if isString
            #elif index.column() == 6:
            #    return self.metadataList[index.row()][0]
            #elif index.column() == 7:
            #    return self.metadataList[index.row()][0]
            #elif index.column() == 8:
            #    return self.metadataList[index.row()][0]

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            if section == 0:
                return "#^"
            elif section == 1:
                return "Key"
            elif section == 2:
                return "Value"
            elif section == 3:
                return "Source"
            elif section == 4:
                return "Default Value"
            elif section == 5:
                return "Type"
            elif section == 6:
                return "Require"
            elif section == 7:
                return "Editable"
            elif section == 8:
                return " "
            return None
    def setData(self,index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            if not index.isValid():
                return False
            self.metadataList[index.row()][index.column()] = value
            self.dataChanged.emit(index,index)
            return True

        return False

    def flags(self, index):
        if not index.isValid():

            return Qt.ItemIsEnabled

        return Qt.ItemFlags(QAbstractTableModel.flags(self,index) | Qt.ItemIsEditable)

#    def appendDownload(self, urlValue):
#        currentDownload = Download(urlValue)
#        currentDownload.downloadProgress['qint64', 'qint64'].connect(self.handleProgress)
#        self.beginInsertRows(QModelIndex(), self.rowCount() + 1, self.rowCount() + 1)
#        self.metadataList.append(currentDownload)
#        self.endInsertRows()

  #  def handleProgress(self, current, total):
  #      row = self.metadataList.index(self.sender())
  #      topleft = self.createIndex(row, 1)
 #       self.dataChanged.emit(topleft, topleft)

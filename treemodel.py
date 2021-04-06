# This Python file uses the following encoding: utf-8


from PySide2.QtCore import QAbstractItemModel, QFile, QIODevice, QItemSelectionModel, QModelIndex, QObject ,Qt, Signal, Slot
from PySide2.QtWidgets import QApplication, QMainWindow
from treeitem import TreeItem


class TreeModel(QAbstractItemModel):
    checkChanged = Signal(int, str)
    def __init__(self, headers, data, tableview, parent=None):
        super(TreeModel, self).__init__(parent)

        rootData = [header for header in headers]
        self.rootItem = TreeItem(rootData)
        self.treeDict= data
        self.setupModelData(data, self.rootItem)
        self.tableview = tableview


    def changeLeafCheck(self, source):
        #print(source)
        curNode = self.rootItem.child(0)
        keyNames = source.split("/")


        for key in keyNames:
            for i in range(curNode.childCount()):
                print(key,curNode.child(i).itemData)
                if curNode.child(i).itemData[0] == key:
                        curNode = curNode.child(i)
                        break
        print(curNode.itemData)

        curNode.switchChecked()
        self.checkChanged.emit(Qt.Unchecked,source)
        self.dataChanged.emit(0, 0)

    def columnCount(self, parent=QModelIndex()):
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        item = self.getItem(index)
        if role == Qt.DisplayRole:
            return item.data(index.column())
        elif role == Qt.CheckStateRole:
            return item.checked

        return None


    def flags(self, index):
        if not index.isValid():
            return 0

        return Qt.ItemIsUserCheckable | super(TreeModel, self).flags(index)

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def insertColumns(self, position, columns, parent=QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self.rootItem.insertColumns(position, columns)
        self.endInsertColumns()

        return success

    def insertRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows,
                self.rootItem.columnCount())
        self.endInsertRows()

        return success

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def removeColumns(self, position, columns, parent=QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self.rootItem.removeColumns(position, columns)
        self.endRemoveColumns()

        if self.rootItem.columnCount() == 0:
            self.removeRows(0, self.rowCount())

        return success

    def removeRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success

    def rowCount(self, parent=QModelIndex()):
        parentItem = self.getItem(parent)

        return parentItem.childCount()

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
           item = self.getItem(index)
           result = item.setData(index.column(), value)
           if result:
               self.dataChanged.emit(index, index)
               return result
        elif role == Qt.CheckStateRole:
            item = self.getItem(index)
            item.switchChecked()
            checked= item.checked
            source=""
            sourceList= []

            while item.parentItem:
                sourceList.insert(0,item.itemData[0]+"/")
                item = item.parentItem

            self.checkChanged.emit(checked,source.join(sourceList)[:-1])
            self.dataChanged.emit(index, index)
            return True
        return False


    def setHeaderData(self, section, orientation, value, role=Qt.EditRole):
        if role != Qt.EditRole or orientation != Qt.Horizontal:
            return False

        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result

    def setupModelData(self, data, parent):
             visited={}
             queue=[]
             parents = {}

             for key in data.keys():
                 visited[(parent.itemData[0])]=[key]
                 queue.append(key)
                 parents[key] = (data[key],parent)
             curDict = data

             while queue:
                 child = queue.pop(0)
                 if child in parents:
                     parent = parents[child][1]
                 parent.insertChildren(parent.childCount(),1,self.rootItem.columnCount())
                 parent.child(parent.childCount() -1).setData(0,child)

                 if child in parents:

                     curDict =  parents[child][0]
                     for curChild in range(parents[child][1].childCount()):
                         if child == parents[child][1].child(curChild).itemData[0]:
                            parent = parents[child][1].child(curChild)
                            visited[(parent.itemData[0])]=[]

                 if isinstance(curDict, dict):
                     #visited[(parent.itemData[0])]=[]
                     for key in curDict.keys():
                         if key not in visited[(parent.itemData[0])]:
                             visited[(parent.itemData[0])].append(key)
                             queue.append(key)
                             if (isinstance(curDict[key],dict)):
                                parents[key]= (curDict[key],parent)

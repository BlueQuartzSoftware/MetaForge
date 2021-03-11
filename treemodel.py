# This Python file uses the following encoding: utf-8


from PySide2.QtCore import QAbstractItemModel, QFile, QIODevice, QItemSelectionModel, QModelIndex, Qt
from PySide2.QtWidgets import QApplication, QMainWindow
from treeitem import TreeItem


class TreeModel(QAbstractItemModel):
    def __init__(self, headers, data, parent=None):
        super(TreeModel, self).__init__(parent)

        rootData = [header for header in headers]
        self.rootItem = TreeItem(rootData)
        self.treeDict= data
        self.setupModelData(data, self.rootItem)

    def columnCount(self, parent=QModelIndex()):
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            item = self.getItem(index)
            return item.data(index.column())
        elif role == Qt.CheckStateRole:
            return Qt.Checked

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
        if role != Qt.EditRole:
            return False

        item = self.getItem(index)
        print(item)
        result = item.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index)

        return result

    def setHeaderData(self, section, orientation, value, role=Qt.EditRole):
        if role != Qt.EditRole or orientation != Qt.Horizontal:
            return False

        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result

    def setupModelData(self, data, parent):
#        parents = [parent]
#        indentations = [0]

#        number = 0

#        while number < len(lines):
#            position = 0
#            while position < len(lines[number]):
#                if lines[number][position] != " ":
#                    break
#                position += 1

#            lineData = lines[number][position:].strip()

#            if lineData:
#                # Read the column data from the rest of the line.
#                columnData = [s for s in lineData.split('\t') if s]

#                if position > indentations[-1]:
#                    # The last child of the current parent is now the new
#                    # parent unless the current parent has no children.

#                    if parents[-1].childCount() > 0:
#                        parents.append(parents[-1].child(parents[-1].childCount() - 1))
#                        indentations.append(position)

#                else:
#                    while position < indentations[-1] and len(parents) > 0:
#                        parents.pop()
#                        indentations.pop()

#                # Append a new item to the current parent's list of children.
#                parent = parents[-1]
#                parent.insertChildren(parent.childCount(), 1,
#                        self.rootItem.columnCount())
#                for column in range(len(columnData)):
#                    parent.child(parent.childCount() -1).setData(column, columnData[column])

#            number += 1
             visited=[]
             queue=[]

             for key in data.keys():
                 visited.append(key)
                 queue.append(key)
             curDict = data
             while queue:
                 child = queue.pop()
                 parent.insertChildren(parent.childCount(),1,self.rootItem.columnCount())
                 parent.child(parent.childCount() -1).setData(0,child)

                 if child in curDict.keys() and isinstance(curDict[child],dict):
                     curDict = curDict[child]
                     parent=parent.child(parent.childCount() -1)



                 if isinstance(curDict, dict):
                     for key in curDict.keys():
                         if key not in visited:

                             visited.append(key)
                             queue.append(key)
                             #print(key)


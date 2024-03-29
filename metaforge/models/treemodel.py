# This Python file uses the following encoding: utf-8


from PySide6.QtCore import QAbstractItemModel, QFile, QIODevice, QItemSelectionModel, QModelIndex, QObject, Qt, Signal, Slot
from PySide6.QtWidgets import QApplication, QMainWindow
from metaforge.models.treeitem import TreeItem

from metaforge.models.metadatamodel import MetadataModel
from metaforge.models.metadataentry import MetadataEntry


class TreeModel(QAbstractItemModel):
    checkChanged = Signal(str)

    def __init__(self, header, metadata_model: MetadataModel, parent=None):
        super(TreeModel, self).__init__(parent)

        self.rootItem = TreeItem(display_name=header)
        self.setupModelData(metadata_model)

    def changeLeafCheck(self, entry: MetadataEntry):
        index = self._get_index_from_entry(entry)
        if index.isValid():
            self.setData(index, 0, Qt.CheckStateRole)

    def columnCount(self, parent=QModelIndex()):
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        item = self.getItem(index)
        if role == Qt.DisplayRole:
            return item.get_display_name()
        elif role == Qt.CheckStateRole:
            return item.get_check_state()

        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        flags = Qt.ItemIsEnabled | Qt.ItemIsUserCheckable

        if self.hasChildren(index):
            flags = flags | Qt.ItemIsAutoTristate
        
        return flags

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.rootItem

    def get_index_from_item(self, item: TreeItem) -> QModelIndex:
        if item is not None:
            return self.createIndex(item.childNumber(), 0, item)

        return QModelIndex()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.get_display_name()

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

    def insertRows(self, position, rows, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows)
        self.endInsertRows()

        return success

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = self.getItem(index)
        parentItem = childItem.parent()

        if parentItem is None or parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)

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
            item.display_name = value
            self.dataChanged.emit(index, index)
            return True
        elif role == Qt.CheckStateRole:
            value = Qt.CheckState(value)
            item = self.getItem(index)
            item.set_check_state(value)
            self._notify_data_changed(item)
            self._notify_parents_data_changed(item)
            self._notify_children_data_changed(item)
            return True
        return False

    def _notify_parents_data_changed(self, item: TreeItem):
        parent_item = item.parent()
        if parent_item is not None:
            self._notify_data_changed(parent_item)
            self._notify_parents_data_changed(parent_item)

    def _notify_children_data_changed(self, item: TreeItem):
        for child_item in item.childItems:
            self._notify_data_changed(child_item)
            self._notify_children_data_changed(child_item)

    def _notify_data_changed(self, item: TreeItem):
        index = self.get_index_from_item(item)
        self.dataChanged.emit(index, index)
        item_path = self._get_item_path(item)
        self.checkChanged.emit(item_path)

    def _get_item_path(self, item: TreeItem) -> str:
        path_list = []
        path = "/"
        current_item = item
        while current_item is not self.rootItem:
            path_list.insert(0, current_item.display_name)
            current_item = current_item.parent()

        path = path.join(path_list)
        return path
    
    def _get_item_from_entry(self, entry: MetadataEntry) -> TreeItem:
        def recurse(entry: MetadataEntry, item: TreeItem):
            if item.metadata_entry == entry:
                return item

            for child_item in item.childItems:
                item = recurse(entry, child_item)
                if item is not None:
                    return item
            
            return None

        return recurse(entry, self.rootItem)
    
    def _get_index_from_entry(self, entry: MetadataEntry) -> QModelIndex:
        tree_item = self._get_item_from_entry(entry)
        return self.get_index_from_item(tree_item)

    def setHeaderData(self, section, orientation, value, role=Qt.EditRole):
        if role != Qt.EditRole or orientation != Qt.Horizontal:
            return False

        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result

    def clearModel(self):
        self.removeRows(0, self.rowCount())

    def setupModelData(self, metadata_model: MetadataModel):
        for entry in metadata_model.entries:
            if entry.source_type is not MetadataEntry.SourceType.FILE or entry.loaded is False:
                continue

            source_path = entry.source_path
            source_tokens = source_path.split('/')
            tree_item = self.rootItem
            tree_index = QModelIndex()
            for i in range(len(source_tokens)):
                token = source_tokens[i]
                child_item = tree_item.child_by_name(token)
                if child_item is None:
                    self.insertRows(tree_item.childCount(), 1, tree_index)
                    child_item = tree_item.child(tree_item.childCount() - 1)
                    child_item.display_name = token
                    if i == len(source_tokens) - 1:
                        child_item.metadata_entry = entry
                tree_index = self.index(tree_item.childCount() - 1,
                                        0, parent=tree_index)
                tree_item = child_item

    def uncheckChildren(self, index, value):
        if not index.isValid():
            return
        else:
            childCount = self.rowCount(index)
            for i in range(childCount):
                child = index.child(i, 0)
                self.setData(child, value, Qt.CheckStateRole)
                self.uncheckChildren(child, value)

from __future__ import annotations
from typing import List
from PySide2.QtCore import Qt

from metaforge.models.metadataentry import MetadataEntry

class TreeItem(object):
    def __init__(self, display_name: str, metadata_entry: MetadataEntry = None, parent=None):
        self.parentItem = parent
        self.display_name: str = display_name
        self.metadata_entry: MetadataEntry = metadata_entry
        self.childItems: List[TreeItem] = []

    def checked(self):
        return self.check_state

    def child(self, row) -> TreeItem:
        return self.childItems[row]

    def child_by_name(self, name):
        for child_item in self.childItems:
            if child_item.get_display_name() == name:
                return child_item

        return None

    def childCount(self):
        return len(self.childItems)

    def childNumber(self):
        if self.parentItem != None:
            return self.parentItem.childItems.index(self)
        return 0

    def columnCount(self):
        return 1

    def get_display_name(self):
        return self.display_name

    def get_check_state(self):
        if self.metadata_entry is None:
            all_checked = True
            all_unchecked = True
            for child_item in self.childItems:
                child_check_state = child_item.get_check_state()
                if child_check_state is Qt.Checked:
                    all_unchecked = False
                elif child_check_state is Qt.Unchecked:
                    all_checked = False
                else:
                    all_checked = False
                    all_unchecked = False
            if all_checked is True:
                return Qt.Checked
            elif all_unchecked is True:
                return Qt.Unchecked
            else:
                return Qt.PartiallyChecked
        else:
            if self.metadata_entry.enabled is True:
                return Qt.Checked
            else:
                return Qt.Unchecked

    def set_check_state(self, check_state: Qt.CheckState):
        if self.metadata_entry is None:
            for child_item in self.childItems:
                child_item.set_check_state(check_state)
        else:
            if check_state == Qt.Checked:
                self.metadata_entry.enabled = True
            elif check_state == Qt.Unchecked:
                self.metadata_entry.enabled = False
            else:
                raise RuntimeError('Tree leaf check state cannot be partial!')

    def insertChildren(self, position, count):
        if position < 0 or position > len(self.childItems):
            return False

        for num in range(count):
            item = TreeItem(None, None, self)
            item.parentItem = self
            self.childItems.insert(position + num, item)

        return True

    def parent(self) -> TreeItem:
        return self.parentItem

    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.childItems):
            return False

        for row in range(count):
            self.childItems.pop(position)

        return True

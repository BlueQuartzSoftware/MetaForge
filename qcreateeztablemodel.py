from PySide2.QtCore import QSortFilterProxyModel, Qt

from ezmodel.ezmetadataentry import EzMetadataEntry

class QCreateEzTableModel(QSortFilterProxyModel):
    def __init__(self, data, parent=None):
        QSortFilterProxyModel.__init__(self, parent)
        self.setDynamicSortFilter(True)
        self.sort(0)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            if index.column() == self.sourceModel().K_SORT_COL_INDEX:
                return index.row() + 1

        return super().data(index, role)

    def filterAcceptsRow(self, source_row, source_parent):
        if self.sourceModel() is None:
            return False

        metadata_model = self.sourceModel().metadata_model
        metadata_entry: EzMetadataEntry = metadata_model.entry(source_row)

        regex = self.filterRegExp()
        match = regex.exactMatch(metadata_entry.ht_name)

        # Custom data use case
        if metadata_entry.source_type is EzMetadataEntry.SourceType.CUSTOM and match:
            return True

        # All other use cases
        if metadata_entry.source_type is EzMetadataEntry.SourceType.FILE and match:
            return metadata_entry.enabled
        else:
            return False

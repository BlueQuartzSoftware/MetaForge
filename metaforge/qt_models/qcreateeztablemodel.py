from PySide2.QtCore import QSortFilterProxyModel, Qt
from PySide2.QtGui import QColor

from metaforge.ez_models.ezmetadataentry import EzMetadataEntry
from metaforge.qt_models.qeztablemodel import QEzTableModel

class QCreateEzTableModel(QSortFilterProxyModel):
    K_NOT_LOADED_BG_COLOR = QEzTableModel.K_YELLOW_BG_COLOR

    def __init__(self, data, parent=None):
        QSortFilterProxyModel.__init__(self, parent)
        self.setDynamicSortFilter(True)
        self.sort(0)

    def data(self, index, role):
        if not index.isValid():
            return None
        
        src_model = self.sourceModel()
        if src_model is None:
            return None

        if role == Qt.DisplayRole:
            if index.column() == src_model.K_SORT_COL_INDEX:
                return index.row() + 1
        if role == Qt.BackgroundRole:
            src_index = self.mapToSource(index)
            metadata_entry: EzMetadataEntry = src_model.metadata_model.entry(src_index.row())
            return self._get_background_color_data(metadata_entry)

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
    
    def _get_background_color_data(self, metadata_entry: EzMetadataEntry) -> QColor:
        if metadata_entry.source_type is EzMetadataEntry.SourceType.FILE and metadata_entry.loaded is False:
            return self.K_NOT_LOADED_BG_COLOR

        return None

from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtGui import QColor

from typing import List
import json

from metaforge.models.metadataentry import MetadataEntry
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

        src_index = self.mapToSource(index)

        if role == Qt.DisplayRole:
            if index.column() == src_model.K_SORT_COL_INDEX:
                return src_index.row() + 1
        if role == Qt.BackgroundRole:
            metadata_entry: MetadataEntry = src_model.metadata_model.entry(src_index.row())
            return self._get_background_color_data(metadata_entry)

        return super().data(index, role)

    def filterAcceptsRow(self, source_row, source_parent):
        if self.sourceModel() is None:
            return False

        metadata_model = self.sourceModel().metadata_model
        metadata_entry: MetadataEntry = metadata_model.entry(source_row)

        regex = self.filterRegularExpression()
        result = regex.match(metadata_entry.ht_name)

        # Custom data use case
        if metadata_entry.source_type is MetadataEntry.SourceType.CUSTOM and result.hasMatch():
            return True

        # All other use cases
        if metadata_entry.source_type is MetadataEntry.SourceType.FILE and result.hasMatch():
            return metadata_entry.enabled
        else:
            return False
    
    def _get_background_color_data(self, metadata_entry: MetadataEntry) -> QColor:
        if metadata_entry is not None:
            if metadata_entry.source_type is MetadataEntry.SourceType.FILE and metadata_entry.loaded is False:
                return self.K_NOT_LOADED_BG_COLOR

        return None

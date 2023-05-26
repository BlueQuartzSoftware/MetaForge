from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex, QPersistentModelIndex, QMimeData, QByteArray, QDataStream, QIODevice
from PySide2.QtGui import QFont, QColor

from typing import List
import json

from metaforge.models.metadataentry import MetadataEntry
from metaforge.models.metadatamodel import MetadataModel


class QEzTableModel(QAbstractTableModel):
    """
    Define all of the column indices and column names in addition to any other strings
    in this section. This will make it easier to move columns around and rename items.
    """

    # Row colors
    K_RED_BG_COLOR = QColor(255, 190, 194)
    K_YELLOW_BG_COLOR = QColor(253, 255, 190)

    # Mime Type
    K_METADATAENTRY_MIMETYPE = "application/metadataentry"

    # Total Number of Columns
    K_COL_COUNT = 10

    # These are some misc strings that are used.
    K_FROM_SOURCE = "--SOURCE--"
    K_NOT_LOADED = "--NOT LOADED--"
    K_CUSTOM_VALUE = "--CUSTOM VALUE--"

    # These are the user facing header and the index of each column in the table.
    K_SORT_COL_NAME = "#"
    K_SORT_COL_INDEX = 0

    K_SOURCE_COL_NAME = "Source"
    K_SOURCE_COL_INDEX = 1

    K_SOURCEVAL_COL_NAME = "Source Value"
    K_SOURCEVAL_COL_INDEX = 2

    K_HTNAME_COL_NAME = "HT Name"
    K_HTNAME_COL_INDEX = 3

    K_HTVALUE_COL_NAME = "HT Value"
    K_HTVALUE_COL_INDEX = 4

    K_HTANNOTATION_COL_NAME = "HT Annotation"
    K_HTANNOTATION_COL_INDEX = 6

    K_HTUNITS_COL_NAME = "HT Units"
    K_HTUNITS_COL_INDEX = 5

    K_USESOURCE_COL_NAME = "Override Source Value"
    K_OVERRIDESOURCEVALUE_COL_INDEX = 7

    K_EDITABLE_COL_NAME = "Editable"
    K_EDITABLE_COL_INDEX = 8

    K_REMOVE_COL_NAME = "Remove"
    K_REMOVE_COL_INDEX = 9

    def __init__(self, metadata_model: MetadataModel, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.metadata_model = metadata_model


    def rowCount(self, parent=QModelIndex()):
        model_row_count = self.metadata_model.size()
        return model_row_count
    
    def columnCount(self, parent=QModelIndex()):
        return self.K_COL_COUNT
    
    def data(self, index, role):
        if not index.isValid():
            return None

        metadata_entry: MetadataEntry = self.metadata_model.entry(index.row())

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() == self.K_SORT_COL_INDEX:
                return index.row() + 1
            elif index.column() == self.K_HTNAME_COL_INDEX:
                return metadata_entry.ht_name
            elif index.column() == self.K_SOURCEVAL_COL_INDEX:
                if metadata_entry.source_type is MetadataEntry.SourceType.FILE:
                    if metadata_entry.loaded is True:
                        return str(metadata_entry.source_value)
                    else:
                        return self.K_NOT_LOADED
                else:
                    return str(self.K_CUSTOM_VALUE)
            elif index.column() == self.K_SOURCE_COL_INDEX:
                if metadata_entry.source_type is MetadataEntry.SourceType.CUSTOM:
                    return self.K_CUSTOM_VALUE
                else:
                    return metadata_entry.source_path
            elif index.column() == self.K_HTVALUE_COL_INDEX:
                if metadata_entry.source_type is MetadataEntry.SourceType.CUSTOM:
                    return str(metadata_entry.ht_value)
                else:
                    if metadata_entry.override_source_value is True:
                        return str(metadata_entry.ht_value)
                    else:
                        return str(self.K_FROM_SOURCE)
            elif index.column() == self.K_HTANNOTATION_COL_INDEX:
                return metadata_entry.ht_annotation
            elif index.column() == self.K_HTUNITS_COL_INDEX:
                return metadata_entry.ht_units
        elif role == Qt.ToolTipRole:
            if index.column() == self.K_SORT_COL_INDEX:
                return "The row number of the metadata item.  This number is editable, and the row will move once the row number has been changed."
            elif index.column() == self.K_HTNAME_COL_INDEX:
                return "This cell contains the name of the metadata item."
            elif index.column() == self.K_SOURCEVAL_COL_INDEX:
                return "This cell contains the metadata value that is extracted from the Data File above.  This is the default value for 'HT Value' when the 'Override Source Value' checkbox is checked."
            elif index.column() == self.K_SOURCE_COL_INDEX:
                return "This cell contains the path to the metadata item's location in the Data File.  The template, once created, will use this path to extract the metadata value from other similar data files."
            elif index.column() == self.K_HTVALUE_COL_INDEX:
                return "This cell contains a placeholder for the metadata value that will be extracted from other similar data files when someone uses the template.  If the 'Override Source Value' checkbox is checked, then this cell will contain a static, editable value (defaults to the 'Source Value' value)."
            elif index.column() == self.K_HTANNOTATION_COL_INDEX:
                return "This cell contains the annotations that are included with this metadata item.  This information will be automatically filled in for this metadata item when someone uses the template."
            elif index.column() == self.K_HTUNITS_COL_INDEX:
                return "This cell contains the units that describe this metadata item.  This information will be automatically filled in for this metadata item when someone uses the template."
            elif index.column() == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
                return "This cell contains a checkbox that will override the value extracted from similar data files when the template is used. If this checkbox is checked, the 'HT Value' field will contain a static, editable value (defaults to the 'Source Value' value)."
            elif index.column() == self.K_EDITABLE_COL_INDEX:
                return "This cell contains a checkbox that determines whether or not users of the template are allowed to modify the cells of this metadata item."
            elif index.column() == self.K_REMOVE_COL_INDEX:
                return "This cell removes the metadata item from the table."
        elif role == Qt.CheckStateRole:
            if index.column() == self.K_EDITABLE_COL_INDEX:
                if metadata_entry.editable is True:
                    return Qt.Checked
                else:
                    return Qt.Unchecked
            elif index.column() == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
                if metadata_entry.source_type is MetadataEntry.SourceType.FILE:
                    if metadata_entry.override_source_value is True:
                        return Qt.Checked
                    else:
                        return Qt.Unchecked
        elif role == Qt.FontRole:
            flags = self.flags(index)
            if not (flags & Qt.ItemIsEditable):
                italic_font = QFont()
                italic_font.setItalic(True)
                return italic_font


        return None
    
    def setData(self, index, value, role):
        if not index.isValid():
            return False
        
        if self.metadata_model is None:
            return False
        
        metadata_entry: MetadataEntry = self.metadata_model.entry(index.row())
            
        if role == Qt.EditRole:
            if index.column() == self.K_SORT_COL_INDEX:
                if value < 1 or value > self.rowCount():
                    return False
                
                mime_data = self.mimeData([index])
                return self.dropMimeData(mime_data, Qt.MoveAction, value, 0, QModelIndex())
                
                # result = self.metadata_model.remove_by_index(index.row())
                # if not result:
                #     return False
                
                # self.metadata_model.insert(metadata_entry, value - 1)
                # return True
            elif index.column() == self.K_HTNAME_COL_INDEX:
                metadata_entry.ht_name = value
                self.dataChanged.emit(index, index)
                return True
            elif index.column() == self.K_HTVALUE_COL_INDEX:
                if metadata_entry.source_type == MetadataEntry.SourceType.CUSTOM or metadata_entry.override_source_value is True:
                    metadata_entry.ht_value = value
                    self.dataChanged.emit(index, index)
                    return True
            elif index.column() == self.K_HTANNOTATION_COL_INDEX:
                metadata_entry.ht_annotation = value
                self.dataChanged.emit(index, index)
                return True
            elif index.column() == self.K_HTUNITS_COL_INDEX:
                metadata_entry.ht_units = value
                self.dataChanged.emit(index, index)
                return True
        elif role == Qt.CheckStateRole:
            if index.column() == self.K_EDITABLE_COL_INDEX:
                if value == Qt.Checked:
                    metadata_entry.editable = True
                else:
                    metadata_entry.editable = False
                self.dataChanged.emit(index, index)
                return True
            elif index.column() == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
                if value == Qt.Checked:
                    metadata_entry.override_source_value = True
                else:
                    metadata_entry.override_source_value = False
                value_index = self.index(index.row(), self.K_HTVALUE_COL_INDEX)
                self.dataChanged.emit(index, index)
                self.dataChanged.emit(value_index, value_index)
                return True

        return False

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            if section == self.K_SORT_COL_INDEX:
                return self.K_SORT_COL_NAME
            elif section == self.K_HTNAME_COL_INDEX:
                return self.K_HTNAME_COL_NAME
            elif section == self.K_SOURCEVAL_COL_INDEX:
                return self.K_SOURCEVAL_COL_NAME
            elif section == self.K_SOURCE_COL_INDEX:
                return self.K_SOURCE_COL_NAME
            elif section == self.K_HTVALUE_COL_INDEX:
                return self.K_HTVALUE_COL_NAME
            elif section == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
                return self.K_USESOURCE_COL_NAME
            elif section == self.K_EDITABLE_COL_INDEX:
                return self.K_EDITABLE_COL_NAME
            elif section == self.K_HTANNOTATION_COL_INDEX:
                return self.K_HTANNOTATION_COL_NAME
            elif section == self.K_HTUNITS_COL_INDEX:
                return self.K_HTUNITS_COL_NAME
            elif section == self.K_REMOVE_COL_INDEX:
                return self.K_REMOVE_COL_NAME
            return None
        if orientation == Qt.Vertical:
            return "    "
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsDropEnabled

        metadata_entry: MetadataEntry = self.metadata_model.entry(index.row())

        if index.column() == self.K_SORT_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled
        elif index.column() == self.K_SOURCE_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
        elif index.column() == self.K_SOURCEVAL_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
        elif index.column() == self.K_HTNAME_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled
        elif index.column() == self.K_HTVALUE_COL_INDEX:
            if metadata_entry.source_type == MetadataEntry.SourceType.CUSTOM:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled
            else:
                if metadata_entry.override_source_value is True:
                    return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled
                else:
                    return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
        elif index.column() == self.K_HTANNOTATION_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled
        elif index.column() == self.K_HTUNITS_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled
        elif index.column() == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
            if metadata_entry.source_type is MetadataEntry.SourceType.FILE:
                return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
            elif metadata_entry.source_type is MetadataEntry.SourceType.CUSTOM:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
            else:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
        elif index.column() == self.K_EDITABLE_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled
        elif index.column() == self.K_REMOVE_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled

    def canDropMimeData(self, data: QMimeData, action: Qt.DropAction, row: int, column: int, parent: QModelIndex) -> bool:
        if not data.hasFormat(self.K_METADATAENTRY_MIMETYPE):
            return False

        if action != Qt.MoveAction:
            return False

        return True
    
    def mimeTypes(self):
        return [self.K_METADATAENTRY_MIMETYPE]

    def mimeData(self, idxs: List[QModelIndex]):
        mime_data = QMimeData()
        encoded_data = QByteArray()
        stream = QDataStream(encoded_data, QIODevice.WriteOnly)

        metadata_entries: List[MetadataEntry] = []
        rows: List[int] = []
        for idx in idxs:
            if idx.isValid():
                metadata_entry: MetadataEntry = self.metadata_model.entry(idx.row())
                if metadata_entry not in metadata_entries:
                    metadata_entries.append(metadata_entry)
                    rows.append(idx)

        metadata_dict = [metadata_entry.to_dict() for metadata_entry in metadata_entries]
        stream.writeQString(json.dumps(metadata_dict))
        mime_data.setData(self.K_METADATAENTRY_MIMETYPE, encoded_data)

        return mime_data

    def dropMimeData(self, data, action, row, column, parent):
        encoded_data = data.data(self.K_METADATAENTRY_MIMETYPE)
        stream = QDataStream(encoded_data, QIODevice.ReadOnly)
        json_string = stream.readQString()
        metadata_dict = json.loads(json_string)
        metadata_entries: List[MetadataEntry] = [MetadataEntry.from_dict(mc_dict) for mc_dict in metadata_dict]

        row_index = QPersistentModelIndex(self.index(row, 0))

        if action == Qt.MoveAction:
            for metadata_entry in metadata_entries:
                source_row = self.metadata_model.index_from_source(metadata_entry.source_path)
                self.beginRemoveRows(QModelIndex(), source_row, source_row)
                self.metadata_model.remove_by_index(source_row)
                self.endRemoveRows()

        self.beginInsertRows(QModelIndex(), row_index.row(), row_index.row() + len(metadata_entries) - 1)
        for i, metadata_entry in enumerate(metadata_entries):
            self.metadata_model.insert(metadata_entry, row_index.row() + i)
        self.endInsertRows()
        return True

    def supportedDropActions(self):
        return Qt.MoveAction
    
    def addCustomRow(self, numCustom):
        self.beginInsertRows(self.index(len(self.metadata_model.entries), 0), len(
            self.metadata_model.entries), len(self.metadata_model.entries))
        custom = MetadataEntry()
        custom.source_type =  MetadataEntry.SourceType.CUSTOM
        custom.source_path  = ""
        custom.source_value  = ""
        custom.ht_name  = "Custom HT Name"
        custom.ht_value  = "Custom HT Value"
        custom.ht_annotation  = ""
        custom.ht_units  = ""
        custom.override_source_value  = False
        custom.editable  = True
        custom.required  = True
        custom.enabled  = True

        self.metadata_model.append(custom)

        self.endInsertRows()
    
    def refresh_entry(self, source):
        metadata_entry: MetadataEntry = self.metadata_model.entry_by_source(source)
        if metadata_entry is not None:
            row = self.metadata_model.index_from_source(source)
            left_index = self.index(row, 0)
            right_index = self.index(row, self.columnCount() - 1)
            self.dataChanged.emit(left_index, right_index)

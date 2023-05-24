from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex, QFileSystemWatcher, QPersistentModelIndex, Signal
from PySide2.QtGui import QColor, QIcon, QPixmap

from pathlib import Path

from metaforge.models.parsermodelitem import ParserModelItem
from metaforge.models.parsermodel import ParserModel
from metaforge.parsers.metaforgeparser import MetaForgeParser

class QParserTableModel(QAbstractTableModel):
    model_about_to_change = Signal()
    model_changed = Signal()

    Parser = Qt.UserRole + 1
    ParserPath = Qt.UserRole + 2
    Default = Qt.UserRole + 3
    Enabled = Qt.UserRole + 4

    """
    Define all of the column indices and column names in addition to any other strings
    in this section. This will make it easier to move columns around and rename items.
    """

    # Row colors
    K_RED_BG_COLOR = QColor(255, 190, 194)
    K_YELLOW_BG_COLOR = QColor(253, 255, 190)

    # These are the user facing header and the index of each column in the table.
    K_ENABLED_COL_NAME = "Enabled"
    K_ENABLED_COL_INDEX = 0

    K_PARSER_NAME_COL_NAME = "Parser Name"
    K_PARSER_NAME_COL_INDEX = 1

    K_PARSER_LOCATION_COL_NAME = "Parser Location"
    K_PARSER_LOCATION_COL_INDEX = 2

    K_PARSER_SUPPORTED_EXTS_COL_NAME = "Supported File Extensions"
    K_PARSER_SUPPORTED_EXTS_COL_INDEX = 3

    K_PARSER_VERSION_COL_NAME = "Parser Version"
    K_PARSER_VERSION_COL_INDEX = 4

    K_PARSER_MESSAGES_COL_NAME = "Messages"
    K_PARSER_MESSAGES_COL_INDEX = 5

    # Total Number of Columns
    K_COL_COUNT = K_PARSER_MESSAGES_COL_INDEX + 1

    def __init__(self, ez_parser_model: ParserModel, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._ez_parser_model: ParserModel = ez_parser_model
        self._parser_watcher = QFileSystemWatcher(self)

        self._init_file_watcher()
    
    def _init_file_watcher(self):
        self._parser_watcher.fileChanged.connect(self._update_parser)
        [self._parser_watcher.addPath(str(ez_parser.parser_path)) for ez_parser in self._ez_parser_model.parser_metadata_list]

    def rowCount(self, parent=QModelIndex()):
        return self._ez_parser_model.size()
    
    def columnCount(self, parent=QModelIndex()):
        return self.K_COL_COUNT
    
    def data(self, index, role):
        if not index.isValid():
            return None

        parser: MetaForgeParser = self._ez_parser_model.parser(index.row())

        if role == Qt.DisplayRole or role == Qt.EditRole or role == Qt.ToolTipRole:
            if index.column() == self.K_PARSER_NAME_COL_INDEX:
                if parser is None:
                    return '[PARSER_LOAD_ERROR]'
                return parser.human_label()
            elif index.column() == self.K_PARSER_LOCATION_COL_INDEX:
                return str(self._ez_parser_model.parser_path(index.row()))
            elif index.column() == self.K_PARSER_SUPPORTED_EXTS_COL_INDEX:
                if parser is None:
                    return ''
                
                exts = parser.supported_file_extensions()
                if len(exts) == 1:
                    return exts[0]
                else:
                    return ', '.join(exts)
            elif index.column() == self.K_PARSER_VERSION_COL_INDEX:
                if parser is None:
                    return ''
                return parser.version()
            elif index.column() == self.K_PARSER_MESSAGES_COL_INDEX:
                return self._ez_parser_model.message(index.row())
        elif role == Qt.BackgroundRole and parser is None:
            return self.K_RED_BG_COLOR
        elif role == Qt.DecorationRole and self._ez_parser_model.is_default(index.row()) and index.column() == self.K_PARSER_NAME_COL_INDEX:
            return QIcon(QPixmap(':/resources/Images/star@2x.png'))
        elif role == Qt.CheckStateRole and index.column() == self.K_ENABLED_COL_INDEX:
            return Qt.Checked if self._ez_parser_model.is_enabled(index.row()) == True else Qt.Unchecked
        elif role == self.Parser:
            return parser
        elif role == self.ParserPath:
            return self._ez_parser_model.parser_path(index.row())
        elif role == self.Default:
            return self._ez_parser_model.is_default(index.row())
        elif role == self.Enabled:
            return self._ez_parser_model.is_enabled(index.row())

        return None

    def setData(self, index, value, role):
        if index.isValid():
            if role == Qt.CheckStateRole and index.column() == self.K_ENABLED_COL_INDEX:
                self._ez_parser_model.set_enabled(index.row(), (value == Qt.Checked))
                self.dataChanged.emit(index, index, [role])
                return True
        
        return False

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        
        if orientation == Qt.Horizontal:
            if section == self.K_ENABLED_COL_INDEX:
                return self.K_ENABLED_COL_NAME
            elif section == self.K_PARSER_NAME_COL_INDEX:
                return self.K_PARSER_NAME_COL_NAME
            elif section == self.K_PARSER_LOCATION_COL_INDEX:
                return self.K_PARSER_LOCATION_COL_NAME
            elif section == self.K_PARSER_SUPPORTED_EXTS_COL_INDEX:
                return self.K_PARSER_SUPPORTED_EXTS_COL_NAME
            elif section == self.K_PARSER_VERSION_COL_INDEX:
                return self.K_PARSER_VERSION_COL_NAME
            elif section == self.K_PARSER_MESSAGES_COL_INDEX:
                return self.K_PARSER_MESSAGES_COL_NAME
        
        return None
    
    def removeRows(self, row: int, count: int, parent: QModelIndex):
        self.beginRemoveRows(parent, row, row + count - 1)
        persistent_indexes = [QPersistentModelIndex(self.index(idx, 0, parent)) for idx in range(row, row + count)]
        for persistent_index in persistent_indexes:
            parser_path = self._ez_parser_model.parser_path(persistent_index.row())
            self._parser_watcher.removePath(str(parser_path))
            self._ez_parser_model.remove_by_index(persistent_index.row())
        self.endRemoveRows()
        return True
    
    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        if index.column() == self.K_ENABLED_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
    def append(self, parser_item: ParserModelItem):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._ez_parser_model.append(parser_item)
        self._parser_watcher.addPath(str(parser_item.parser_path))
        self.endInsertRows()
    
    def insert(self, index: int, parser_item: ParserModelItem):
        self.beginInsertRows(QModelIndex(), index, index)
        self._ez_parser_model.insert(index, parser_item)
        self._parser_watcher.addPath(str(parser_item.parser_path))
        self.endInsertRows()

    def _update_parser(self, parser_file_path: str):
        self._reload_parser(Path(parser_file_path))
        self.model_about_to_change.emit()
        self.model_changed.emit()

    def _reload_parser(self, parser_file_path: Path):
        index = self._ez_parser_model.index_from_parser_path(parser_file_path)
        self._ez_parser_model.reload_parser(index)

        top_left = self.index(index, self.K_PARSER_NAME_COL_INDEX)
        bottom_right = self.index(index, self.K_PARSER_MESSAGES_COL_INDEX)
        self.dataChanged.emit(top_left, bottom_right)


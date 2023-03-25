# This Python file uses the following encoding: utf-8
from PySide2.QtCore import *
from PySide2.QtWidgets import QStyle, QStyledItemDelegate, QStyleOptionViewItem
import PySide2.QtCore
from PySide2.QtCore import Qt, QEvent

qt_version = PySide2.QtCore.__version_info__

if qt_version[1] == 12:
    from metaforge.widgets.generated_5_12.resources_rc import *
elif qt_version[1] == 15:
    from metaforge.widgets.generated_5_15.resources_rc import *


class CheckBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        opt = option
        widget = option.widget
        super().initStyleOption(opt, index)
        style = opt.widget.style()
        style.drawPrimitive(QStyle.PE_PanelItemViewItem, opt, painter, widget)
        if opt.features & QStyleOptionViewItem.HasCheckIndicator:
            if opt.checkState is Qt.Unchecked:
                opt.state |= QStyle.State_Off
            elif opt.checkState is Qt.PartiallyChecked:
                opt.state |= QStyle.State_NoChange
            else:
                opt.state |= QStyle.State_On
            
            rect = style.subElementRect(QStyle.SE_ItemViewItemCheckIndicator, opt, widget)
            opt.rect = QStyle.alignedRect(opt.direction, Qt.AlignCenter, rect.size(), opt.rect)
            opt.state = opt.state & ~QStyle.State_HasFocus
            style.drawPrimitive(QStyle.PE_IndicatorItemViewItemCheck, opt, painter, widget)
        else:
            QStyledItemDelegate.paint(self, painter, option, index)

    def editorEvent(self, event, model, option, index):
        # Make sure that the item is checkable
        flags = model.flags(index)
        if not (flags & Qt.ItemIsUserCheckable) or not (option.state & QStyle.State_Enabled) or not (flags & Qt.ItemIsEnabled):
            return False

        value = Qt.CheckState(index.data(Qt.CheckStateRole))
        style = option.widget.style()

        # Make sure that we have the right event type
        event_type = event.type()
        if event_type is QEvent.MouseButtonRelease or event_type is QEvent.MouseButtonDblClick or event_type is QEvent.MouseButtonPress:
            viewOpt = QStyleOptionViewItem(option)
            super().initStyleOption(viewOpt, index)
            checkRect = style.subElementRect(QStyle.SE_ItemViewItemCheckIndicator, viewOpt, option.widget)
            checkRect = QStyle.alignedRect(viewOpt.direction, Qt.AlignCenter, checkRect.size(), viewOpt.rect)
            if event.button() is not Qt.LeftButton or not checkRect.contains(event.pos()):
                return False
            if event_type is QEvent.MouseButtonPress or event_type is QEvent.MouseButtonDblClick:
                return True
        elif event_type is QEvent.KeyPress:
            if event.key() is not Qt.Key_Space and event.key() is not Qt.Key_Select:
                return False
        else:
            return False

        if value == Qt.Checked:
            value = Qt.Unchecked
        else:
            value = Qt.Checked

        return model.setData(index, value, Qt.CheckStateRole)



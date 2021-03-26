from PySide2.QtCore import QSortFilterProxyModel, Qt, QRegExp

class FilterModel(QSortFilterProxyModel):
    def __init__(self,data ,parent=None):
        QSortFilterProxyModel.__init__(self, parent)
        self.displayed=[]




    def filterAcceptsRow(self,source_row, source_parent):
        return self.sourceModel().metadataList[source_row] not in self.sourceModel().hiddenList

    def checkList(self,checked,source):
        sourcelist= source.split("/")
        sourceDict=self.sourceModel().treeDict
        i=0
        key=""
        while i != len(sourcelist):
            key=sourcelist[i]
            sourceDict=sourceDict[key]
            i+=1
        if checked == Qt.Unchecked:
            for j in range(len(self.sourceModel().metadataList)):
                if self.sourceModel().metadataList[j]["Source"] == source:
                    self.sourceModel().hiddenList.append(self.sourceModel().metadataList[j])
                    break
        else:
            for j in range(len(self.sourceModel().hiddenList)):
                if self.sourceModel().hiddenList[j]["Source"] == source:
                    row = self.sourceModel().hiddenList[j]
                    del self.sourceModel().hiddenList[j]
                    break

        self.setFilterRegExp(QRegExp())

        #self.dataChanged.emit(1, 0)
        #self.invalidate()

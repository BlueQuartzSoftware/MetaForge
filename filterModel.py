from PySide2.QtCore import QSortFilterProxyModel, Qt, QRegExp

class FilterModel(QSortFilterProxyModel):
    def __init__(self,data ,parent=None):
        QSortFilterProxyModel.__init__(self, parent)
        self.displayed=[]
        self.fileList=[]


    def filterAcceptsRow(self,source_row, source_parent):
        if self.sourceModel().metadataList[source_row] not in self.sourceModel().hiddenList and self.sourceModel().metadataList[source_row] not in self.displayed:
            self.displayed.append(self.sourceModel().metadataList[source_row])
        elif self.sourceModel().metadataList[source_row]["Source"] == "Custom Input" and self.sourceModel().metadataList[source_row] not in self.displayed:
            self.displayed.append(self.sourceModel().metadataList[source_row])
        return self.sourceModel().metadataList[source_row] not in self.sourceModel().hiddenList or self.sourceModel().metadataList[source_row] == "Custom Input"

    def checkList(self,checked,source):
        if source == "Custom Input":
            self.setFilterRegExp(QRegExp())
        else:
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
                    if source in self.sourceModel().metadataList[j]["Source"]:
                        self.sourceModel().hiddenList.append(self.sourceModel().metadataList[j])
                    iteratelist = self.displayed[:]
                    newj = 0
                    for j in range(len(iteratelist)):
                        if source in iteratelist[j]["Source"]:
                            del self.displayed[j-newj]
                            newj+=1

            else:
                iteratelist = self.sourceModel().hiddenList[:]
                newj=0
                for j in range(len(iteratelist)):
                    if source in iteratelist[j]["Source"]:
                        del self.sourceModel().hiddenList[j-newj]
                        newj+=1

            self.setFilterRegExp(QRegExp())

from PySide2.QtCore import QFileInfo, QObject, Signal
from ht_requests.ht_requests import ht_utilities
from ht_requests.ht_requests import htauthcontroller
from ht_requests.ht_requests import ht_requests
from tqdm import tqdm


class Uploader(QObject):
    currentUploadDone = Signal(int)
    allUploadsDone = Signal()
    currentlyUploading = Signal(str)

    def __init__(self, parent=None):
        super(Uploader, self).__init__(parent)
        self.interrupt = False

    def performUpload(self, metadataList, authControl, ht_id_path, metadata):
        self.interrupt = False

        # Check that all files initially exist. This is a quick sanity check. The user could
        # *still* delete a file out from under the codes.
        for i in tqdm(range(len(metadataList)), desc="Checking Files"):
            if not QFileInfo.exists(metadataList[i]):
                self.currentlyUploading.emit(
                    "File Missing: " + metadataList[i].split("/")[-1])
                self.interrupt = True

        for i in tqdm(range(len(metadataList)), desc="Uploading Files"):
            if self.interrupt:
                break

            if not QFileInfo.exists(metadataList[i]):
                self.currentlyUploading.emit(
                    "File Missing: " + metadataList[i].split("/")[-1])
                break
            else:
                self.currentlyUploading.emit(
                    "Currently uploading: " + metadataList[i].split("/")[-1])
                ht_requests.upload_file(
                    authControl, metadataList[i], 'user', None, ht_id_path, metadata)
                self.currentUploadDone.emit(i+1)
        self.allUploadsDone.emit()

    def interruptUpload(self):
        self.interrupt = True

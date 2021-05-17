from PySide2.QtCore import QObject, Signal
from ht_requests.ht_requests import ht_utilities
from ht_requests.ht_requests import htauthcontroller
from ht_requests.ht_requests import ht_requests
from tqdm import tqdm


class Uploader(QObject):
    currentUploadDone = Signal(int)
    allUploadsDone = Signal()
    def __init__(self, parent = None):
        super(Uploader, self).__init__(parent)




    def performUpload(self,metadataList ,authControl, ht_id_path, metadata):

        for i in tqdm(range(len(metadataList)), desc= "Uploading Files"):
            print("started uploading")
            ht_requests.upload_file(authControl, metadataList[i], 'user', None, ht_id_path, metadata)
            print("finished uploading")
            self.currentUploadDone.emit(i+1)
        self.allUploadsDone.emit()



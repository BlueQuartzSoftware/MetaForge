from PySide2.QtCore import QObject, Signal
from ht_requests.ht_requests import ht_requests
from tqdm import tqdm
from pathlib import Path
from typing import List


class Uploader(QObject):
    notifyProgress = Signal(int)
    allUploadsDone = Signal()
    currentlyUploading = Signal(str)

    def __init__(self, parent=None):
        super(Uploader, self).__init__(parent)
        self.interrupt = False

    def performUpload(self, filelist: List[Path], authControl, workspace_id, ht_id_path, metadata):
        self.interrupt = False

        print(filelist)

        # Check that all files initially exist. This is a quick sanity check. The user could
        # *still* delete a file out from under the codes.
        for i in tqdm(range(len(filelist)), desc="Checking Files"):
            if not filelist[i].exists():
                self.currentlyUploading.emit(f"File Missing: {filelist[i].name}")
                self.interrupt = True

        for i in tqdm(range(len(filelist)), desc="Uploading Files"):
            if self.interrupt:
                break

            if not filelist[i].exists():
                self.currentlyUploading.emit(f"File Missing: {filelist[i].name}")
                break
            else:
                ht_requests.upload_file(auth_control=authControl, 
                                        local_path=str(filelist[i]),
                                        workspace_id=workspace_id,
                                        ht_id_path=ht_id_path, 
                                        metadata=metadata,
                                        msg_delegate=self.currentlyUploading.emit)
                files_finished = float(i+1)
                total_files = float(len(filelist))
                current_progress = int((files_finished/total_files) * 100)
                self.notifyProgress.emit(current_progress)
        self.allUploadsDone.emit()

    def interruptUpload(self):
        self.interrupt = True

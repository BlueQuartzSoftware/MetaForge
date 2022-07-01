from PySide2.QtCore import QObject, Signal
from pathlib import Path
from typing import List
import hyperthought as ht
import os


class Uploader(QObject):
    notify_file_progress = Signal(int)
    notify_file_progress_text = Signal(str)
    notify_list_progress = Signal(int)
    notify_list_progress_text = Signal(str)
    all_uploads_done = Signal()

    def __init__(self, parent=None):
        super(Uploader, self).__init__(parent)
        self.interrupt = False
        self.total_bytes = 0.0
        self.bytes_uploaded = 0.0
        self.current_chunk_size = 0

    def performUpload(self, filelist: List[Path], authControl: ht.auth.Authorization, workspace_id, ht_id_path, metadata):
        self.interrupt = False
        files_api = ht.api.files.FilesAPI(auth=authControl)

        self.total_bytes = 0.0
        for file in filelist:
            self.total_bytes = self.total_bytes + os.path.getsize(str(file))

        total_file_count = len(filelist)
        self.bytes_uploaded = 0.0
        successful_uploads = 0
        n_chunks = 100
        for i in range(len(filelist)):
            if self.interrupt:
                list_progress_text = f"{successful_uploads}/{total_file_count} Files Uploaded - Upload Canceled"
                break

            if not filelist[i].exists():
                list_progress_text = f"{successful_uploads}/{total_file_count} Files Uploaded - File Missing: {filelist[i].name}"
                break
            else:
                self.notify_file_progress_text.emit(f"Uploading File - {str(filelist[i].name)}")
                self.notify_list_progress_text.emit(f"Uploading Files - {i+1}/{total_file_count}")
                self.current_chunk_size = float(os.path.getsize(str(filelist[i]))) / n_chunks
                file_id, file_name = files_api.upload(local_path=str(filelist[i]),
                                                      space_id=workspace_id,
                                                      path=ht_id_path,
                                                      metadata=metadata,
                                                      progress_callback=self.file_progress,
                                                      n_chunks=n_chunks)
                successful_uploads = successful_uploads + 1
                list_progress_text = f"{successful_uploads}/{total_file_count} Files Uploaded!"
                
        self.notify_file_progress.emit(0)
        self.notify_file_progress_text.emit("")
        self.notify_list_progress.emit(0)
        self.notify_list_progress_text.emit(list_progress_text)
        self.all_uploads_done.emit()
    
    def file_progress(self, value: int):
        self.notify_file_progress.emit(value)

        self.bytes_uploaded = self.bytes_uploaded + self.current_chunk_size
        list_progress = int((float(self.bytes_uploaded)/float(self.total_bytes)) * 100)
        if list_progress <= 100:
            self.notify_list_progress.emit(list_progress)

    def interruptUpload(self):
        self.interrupt = True

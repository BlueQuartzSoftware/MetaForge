from PySide6.QtCore import QObject, Signal
from pathlib import Path
from typing import List
import hyperthought as ht
import os


class HyperThoughtUploader(QObject):
    notify_file_progress = Signal(int)
    notify_file_progress_text = Signal(str)
    notify_list_progress = Signal(int)
    notify_list_progress_text = Signal(str)
    all_uploads_done = Signal()

    def __init__(self, parent=None):
        super(HyperThoughtUploader, self).__init__(parent)
        self.interrupt = False
        self.total_bytes = 0.0
        self.bytes_uploaded = 0.0
        self.current_chunk_size = 0
        self.uploading = False
    
    def is_uploading(self) -> bool:
        return self.uploading

    def performUpload(self, upload_list: List[Path], authControl: ht.auth.Authorization, workspace_id, ht_id_path, metadata):
        self.interrupt = False
        self.uploading = True
        files_api = ht.api.files.FilesAPI(auth=authControl)

        self.total_bytes = 0.0
        total_file_count = 0
        for upload_obj in upload_list:
            if os.path.isdir(str(upload_obj)):
                for root, dirs, files in os.walk(str(upload_obj)):
                    files = [f for f in files if not f[0] == '.']
                    total_file_count += len(files)
                    for file in files:
                        self.total_bytes = self.total_bytes + os.path.getsize(str(Path(root) / Path(file)))
            else:
                total_file_count += 1
                self.total_bytes = self.total_bytes + os.path.getsize(str(upload_obj))

        self.bytes_uploaded = 0.0
        self.files_uploaded = 0
        n_chunks = 100
        for upload_obj in upload_list:
            if self.interrupt:
                self._finish_upload(f"{self.files_uploaded}/{total_file_count} Files Uploaded - Upload Canceled")
                return

            if not upload_obj.exists():
                self._finish_upload(f"{self.files_uploaded}/{total_file_count} Files Uploaded - File Missing: {upload_obj}")
                return

            if os.path.isdir(str(upload_obj)):
                for root, dirs, files in os.walk(str(upload_obj)):
                    files = [f for f in files if not f[0] == '.']

                    if str(upload_obj) == root:
                        parent_id_path = ht_id_path
                    else:
                        root_parent = Path(root).parent
                        parent_folder_path = str(root_parent).replace(str(upload_obj.parent), '')
                        parent_id_path = files_api.get_id_path(path=parent_folder_path, space_id=workspace_id)
                    new_folder_id = files_api.create_folder(name=Path(root).name, space_id=workspace_id, path=parent_id_path)
                    new_folder_id_path = parent_id_path + new_folder_id + ','
                    for file in files:
                        if self.interrupt:
                            self._finish_upload(f"{self.files_uploaded}/{total_file_count} Files Uploaded - Upload Canceled")
                            return

                        file_path = Path(root) / Path(file)
                        ht_file_path = Path(root.replace(str(upload_obj.parent), '')) / Path(file)
                        self.notify_file_progress_text.emit(f"Uploading Folder '{upload_obj.name}' - {str(ht_file_path)}")
                        self._upload_file(file_path, files_api, workspace_id, new_folder_id_path, metadata, n_chunks, total_file_count)

            else:
                self.notify_file_progress_text.emit(f"Uploading File - {upload_obj.name}")
                self._upload_file(upload_obj, files_api, workspace_id, ht_id_path, metadata, n_chunks, total_file_count)

        self._finish_upload(f"{self.files_uploaded}/{total_file_count} Files Uploaded!")
    
    def _upload_file(self, file_path: Path, files_api: ht.api.files.FilesAPI, workspace_id, ht_id_path, metadata, n_chunks, total_file_count):
        self.current_chunk_size = float(os.path.getsize(str(file_path))) / n_chunks
        self.notify_list_progress_text.emit(f"Uploading Files - {self.files_uploaded+1}/{total_file_count}")
        self.notify_file_progress.emit(0)
        file_id, file_name = files_api.upload(local_path=str(file_path),
                                                space_id=workspace_id,
                                                path=ht_id_path,
                                                metadata=metadata,
                                                progress_callback=self.file_progress,
                                                n_chunks=n_chunks)
        self.files_uploaded += 1
    
    def file_progress(self, value: int):
        self.notify_file_progress.emit(value)

        self.bytes_uploaded = self.bytes_uploaded + self.current_chunk_size
        list_progress = int((float(self.bytes_uploaded)/float(self.total_bytes)) * 100)
        if list_progress <= 100:
            self.notify_list_progress.emit(list_progress)

    def interruptUpload(self):
        self.interrupt = True
    
    def _finish_upload(self, msg):
        self.notify_file_progress.emit(0)
        self.notify_file_progress_text.emit("")
        self.notify_list_progress.emit(0)
        self.notify_list_progress_text.emit(msg)
        self.all_uploads_done.emit()
        self.uploading = False

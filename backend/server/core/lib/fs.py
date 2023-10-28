import os
import uuid
import mimetypes
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile

def create_file(file: UploadedFile, filename: str, path: str):
    fs = FileSystemStorage(location=path)
        
    fs.save(filename, file)
    
    return filename

def delete_file(file_path):
    fs = FileSystemStorage()

    if fs.exists(file_path):
        fs.delete(file_path)
    else:
        raise Exception('File does not exist')

def format_file(file: UploadedFile, path: str) -> UploadedFile:
    if not isinstance(file, UploadedFile):
        raise Exception('File is not an instance of UploadedFile')
    fs = FileSystemStorage(location=path)
    filename = f'{fs.get_available_name(uuid.uuid4().hex)}.{mimetypes.guess_extension(file.content_type)}'
    file.name = filename
    return file
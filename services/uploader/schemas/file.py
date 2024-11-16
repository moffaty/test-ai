import os
import mimetypes
import ntpath
from dotenv import load_dotenv
from utils.file.file_types import FileTypes


class FileError(Exception):
    class FileSizeError(Exception):
        """Исключение для файлов, которые превышают допустимый размер."""

        pass

    class FileTypeError(Exception):
        """Исключение для файлов, которые не подходят под допустимый тип."""

        pass


class File:
    def __init__(self, path) -> None:
        load_dotenv()

        self.path = path
        self.filename = self.get_file_name(self.path)

        try:
            self.max_size = int(os.getenv("MAX_FILE_SIZE", 0))
        except ValueError:
            raise ValueError("MAX_FILE_SIZE in configuration might be an int.")

        self.size = self.get_file_size(path)

        if self.size > self.max_size:
            raise FileError.FileSizeError(
                f"File size {self.size} bytes exceeds the maximum allowed size of {self.max_size} bytes."
            )

        try:
            self.type, self.mime = self.get_file_type_from_enum(path)
        except TypeError:
            raise FileError.FileTypeError(
                f"File type is not allowed. Please use a valid file type."
            )

        self.stream = open(path, "rb")

    @staticmethod
    def get_file_name(file_path: str) -> str:
        """Возвращает имя файла из пути файла"""
        head, tail = ntpath.split(file_path)
        return tail or ntpath.basename(head)

    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Возвращает размер файла в байтах, если файл существует."""
        if os.path.exists(file_path):
            return os.path.getsize(file_path)
        else:
            raise FileNotFoundError(f"File {file_path} not found.")

    @staticmethod
    def get_file_type(file_path: str) -> str:
        """Возвращает MIME-тип файла на основе его пути."""
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type if mime_type else "unknown/unknown"

    @staticmethod
    def get_file_type_from_enum(file_path: str) -> FileTypes:
        """Возвращает соответствующий элемент Enum FileTypes на основе MIME-типа файла."""
        mime_type = File.get_file_type(file_path)
        for file_type in FileTypes:
            if mime_type == file_type.mime_type:
                return file_type.value
        return None

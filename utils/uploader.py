from utils.purpose import Purpose
from typing import Iterable, Optional, Union
from openai.types import FileObject
from openai.types.beta import Thread, Assistant
from openai import OpenAI
from utils.file.file import File
from utils.tools import Tools

class FileUploader:
    def __init__(self, client: OpenAI) -> None:
        self.client = client

    def create_file(self, file: str, purpose: Optional[Iterable[Purpose]] = Purpose.Assistants) -> FileObject:
        return self.client.files.create(
            file=File(file).stream, purpose=str(purpose)
        )
    
    def create_files(self, files: list[str], purpose: Optional[Iterable[Purpose]] = Purpose.Assistants) -> list[FileObject]:
        file_objects = []
        for file in files:
            file = File(file)
            file_objects.append(self.client.files.create(
                file=file.stream, purpose=str(purpose)
            ))
        return file_objects
    
    def attach(self, 
               content: str, 
               message_file: Optional[FileObject] = None,
               type: Optional[Iterable[Tools.FileOperations]] = Tools.FileOperations.FILE_SEARCH) -> Thread:
            if isinstance(content, str) and message_file is not None:
                return self.client.beta.threads.create(
                    messages=[
                        {
                            "role": "user",
                            "content": content,
                            "attachments": [
                                {"file_id": message_file.id, "tools": [{"type": str(type)}]},
                            ],
                        }
                    ]
                )
            elif content is not None:
                return self.client.beta.threads.create(content)
            else:
                raise ValueError("Invalid arguments provided.")
            
    def attach_many(self, 
                    content: str, 
                    message_files: list[FileObject],
                    type: Optional[Iterable[Tools.FileOperations]] = Tools.FileOperations.FILE_SEARCH) -> Thread:
        attachments = []
        
        if message_files:
            for message_file in message_files:
                print(message_file)
                attachments.append({
                    "file_id": message_file.id, 
                    "tools": [{"type": str(type)}],
                })

        return self.client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": content,
                    "attachments": attachments,  # Используем сформированный список вложений
                }
            ]
        )
from utils.purpose import Purpose
from utils.schemas.attachment import Attachment, Tool, AttachmentContainer
from typing import Iterable, Optional, List, Union
from openai.types import FileObject
from openai.types.beta import Thread
from openai.types.beta.thread_create_params import Message, MessageAttachment
from openai.types.beta.threads.message_content import MessageContent
from openai import OpenAI
from utils.file.file import File

class FileUploader:
    def __init__(self, client: OpenAI) -> None:
        self.client = client

    def create_message(self, content: MessageContent) -> Message:
        return {
            "role": "user",
            "content": content,
        }

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
               content: MessageContent, 
               message_file: Optional[Union[MessageAttachment, str]] = None,
               type: Optional[Tool] = Tool(type='file_search')) -> Thread:
            attachment: Attachment
            message: Message = self.create_message(content)
            if message_file:
                attachment = AttachmentContainer(
                    attachments=[
                        MessageAttachment(
                            file_id=message_file.id,
                            tools=[Tool(type=str(type))]
                        )
                    ]
                )
                message["attachments"] = attachment.attachments
                return self.client.beta.threads.create(messages=[message])   
            else:
                raise ValueError("Invalid arguments provided.")
            
    def attach_many(self, 
                    content: MessageContent, 
                    message_files: Optional[List[Union[MessageAttachment, str]]] = None,
                    type: Optional[Tool] = Tool(type='file_search')) -> Thread:
            message: Message = self.create_message(content)
            attachments = []
            if message_files:
                for message_file in message_files:
                    attachments.append(
                        MessageAttachment(
                            file_id=message_file.id, 
                            tools=[Tool(type=str(type))]
                        )
                    )
            attachment_container = AttachmentContainer(attachments=attachments)
            message['attachments'] = attachment_container.attachments
            return self.client.beta.threads.create(messages=[message])   

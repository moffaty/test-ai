from openai import OpenAI
from typing import Optional, List, Union
from services.uploader.schemas import File, FileObject, FilePurpose
from services.assistant.schemas.message import Message, MessageContent, Thread
from services.assistant.schemas.attachment import (
    MessageAttachment,
    AttachmentContainer,
    Tool,
)


class FileUploader:
    def __init__(self) -> None:
        self.client = OpenAI()

    async def upload(
        self, files: List[str], purpose: Optional[str] = "assistants"
    ) -> List[FileObject]:
        if not files:
            return []
        file_objects = []
        for file in files:
            file_instance = File(file)
            file_object = self.client.files.create(
                file=(file_instance.filename, file_instance.stream), purpose=purpose
            )
            file_objects.append(file_object)

        return file_objects

    def create_message(self, content: MessageContent) -> Message:
        return {
            "role": "user",
            "content": content,
        }

    def create_file(
        self, file: str, purpose: Optional[FilePurpose] = "assistants"
    ) -> FileObject:
        return self.client.files.create(file=File(file).stream, purpose=str(purpose))

    def create_files(
        self, files: list[str], purpose: Optional[FilePurpose] = "assistants"
    ) -> list[FileObject]:
        file_objects = []
        for file in files:
            file = File(file)
            file_objects.append(
                self.client.files.create(file=file.stream, purpose=str(purpose))
            )
        return file_objects

    def get_thread(self, thread_id: str):
        return self.client.beta.threads.retrieve(thread_id)

    def attach(
        self,
        assistant_id: str,
        content: Union[MessageContent, str],
        message_files: Optional[
            Union[MessageAttachment, str, List[Union[MessageAttachment, str]]]
        ] = None,
        type: Optional[Tool] = Tool(type="file_search"),
    ) -> Thread:
        message: Message = self.create_message(content)
        attachments = []

        if message_files:
            if not isinstance(message_files, list):
                message_files = [message_files]

            for message_file in message_files:
                attachments.append(
                    MessageAttachment(file_id=message_file.id, tools=[type.to_dict()])
                )

            attachment_container = AttachmentContainer(attachments=attachments)
            message["attachments"] = attachment_container.attachments
        return self.client.beta.threads.create(
            assistant_id=assistant_id,
            thread={"messages": [message]},
        )

from typing import List, Optional

from openai import NotFoundError, OpenAI

from services.assistant.schemas import (
    AssistantTool,
    AttachmentContainer,
    Message,
    MessageAttachment,
    Thread,
    ThreadDeleted,
)
from openai.types import FileObject


class ChatHandler:
    def __init__(self, client: OpenAI) -> None:
        self.client = client

    def delete_chat(self, thread_id: str) -> ThreadDeleted:
        try:
            return self.client.beta.threads.delete(thread_id=thread_id)
        except NotFoundError:
            return ThreadDeleted(id=thread_id, deleted=False, object="thread.deleted")

    def attach_message(self, message: Message, thread_id: Optional[str] = None) -> str:
        content = message["content"]
        message_files = message["attachments"]
        return self.attach(content, message_files, thread_id=thread_id)

    def attach(
        self,
        content: str,
        message_files: Optional[List[MessageAttachment]] = None,
        assistant_tool: Optional[AssistantTool] = None,
        thread_id: Optional[str] = None,
    ) -> Thread:
        assistant_tool = self.__define_tool(assistant_tool)
        message: Message = self.__create_message(content)
        message_files = self.__define_message_files(message_files)
        message["attachments"] = self.__create_attachment_container(message_files)

        if thread_id is not None:
            return self.client.beta.threads.messages.create(
                thread_id,
                content=message["content"],
                attachments=message["attachments"],
                role=message["role"],
            )

        return self.client.beta.threads.create(messages=[message])

    def create_empty_thread(self) -> str:
        return self.client.beta.threads.create().id

    def create_thread(
        self, content: str, message_files: List[FileObject], thread_id: Optional[str]
    ) -> Thread:
        message = self.__combine_message(content, message_files)
        return self.attach_message(message, thread_id)

    def __define_tool(
        self, assistant_tool: Optional[AssistantTool] = None
    ) -> AssistantTool:
        if not assistant_tool:
            return AssistantTool(type="file_search")
        return assistant_tool

    def __define_message_files(
        self, message_files: Optional[List[MessageAttachment]] = None
    ) -> List[MessageAttachment]:
        if not message_files:
            return []
        return message_files

    def __create_attachment_container(
        self,
        files: List[MessageAttachment],
    ) -> AttachmentContainer:
        attachment_container = AttachmentContainer(attachments=files)
        return attachment_container.attachments

    def __combine_message(
        self, content: str, message_files: List[FileObject]
    ) -> Message:
        attachments: List[MessageAttachment] = []
        for file_obj in message_files:
            attachments.append(
                MessageAttachment(file_id=file_obj.id, tools=[{"type": "file_search"}])
            )

        message = Message(content=content, attachments=attachments)
        return message

    def __create_message(self, content: str) -> Message:
        return {"role": "user", "content": content}

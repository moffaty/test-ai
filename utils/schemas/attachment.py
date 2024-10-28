from pydantic import BaseModel
from typing import List, Literal
from openai.types.beta.thread_create_params import MessageAttachment

class Tool(BaseModel):
    type: Literal['file_search', 'code_interpreter', 'function']

    def __str__(self) -> str:
        return self.type

class AttachmentContainer(BaseModel):
    attachments: List[MessageAttachment]

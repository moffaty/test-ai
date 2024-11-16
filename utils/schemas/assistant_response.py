from typing import Optional

from pydantic import BaseModel


class AssistantResponse(BaseModel):
    thread_id: str
    content: Optional[str] = ""

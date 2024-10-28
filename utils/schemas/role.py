from pydantic import BaseModel
from typing import Literal

class Role(BaseModel):
    role: Literal['user', 'assistant']
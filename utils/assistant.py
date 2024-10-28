from openai import OpenAI
from typing import Optional, Literal
from dotenv import dotenv_values, set_key
from openai.types.beta import Assistant
from openai.types.beta import AssistantDeleted
from openai.pagination import SyncCursorPage
from openai._types import NotGiven, NOT_GIVEN


class AssistantsManager:
    def __init__(self, client: OpenAI, assistant_id: Optional[str] = None) -> None:
        self.default_name = "General Assistant"
        self.client = client
        self.id = assistant_id
        self.assistant = None

        config = dotenv_values(".env.secret")

        if assistant_id is None:
            self.id = config.get("ASSISTANT_ID")

        if self.id is None or self.id == "":
            self.assistant = self.create()
            self.id = self.assistant.id

            set_key(".env.secret", "ASSISTANT_ID", self.id)
        else:
            self.assistant = self.find(self.id)
            self.id = self.assistant.id

    def create(
        self, name: Optional[str] = None, instructions: Optional[str] = None
    ) -> Assistant:
        return self.client.beta.assistants.create(
            name=name or self.default_name,
            instructions=instructions
            or (
                "You are a versatile assistant capable of handling various everyday tasks. "
                "You can assist with answering questions, providing information, "
                "managing schedules, and offering suggestions. "
                "Use your knowledge to help users with practical advice and solutions. "
                "For example, you can help users find recipes, schedule meetings, "
                "or summarize important documents. Always aim to provide clear and concise answers."
            ),
            model="gpt-4o",
            tools=[{"type": "file_search"}],
        )

    def find(self, assistant_id: str) -> Assistant:
        return self.client.beta.assistants.retrieve(assistant_id)

    def delete(self, assistant_id: str) -> AssistantDeleted:
        return self.client.beta.assistants.delete(assistant_id)

    def list(
        self,
        *,
        after: str | NotGiven = NOT_GIVEN,
        before: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        order: Literal["asc", "desc"] | NotGiven = NOT_GIVEN
    ) -> SyncCursorPage[Assistant]:
        return self.client.beta.assistants.list(
            after=after, before=before, limit=limit, order=order
        )

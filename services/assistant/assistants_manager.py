from openai import OpenAI
from typing import Optional, Literal, Union
from dotenv import dotenv_values
from openai import NotFoundError, OpenAI
from openai._types import NOT_GIVEN, NotGiven
from openai.pagination import SyncCursorPage
from openai.types.beta import Assistant, AssistantDeleted, AssistantToolParam


class AssistantsManager:
    def __init__(
        self,
        client: OpenAI,
        assistant_id: Optional[str] = None,
        model: Optional[str] = "gpt-4o",
    ) -> None:
        self.default_name = "General Assistant"
        self.client = client
        self.id = assistant_id
        self.assistant: Union[Assistant, None] = None
        self.config = dotenv_values(".env.secret")
        self.model = model
        self.define()

    def define(self) -> None:
        self.assistant = self.create_or_find(self.id)
        self.id = self.assistant.id

    def create_or_find(self, assistant_id: Optional[str]) -> Assistant:
        if not assistant_id or self.config.get("ASSISTANT_ID") == " ":
            assistants = self.list_assistants(limit=1).data
            return assistants[0] if assistants else self.create(model=self.model)
        else:
            try:
                return self.find(assistant_id)
            except NotFoundError:
                return self.create(model=self.model)

    def create(
        self,
        name: Optional[str] = None,
        instructions: Optional[str] = None,
        model: Optional[str] = "gpt-4o",
        tools: Optional[AssistantToolParam] = None,
    ) -> Assistant:
        tools = self.__calc_tools(tools)
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
            model=model,
            tools=[tools],
        )

    def find(self, assistant_id: str) -> Assistant:
        return self.client.beta.assistants.retrieve(assistant_id)

    def delete(self, assistant_id: str) -> AssistantDeleted:
        try:
            return self.client.beta.assistants.delete(assistant_id)
        except NotFoundError:
            return AssistantDeleted(
                id=assistant_id, deleted=False, object="assistant.deleted"
            )

    def list_assistants(
        self,
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[Literal["asc", "desc"], NotGiven] = NOT_GIVEN,
    ) -> SyncCursorPage[Assistant]:
        return self.client.beta.assistants.list(
            after=after, before=before, limit=limit, order=order
        )

    def __calc_tools(
        self, tools: Optional[AssistantToolParam] = None
    ) -> AssistantToolParam:
        if not tools:
            return AssistantToolParam(type="file_search")
        return tools

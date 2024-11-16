from openai import AsyncOpenAI
from services.safe_openai import SafeOpenAI
from dotenv import dotenv_values, load_dotenv
from typing import Optional, AsyncGenerator, Union
from services.assistant.assistants_manager import AssistantsManager
from services.assistant.schemas import AssistantResponse
from services.assistant.chat_handler import ChatHandler


class OpenAIAssistantService:
    def __init__(self, assistent_id: Optional[str] = None) -> None:
        load_dotenv(".env.secret")
        self.config = dotenv_values()
        self.is_streaming = self.config.get("SERVICES_ASSISTANT_STREAMING")
        self.client = SafeOpenAI()
        self.async_client = AsyncOpenAI()
        self.chat = ChatHandler()
        self.assistant_manager = AssistantsManager(assistent_id)
        self.streaming_media_type = "text/event-stream"

    async def get_answer(
        self, thread_id: str, assistant_id: Optional[str] = None
    ) -> Union[AsyncGenerator[str, str], AssistantResponse]:
        if self.is_streaming:
            return self.stream_answer(thread_id, assistant_id)
        else:
            return AssistantResponse(
                thread_id=thread_id, content=self.fetch_answer(thread_id, assistant_id)
            )

    async def stream_answer(
        self, thread_id: str, assistant_id: Optional[str] = None
    ) -> AsyncGenerator[str, str]:
        if not assistant_id:
            assistant_id = self.assistant_manager.id

        assistant = self.assistant_manager.find(assistant_id)

        stream = self.async_client.beta.threads.runs.stream(
            assistant_id=assistant.id, thread_id=thread_id
        )

        async with stream as stream:
            async for text in stream.text_deltas:
                yield f"{text}"

    def fetch_answer(self, thread_id: str, assistant_id: Optional[str] = None) -> str:
        if not assistant_id:
            assistant_id = self.assistant_manager.id

        assistant = self.assistant_manager.find(assistant_id)
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id, assistant_id=assistant.id
        )

        messages = list(
            self.client.beta.threads.messages.list(thread_id=thread_id, run_id=run.id)
        )

        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = self.client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        return message_content.value

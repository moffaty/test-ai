from openai import OpenAI
from dotenv import dotenv_values
from typing import Optional
from utils.uploader import FileUploader
from utils.assistant import AssistantsManager


class Client:
    def __init__(self, assistent_id: Optional[str] = None) -> None:
        config = dotenv_values(".env.secret")
        self.client = OpenAI(api_key=config["OPENAI_API_KEY"])
        self.uploader = FileUploader(self.client)
        self.assistant_manager = AssistantsManager(self.client, assistent_id)

    def send(self, thread, assistant_id: Optional[str] = None):
        if assistant_id is None:
            assistant_id = self.assistant_manager.id

        assistant = self.assistant_manager.find(assistant_id)
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=assistant.id
        )

        messages = list(
            self.client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
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

        print(message_content.value)
        print("\n".join(citations))

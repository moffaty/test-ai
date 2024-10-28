import os
from typing_extensions import override
from openai import OpenAI
from dotenv import dotenv_values
from utils.uploader import FileUploader

class Client:
    def __init__(self):
        config = dotenv_values('.env.secret')
        self.client = OpenAI(api_key=config['OPENAI_API_KEY'])
        self.uploader = FileUploader(self.client)
        self.assistant = self.create_assistant()

    def create_assistant(self):
        return self.client.beta.assistants.create(
            name="Financial Analyst Assistant",
            instructions="You are an expert financial analyst. Use you knowledge base to answer questions about audited financial statements.",
            model="gpt-4o",
            tools=[{"type": 'file_search'}],
        )
    
    def send(self, thread):
        client = self.client
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=self.assistant.id
        )

        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))

if __name__ == '__main__':
    client = Client()
    # message_pdf = client.uploader.create_files(['test/test.pdf', 'test/test2.pdf'])
    # message_json = client.uploader.create_file('test/test.json')
    message_docx = client.uploader.create_file('test/test.docx')
    # thread = client.uploader.attach('Tell me what in "message" in this json', message_json)

    # client.send(thread)

    # thread = client.uploader.attach_many('Tell me how much money i spent. And tell me how much i need to payback', message_pdf)

    # client.send(thread)

    thread = client.uploader.attach_many('Сколько весит загруженный файл', [message_docx])

    client.send(thread)

    thread = client.uploader.attach_many(f'Сделай краткую выжимку из прошлого текста. File id=${message_docx.id}', [message_docx])

    client.send(thread)


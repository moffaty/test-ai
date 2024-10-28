from utils.client import Client

if __name__ == "__main__":
    client = Client()

    message_pdf = client.uploader.create_files(["test/test.pdf", "test/test2.pdf"])
    # message_json = client.uploader.create_file('test/test.json')
    # message_docx = client.uploader.create_file('test/test.docx')
    # # thread = client.uploader.attach('Tell me what in "message" in this json', message_json)

    # # client.send(thread)

    thread = client.uploader.attach(
        "Tell me how much money i spent. And tell me how much i need to payback",
        message_pdf,
    )

    client.send(thread)

    # thread = client.uploader.attach('Привет. Как сделать программу "Hello world" на Perl. Напиши только код')

    # client.send(thread)

    # thread = client.uploader.attach(f'Сделай краткую выжимку из прошлого текста. И скажи что находится в файле json', [message_docx, message_json])

    # client.send(thread)

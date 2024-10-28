from enum import Enum


class FileTypes(Enum):
    C = (".c", "text/x-c")
    CPP = (".cpp", "text/x-c++src")
    CS = (".cs", "text/x-csharp")
    CSS = (".css", "text/css")
    DOCX = (
        ".docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    GO = (".go", "text/x-go")
    HTML = (".html", "text/html")
    JAVA = (".java", "text/x-java")
    JS = (".js", "text/javascript")
    JSON = (".json", "application/json")
    MD = (".md", "text/markdown")
    PDF = (".pdf", "application/pdf")
    PHP = (".php", "text/x-php")
    PPTX = (
        ".pptx",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )
    PY = (".py", "text/x-python")
    RB = (".rb", "text/x-ruby")
    SH = (".sh", "application/x-sh")
    TEX = (".tex", "text/x-tex")
    TS = (".ts", "application/typescript")
    TXT = (".txt", "text/plain")

    def __init__(self, extension, mime_type):
        self.extension = extension
        self.mime_type = mime_type

    def __str__(self):
        return f"{self.extension} ({self.mime_type})"

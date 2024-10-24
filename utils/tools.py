from enum import Enum

class Tools():
    class FileOperations(Enum):
        FILE_SEARCH = 'file_search'
        CODE_INTERPRETER = 'code_interpreter'
        FUNCTION_CALLING = 'function'

        def __init__(self, type):
            self.type = type

        def __str__(self):
            return f"{self.type}"
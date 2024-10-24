from enum import Enum

class Purpose(Enum):
    FineTune = "fine_tune"
    Batch = "batch"
    Classify = "classify"
    UserData = "user_data"
    Responses = "responses"
    Vision = "vision"
    Evals = "evals"
    Assistants = "assistants"

    def __init__(self, purpose):
        self.purpose = purpose

    def __str__(self):
        return f"{self.purpose}"

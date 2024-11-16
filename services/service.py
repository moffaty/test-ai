from openai import OpenAI, AsyncOpenAI, OpenAIError


class Service:
    def __init__(self) -> None:
        self.client = OpenAI()
        self.async_client = AsyncOpenAI()

    def safe_api_call(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OpenAIError as e:
            print(f"API error: {e}")
            raise

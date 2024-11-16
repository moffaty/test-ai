from openai import OpenAI, OpenAIError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openai import OpenAI as OpenAIType


class SafeOpenAI:
    def __init__(self) -> None:
        self._client: "OpenAIType" = OpenAI()

    def _safe_call(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OpenAIError as e:
            print(f"API error: {e}")
            raise

    def __getattr__(self, name):
        """
        Проксирует вызовы атрибутов и методов оригинального клиента.
        Если это метод, оборачивает его в _safe_call.
        """
        attr = getattr(self._client, name)

        if callable(attr):

            def safe_method(*args, **kwargs):
                return self._safe_call(attr, *args, **kwargs)

            return safe_method

        return attr

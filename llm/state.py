from typing import TypedDict


class State(TypedDict):
    document: str
    question: str
    generation: str
    message_history: list
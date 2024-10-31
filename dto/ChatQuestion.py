from pydantic import BaseModel


class ChatQuestion(BaseModel):
    question_text: str

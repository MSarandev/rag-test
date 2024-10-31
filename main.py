from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, FileResponse
from dto import ChatQuestion

from service import LlmService

origins = [
    "http://localhost:8000/*",
    "http://localhost*"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_service = LlmService.LlmService()


@app.get("/", response_class=HTMLResponse)
async def get_home_page():
    return FileResponse("static/index.html")


@app.post("/query")
def read_item(chat_question: ChatQuestion.ChatQuestion):
    response = llm_service.handle_input(chat_question.question_text)

    return response

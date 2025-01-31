import logging

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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@app.get("/", response_class=HTMLResponse)
async def get_home_page():
    return FileResponse("static/index.html")


@app.get("/web-query", response_class=HTMLResponse)
async def get_web_querier():
    return FileResponse("static/web.html")


@app.get("/db-query", response_class=HTMLResponse)
async def get_db_querier():
    return FileResponse("static/db.html")


@app.get("/docs-query", response_class=HTMLResponse)
async def get_docs_querier():
    return FileResponse("static/docs.html")


@app.post("/query/web")
def read_item(chat_question: ChatQuestion.ChatQuestion):
    return llm_service.handle_web_scrape(chat_question.question_text)


@app.post("/query/db")
def read_item(chat_question: ChatQuestion.ChatQuestion):
    return llm_service.handle_db_input(chat_question.question_text)


@app.post("/query/docs")
def read_item(chat_question: ChatQuestion.ChatQuestion):
    return llm_service.handle_docs_input(chat_question.question_text)

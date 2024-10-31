import backoff
import openai

from llm import IndexBuilder


class LlmService:
    def __init__(self):
        self.index_builder = IndexBuilder.IndexBuilder()

    @backoff.on_exception(backoff.expo, openai.RateLimitError, max_tries=2)
    def handle_input(self, input_request):
        index = self.index_builder.index

        # query_engine = index.as_query_engine(streaming=False)
        query_engine = index.as_chat_engine()

        # response = query_engine.query(input_request)
        print(f"Request: {input_request}")

        response = query_engine.chat(input_request)
        print(f"Response: {response}")

        return response

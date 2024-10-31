import backoff
import openai

from loaders.DocumentLoader import DocumentLoader


class LlmService:
    def __init__(self):
        self.document_loader = DocumentLoader()

    @backoff.on_exception(backoff.expo, openai.RateLimitError, max_tries=2)
    def handle_input(self, input_request):
        index = self.document_loader.index

        # query_engine = index.as_query_engine(streaming=False)
        query_engine = index.as_chat_engine()

        # response = query_engine.query(input_request)
        print(f"Request: {input_request}")

        response = query_engine.chat(input_request)
        print(f"Response: {response}")

        return response

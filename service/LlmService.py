import logging

import backoff
import openai

from loaders.DocumentLoader import DocumentLoader
from loaders.DBLoader import DBLoader
from loaders.WebLoader import WebLoader

logger = logging.getLogger(__name__)
MAX_RETRIES = 2


class LlmService:
    def __init__(self):
        self.document_loader = DocumentLoader()
        self.db_loader = DBLoader()
        self.web_loader = WebLoader()

    @backoff.on_exception(backoff.expo, openai.RateLimitError, max_tries=MAX_RETRIES)
    def handle_docs_input(self, input_request):
        index = self.document_loader.index

        # query_engine = index.as_query_engine(streaming=False)
        query_engine = index.as_chat_engine()

        # response = query_engine.query(input_request)
        print(f"Request: {input_request}")

        response = query_engine.chat(input_request)
        print(f"Response: {response}")

        return response

    @backoff.on_exception(backoff.expo, openai.RateLimitError, max_tries=MAX_RETRIES)
    def handle_db_input(self, input_request):
        # query_obj = self.db_loader.query_specific_table()  # SINGLE TABLE
        query_obj = self.db_loader.query_globally()  # MULTI TABLE

        try:
            print(f"Request: {input_request}")

            response = query_obj.query(input_request)

            print(f"Response: {response}")
            return response
        except:
            logger.error("Error in query: " + input_request)
            return None

    @backoff.on_exception(backoff.expo, openai.RateLimitError, max_tries=MAX_RETRIES)
    def handle_web_scrape(self, input_request):
        index = self.web_loader.get_index()

        query_engine = index.as_chat_engine()

        print(f"Request: {input_request}")

        response = query_engine.chat(input_request)

        print(f"Response: {response}")

        return response

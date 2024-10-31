import logging
import os

import backoff
import openai
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from auth.OpenAI_Auth import OpenAI_Auth
from support.Logger import Logger

DOCS_DIR = os.getenv('DIRECTORY')
INDEX_STORE_DIR = os.getenv('INDEX_STORE')


class DocumentLoader:
    def __init__(self):
        OpenAI_Auth()

        self.logger = Logger()
        self.index_input(DOCS_DIR)
        self.index = self.get_index(INDEX_STORE_DIR)

    @backoff.on_exception(backoff.expo, openai.RateLimitError, max_tries=2)
    def index_input(self, input_dir):
        doc = SimpleDirectoryReader(input_dir).load_data()
        self.logger.info("Loaded PDF, creating index...")

        index = VectorStoreIndex.from_documents(doc, show_progress=True)
        self.logger.info("Index created")

        index.storage_context.persist(persist_dir=INDEX_STORE_DIR)
        self.logger.info("Index stored")

        return index

    def get_index(self, input_dir):
        try:
            storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORE_DIR)

            self.logger.info("Already have stored index, loading")

            return load_index_from_storage(storage_context)
        except FileNotFoundError:
            self.logger.info("No stored indices found. Creating a new one")
            self.index_input(input_dir)
            self.get_index(input_dir)

import logging
import os

import openai
import backoff
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage

load_dotenv()
API_KEY = os.getenv('API_KEY')
DOCS_DIR = os.getenv('DIRECTORY')
INDEX_STORE_DIR = os.getenv('INDEX_STORE')
CHROMA_DIR = os.getenv('CHROMA_DIR')
logger = logging.getLogger(__name__)


class IndexBuilder:

    def __init__(self):
        self.setup_key(API_KEY)
        self.index_input(DOCS_DIR)
        self.index = self.get_index(INDEX_STORE_DIR)

    @staticmethod
    def setup_key(api_key):
        logger.info(f"API key set: {api_key[:5]}***")
        openai.api_key = api_key

    @backoff.on_exception(backoff.expo, openai.RateLimitError, max_tries=2)
    def index_input(self, input_dir):
        doc = SimpleDirectoryReader(input_dir).load_data()
        logger.info("Loaded PDF, creating index...")

        index = VectorStoreIndex.from_documents(doc, show_progress=True)
        logger.info("Index created")

        index.storage_context.persist(persist_dir=INDEX_STORE_DIR)
        logger.info("Index stored")

        return index

    def get_index(self, input_dir):
        try:
            storage_context = StorageContext.from_defaults(persist_dir=INDEX_STORE_DIR)

            logger.info("Already have stored index, loading")

            return load_index_from_storage(storage_context)
        except FileNotFoundError:
            logger.info("No stored indices found. Creating a new one")
            self.index_input(input_dir)
            self.get_index(input_dir)

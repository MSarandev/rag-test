import os

from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, download_loader
from llama_index.readers.web import BeautifulSoupWebReader
from support.Logger import Logger

load_dotenv()


class WebLoader:
    def __init__(self):
        self.url = os.getenv("URL_TO_SCRAPE")
        self.logger = Logger()

    def get_index(self):
        try:
            loader = BeautifulSoupWebReader()
            documents = loader.load_data(urls=[self.url])

            self.logger.info(f"Loaded data for: {self.url}")
            return VectorStoreIndex.from_documents(documents)
        except:
            raise Exception(f"Failed to load index for: {self.url}")

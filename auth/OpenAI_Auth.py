import os

import openai
import logging

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


class OpenAI_Auth:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        self.setup_key(self.api_key)

    @staticmethod
    def setup_key(api_key):
        logger.info(f"API key set: {api_key[:5]}***")

        openai.api_key = api_key

import os

import openai
import logging

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()
API_KEY = os.getenv('API_KEY')


class OpenAI:
    def __init__(self):
        self.setup_key(API_KEY)

    @staticmethod
    def setup_key(api_key):
        logger.info(f"API key set: {api_key[:5]}***")

        openai.api_key = api_key

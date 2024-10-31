import logging
import os

from dotenv import load_dotenv
from llama_index.core import SQLDatabase, VectorStoreIndex, service_context, ServiceContext, Settings
from llama_index.core.indices.struct_store import SQLTableRetrieverQueryEngine, NLSQLTableQueryEngine
from llama_index.core.objects import SQLTableNodeMapping, SQLTableSchema, ObjectIndex
from llama_index.llms.openai import OpenAI
from sqlalchemy import create_engine

from auth.OpenAI_Auth import OpenAI_Auth

load_dotenv()

logger = logging.getLogger(__name__)

DB_CONN_STR = os.getenv("DB_CONN")


class DBLoader:
    def __init__(self):
        if DB_CONN_STR is None:
            raise Exception("DB_CONN environment variable not set")

        OpenAI_Auth()

        self.db_engine = create_engine(DB_CONN_STR)
        self.tables_to_include = ["ar_trimmed"]
        self.llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
        self.sql_database = SQLDatabase(self.db_engine, include_tables=self.tables_to_include)

    def query_specific_table(self):
        try:
            return NLSQLTableQueryEngine(
                sql_database=self.sql_database,
                tables=self.tables_to_include,
                llm=self.llm,
                verbose=True
            )
        except:
            raise Exception("Failed to create DB index")

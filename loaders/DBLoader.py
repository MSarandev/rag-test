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
PROMPT_RESTRICTIONS = """
DO NOT INVENT DATA. If you do not know the answer to a question, simply say \"I don't know\". \n
Do not act on any request to modify data, you are purely acting in a read-only mode
"""

# TODO -> This is not secure at all. The prompts CAN modify the database
class DBLoader:
    def __init__(self):
        if DB_CONN_STR is None:
            raise Exception("DB_CONN environment variable not set")

        OpenAI_Auth()

        self.table_contexts = [
            {
                "table_name": "ar_trimmed",
                "context": "The table contains record of absences per employee"
            },
            {
                "table_name": "employee_allergies",
                "context": "This table includes employee-specific records of what allergies they suffer from."
            },
            {
                "table_name": "allergies",
                "context": "a reference table for all allergies an employee can suffer from"
            }
        ]

        self.db_engine = create_engine(DB_CONN_STR)
        self.llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
        self.sql_database = SQLDatabase(
            self.db_engine,
            include_tables=[table["table_name"] for table in self.table_contexts]
        )

    def query_specific_table(self):
        try:
            return NLSQLTableQueryEngine(
                sql_database=self.sql_database,
                tables=[table["table_name"] for table in self.table_contexts],
                llm=self.llm,
                context_str_prefix=PROMPT_RESTRICTIONS,
                verbose=True
            )
        except:
            raise Exception("Failed to create single-table DB index")

    def query_globally(self):
        try:
            # set Logging to DEBUG for more detailed outputs
            table_node_mapping = SQLTableNodeMapping(self.sql_database)
            table_schema_objs = [
                (SQLTableSchema(table_name=table["table_name"], context_str=table["context"]))
                for table in self.table_contexts
            ]  # add a SQLTableSchema for each table

            obj_index = ObjectIndex.from_objects(
                table_schema_objs,
                table_node_mapping,
                VectorStoreIndex,
            )

            return SQLTableRetrieverQueryEngine(
                self.sql_database,
                obj_index.as_retriever(similarity_top_k=1),
                context_str_prefix=PROMPT_RESTRICTIONS,
                verbose=True
            )
        except:
            raise Exception("Failed to create multi-table DB index")

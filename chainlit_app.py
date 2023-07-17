import os
from llama_index.callbacks.base import CallbackManager
from llama_index import (
    LLMPredictor,
    ServiceContext,
    StorageContext,
    BeautifulSoupWebReader,
    load_index_from_storage,
)
from langchain.chat_models import ChatOpenAI
import openai
from constants import URLs

import chainlit as cl
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
openai.api_key = OPENAI_API_KEY

try:
    # Rebuild the storage context
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    # Load the index
    index = load_index_from_storage(storage_context)
except:
    # Storage not found; create a new one
    from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
    # Create an instance of BeautifulSoupWebReader
    reader = BeautifulSoupWebReader()

    # Load the URLs and retrieve the content
    documents = reader.load_data(URLs)
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist()


@cl.llama_index_factory
def factory():
    llm_predictor = LLMPredictor(
        llm=ChatOpenAI(openai_api_key=OPENAI_KEY,
            temperature=0,
            model_name="gpt-3.5-turbo",
            streaming=True,
            max_tokens=512
        ),
    )
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor,
        chunk_size=512,
        callback_manager=CallbackManager([cl.LlamaIndexCallbackHandler()]),
    )
    query_engine = index.as_query_engine(
        service_context=service_context,
        streaming=True,
    )

    return query_engine

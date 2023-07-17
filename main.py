from fastapi import FastAPI
from pydantic import BaseModel
from constants import URLs
from typing import List
from llama_index.callbacks.base import CallbackManager
from llama_index import (   LLMPredictor,
                            ServiceContext,
                            GPTVectorStoreIndex,
                            StorageContext,
                            BeautifulSoupWebReader,
                            load_index_from_storage,
                        )
from langchain.chat_models import ChatOpenAI
import openai
import os

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
openai.api_key = OPENAI_API_KEY

app = FastAPI()

# Pydantic object to handle user input
class BotRequest(BaseModel):
    query: str

# Pydantic object to handle metadata for each response
class MetaData(BaseModel):
    url: dict = {}
    text: str = ""
    similarity_score: float = 0.0

# Pydantic object to handle user output
class BotResponse(BaseModel):
    response: str
    metadata: List[MetaData] = []

class RasaLLM:
    storage_context = None
    service_context = None
    llm_predictor = None
    index = None
    query_engine = None
    
    @staticmethod
    def init():
        try:
            # Rebuild the storage context
            RasaLLM.storage_context = StorageContext.from_defaults(persist_dir="./storage")
            # Load the index
            RasaLLM.index = load_index_from_storage(RasaLLM.storage_context)
        except:
            # Storage not found; create a new one

            # Create an instance of BeautifulSoupWebReader
            reader = BeautifulSoupWebReader()

            # Load the URLs and retrieve the content
            documents = reader.load_data(URLs)
            RasaLLM.index = GPTVectorStoreIndex.from_documents(documents)
            RasaLLM.index.storage_context.persist()
        
        # Create LLM object
        RasaLLM.llm_predictor = LLMPredictor(llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY,
                                                    temperature=0,
                                                    model_name="gpt-3.5-turbo",
                                                    max_tokens=512
                                                    )
                                    )
        # Service Context Object to handle queries
        RasaLLM.service_context = ServiceContext.from_defaults(llm_predictor=RasaLLM.llm_predictor,chunk_size=512)
        
        # Creating Query Engine Instance
        RasaLLM.query_engine = RasaLLM.index.as_query_engine(service_context=RasaLLM.service_context)
               
    
@app.post("/query")
async def query_docs(bot_request: BotRequest)->BotResponse:
    """
        Query your docs using OpenAI and URLs. 
        Get response based on the data along with the URL,
        relevant texts and similarity score.
    """
    response = RasaLLM.query_engine.query(bot_request.query)
    doc_sources = []
    for source in response.source_nodes:
        meta = MetaData()
        if source.node.extra_info:
            meta.url = source.node.extra_info
        
        meta.text = source.node.text
        meta.similarity_score = source.score
        doc_sources.append(meta)
    
    return BotResponse(response=response.response, metadata=doc_sources)
        

# Intialize RasaLLM
RasaLLM.init()
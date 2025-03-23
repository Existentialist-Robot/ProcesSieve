import configparser
import os

from linkml_store import Client as LinkMlClient
from neo4j import GraphDatabase
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.kg.shared_storage import initialize_pipeline_status
from openai import OpenAI
from lightrag.utils import EmbeddingFunc
import numpy as np

config = configparser.ConfigParser()

config.read('config.ini')

cohere_config = config['cohere']
# Maybe move to config?
chat_model = cohere_config.get("chat_model", "command-a-03-2025")
embed_model = cohere_config.get("embed_model", "embed-english-v3.0")
CHUNK_TOKEN_SIZE = 1024
MAX_TOKENS = 4000

async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    return await openai_complete_if_cache(
        chat_model,
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key=config.get('cohere', 'apikey'),
        base_url="https://api.cohere.ai/compatibility/v1",
        **kwargs,
    )

async def embedding_func(texts: list[str]) -> np.ndarray:
    return await openai_embed(
        texts,
        model=embed_model,
        api_key=config.get('cohere', 'apikey'),
        base_url="https://api.cohere.ai/compatibility/v1",
    )

cohere_client = OpenAI(
    base_url="https://api.cohere.ai/compatibility/v1",
    api_key=config.get('cohere', 'apikey'),
)

nconf = config['neo4j']

linkMlStore = LinkMlClient().attach_database(f'neo4j://{nconf.get('username')}:{nconf.get('password')}@{nconf.get('host')}', alias='neo4j')
linkMlDb = linkMlStore.get_collection(nconf.get('database', 'neo4j'))

neoDriver = GraphDatabase().driver(f'neo4j://{nconf.get('host')}', auth=(nconf.get('username'), nconf.get('password')))

os.environ['NEO4J_URI'] = f'neo4j://{nconf.get('host')}'
os.environ['NEO4J_PASSWORD'] = nconf.get('password')
os.environ['NEO4J_USERNAME'] = nconf.get('username')

async def get_embedding_dim():
    test_text = ["This is a test sentence."]
    embedding = await embedding_func(test_text)
    embedding_dim = embedding.shape[1]
    return embedding_dim

async def initialize_rag():
    embedding_dimension = await get_embedding_dim()
    print(f"Detected embedding dimension: {embedding_dimension}")

    rag = LightRAG(
        working_dir='./ragdir',
        graph_storage="Neo4JStorage", #<-----------override KG default
        entity_extract_max_gleaning=1,
        enable_llm_cache=True,
        enable_llm_cache_for_entity_extract=True,
        embedding_cache_config=None,  # {"enabled": True,"similarity_threshold": 0.90},
        chunk_token_size=CHUNK_TOKEN_SIZE,
        llm_model_max_token_size=MAX_TOKENS,
        llm_model_func=llm_model_func,
        embedding_func=EmbeddingFunc(
            embedding_dim=embedding_dimension,
            max_token_size=500,
            func=embedding_func,
        ),
    )

    # Initialize database connections
    await rag.initialize_storages()
    # Initialize pipeline status for document processing
    await initialize_pipeline_status()

    return rag

import asyncio
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings 
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from prompts import prompt


# Setting control Global Defaults 
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-large-en-v1.5",
    device="cpu"
)
Settings.llm = Ollama(
    model = "llama3.1:8b",
    request_timeout=360.0,
    context_window=32768,
)

# Create RAG toll using LlamaIndex 
documents = SimpleDirectoryReader("data").load_data()


index = VectorStoreIndex.from_documents(
    documents
)
query_engine = index.as_query_engine(
    response_mode="tree_summarize",  # combines multiple chunks into a longer answer
    similarity_top_k=5               # retrieve more chunks for more context
)


async def search_documents(query: str) -> str:
    response = await query_engine.aquery(query)
    return str(response)


async def main():

    agent = AgentWorkflow.from_tools_or_functions(
        [search_documents],
        llm=Settings.llm,
        system_prompt=prompt
    )

    response = await agent.run(
        "I want to understand the project better. Help!"
    )

    print(response)












if __name__ == "__main__":
    asyncio.run(main())
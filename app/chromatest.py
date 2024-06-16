from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma

import chromadb

collection_name="chat_history"

# Set up Ollama LLM, embedding model and Chroma database.
ollama_url = "http://192.168.100.62:11434"
ollama_embeddings = OllamaEmbeddings(base_url=ollama_url, model="nomic-embed-text")

# Create a Chroma client on out hosted ChromaDB instance. Optionally, uncomment the reset() 
# method to clear the database. 
client = chromadb.HttpClient(host="localhost", port=8000)
# client.reset()


# Create a Langchain Chroma database and add some text documents.
db_chroma = Chroma(
    client=client,
    collection_name=collection_name,
    embedding_function=ollama_embeddings,
)

chat1 = [
    "Cats can jump up to six times their own body length.",
    "Cats have excellent night vision and can see in very low light.",
    "Cats purr not just when they're happy, but also when they're injured or seeking comfort.",
    "Cats spend an average of 15 hours a day sleeping or napping.",
    "Some cat breeds, like the Sphynx, have very little fur.",
    "Dogs are known for their loyalty and companionship.",
    "Dogs come in a variety of breeds, each with unique characteristics.",
    "Dogs have been domesticated for thousands of years.",
    "Training and socialization are important for a well-behaved dog.",
    "Many people consider dogs to be part of their family.",
]
meta1 = [
    {"chat_id": 123},
    {"chat_id": 123},
    {"chat_id": 123},
    {"chat_id": 123},
    {"chat_id": 123},
    {"chat_id": 456},
    {"chat_id": 456},
    {"chat_id": 456},
    {"chat_id": 456},
    {"chat_id": 456},
]
#db_chroma.add_texts(texts=chat1, metadatas=meta1)

# query the DB
query = "animals"
docs = db_chroma.similarity_search_with_score(query, 10, filter={"chat_id": "123464"})

# print results
for doc in docs:
    print(doc[0].page_content + " (" + f"{doc[1]}" + ")")
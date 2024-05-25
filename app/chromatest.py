from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma

import chromadb

collection_name="my_collection"

# Set up Ollama LLM, embedding model and Chroma database.
ollama_url = "http://localhost:11434"
ollama_embeddings = OllamaEmbeddings(base_url=ollama_url, model="nomic-embed-text")

# Create a Chroma client on out hosted ChromaDB instance. Optionally, uncomment the reset() 
# method to clear the database. 
client = chromadb.HttpClient(host="localhost", port=8000)
#client.reset()


# Create a Langchain Chroma database and add some text documents.
db_chroma = Chroma(
    client=client,
    collection_name=collection_name,
    embedding_function=ollama_embeddings,
)

texts = [
    "A list of 10 things that can inspire creativity.",
    "The importance of perseverance in achieving long-term goals.",
    "The role of mentorship in fostering personal and professional growth.",
    "The benefits of curiosity and the pursuit of knowledge.",
    "The power of collaboration in problem-solving and innovation.",
    "The importance of work-life balance for overall well-being.",
    "The impact of emotional intelligence on leadership effectiveness.",
    "The value of integrity and ethical conduct in all aspects of life.",
    "The significance of setting goals and taking action towards them.",
    "The transformative potential of learning new skills and knowledge throughout life."
]
#db_chroma.add_texts(texts=texts)

# query the DB
query = "I find it difficult to manage my work life and personal life"
docs = db_chroma.similarity_search_with_score(query, 5)

# print results
for doc in docs:
    print(doc[0].page_content + " (" + f"{doc[1]}" + ")")
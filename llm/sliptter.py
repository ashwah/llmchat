
import os
# from langchain.chains import LLMChain
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter, MarkdownTextSplitter 
from langchain_openai.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain_chroma import Chroma
from rich import print

load_dotenv()

# Print the OPENAI_API_KEY env variable
key = os.getenv("OPENAI_API_KEY")

# Vecorizing input.md
loader = TextLoader("input.md")

documents = loader.load()
#text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
text_splitter = MarkdownTextSplitter()

documents = text_splitter.split_documents(documents)
#print(documents)
openai_embeddings = OpenAIEmbeddings(openai_api_key=key)
db = Chroma.from_documents(documents, openai_embeddings)

query = "Tell me about the glossary"
docs = db.similarity_search(query, k=3)
print(docs)

llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo")
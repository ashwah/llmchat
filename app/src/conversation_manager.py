from flask import request, jsonify
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from history_retriever import HistoryRetriever
from dotenv import load_dotenv

import os
import chromadb
import datetime
import uuid

load_dotenv()

# Get env variables that are set in app/.env.
ollama_host = os.environ.get('OLLAMA_HOST')
ollama_port = os.environ.get('OLLAMA_PORT')
chroma_host = os.environ.get('CHROMA_HOST')
chroma_port = os.environ.get('CHROMA_PORT')

# Set up Ollama LLM, embedding model and Chroma database.
ollama_url = f"http://{ollama_host}:{ollama_port}"
ollama_embeddings = OllamaEmbeddings(base_url=ollama_url, model="nomic-embed-text")
llm = Ollama(base_url=ollama_url, model="llama3")

# Create a Chroma client on out hosted ChromaDB instance.
client = chromadb.HttpClient(host=chroma_host, port=chroma_port)

# Set a collection name for the Chroma database.
collection_name="chat_history"

# Create a Langchain Chroma database.
chroma_db = Chroma(
    client=client,
    collection_name=collection_name,
    embedding_function=ollama_embeddings,
)

def process_new_message(chat_id, user_id, message_body):

    # Retrieve any relavent previous conversation.
    reciever = HistoryRetriever(chroma_db=chroma_db, chat_id=chat_id)
    relevant_history = reciever.invoke(message_body)

    # Ensure the history is sorted by timestamp.
    sorted_history = sorted(relevant_history, key=lambda x: x[0].metadata['timestamp'])

    history = []
    for history_item in sorted_history:
        message = history_item[0].page_content 
        user = history_item[0].metadata["user_id"]
        timestamp = history_item[0].metadata["timestamp"] 
        # Concat the message with the user and timestamp
        history.append(f"User {user}: {message} (At: {timestamp})")

    metadata = {
        "chat_id": chat_id, 
        "user_id": user_id,
        "timestamp": int(datetime.datetime.now().timestamp()),
        "message_id": str(uuid.uuid4()),
    }
    
    chroma_db.add_texts(texts=[message_body], metadatas=[metadata])

    prompt = PromptTemplate.from_template(
        """
        You are an AI assistant called AI-Guy that helps users with their questions. The current user 
        input is as follows: 
        
        {input}

        This is the relevant chat history, keep this in mind but don't comment that this was provided:
        
        {history}
        """
    )

    prompt_with_subs = prompt.invoke({"input": message_body, "history": relevant_history});

    # Converse with the LLM
    response = llm.invoke(prompt_with_subs)
    
    metadata = {
        "chat_id": chat_id, 
        "user_id": "AI-Guy",
        "timestamp": int(datetime.datetime.now().timestamp()),
        "message_id": str(uuid.uuid4()),
    }
    
    chroma_db.add_texts(texts=[response], metadatas=[metadata])

    message = {
        "message_id": metadata["message_id"],
        "user": "LLM",
        "timestamp": metadata["timestamp"],
        "body": response
    }

    return jsonify(message)

def load_chat(chat_id):
    # Prepare the chat data to be returned.
    chat_data = {
        "conversation": {
            "converation_id": chat_id,
            "title": "My Chat Conversation",
            "created_at": "123123123"
        },
        "history": [] 
    }

    collection = client.get_collection(name=collection_name)
    chat_message_history = collection.get(where={"chat_id": chat_id})


    history = []

    # Get the messages from the chat message history.
    for key, message in enumerate(chat_message_history["documents"]):

        metadata = chat_message_history["metadatas"][key]
        user = metadata["user_id"]
        timestamp = metadata["timestamp"]
        message_id = metadata["message_id"]

        new_message = {
            "message_id": message_id,
            "timestamp": timestamp,
            "user": user,
            "body": message
        }

        history.append(new_message)


    sorted_history = sorted(history, key=lambda x: x['timestamp'])

    chat_data["history"] = sorted_history

    return jsonify(chat_data)
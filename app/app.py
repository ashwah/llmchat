from flask import Flask, request, jsonify
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
# from langchain_community.vectorstores import Chroma

import uuid
import datetime
import chromadb

app = Flask(__name__)

collection_name="my_collection"

# Set up Ollama LLM and embeddings
ollama_url = "http://localhost:11434"
llm = Ollama(base_url=ollama_url, model="phi3")
ollama_embeddings = OllamaEmbeddings(base_url=ollama_url, model="nomic-embed-text")

# Set up Chroma database
client = chromadb.HttpClient(host="localhost", port=8000)


# Create a Langchain Chroma database and add some text documents.
db_chroma = Chroma(
    client=client,
    collection_name=collection_name,
    embedding_function=ollama_embeddings,
)

# Load chat data
@app.route("/chat/<chat_id>/load", methods=["GET"])
def load_chat(chat_id):
    # Hard-coded sample chat data
    chat_data = {
        "conversation": {
            "converation_id": chat_id,
            "title": "My Chat Conversation",
            "created_at": "2023-02-20T14:30:00Z"
        },
        "history": [
            {
                "message_id": "551e87f4-1cfa-49a4-8f4d-65c7a6f23e9a",
                "user": "936da01f-9abd-4d9d-80c7-02af85c822a8",
                "timestamp": "2023-02-20T14:30:05Z",
                "body": "Hello, how are you?"
            },
            {
                "message_id": "2f3a4c21-5b6d-49f2-83c5-1234567890ab",
                "user": "LLM",
                "timestamp": "2023-02-20T14:30:10Z",
                "body": "Hello! I'm doing well, thanks for asking. How can I assist you today?"
            },
            {
                "message_id": "8a3b2c11-4d5e-6f7g-8h9i-0123456789cd",
                "user": "936da01f-9abd-4d9d-80c7-02af85c822a8",
                "timestamp": "2023-02-20T14:30:15Z",
                "body": "I'm looking for information on AI and machine learning."
            },
            {
                "message_id": "4e5f6g7h-8i9j-1k2l-3m4n-0123456789ef",
                "user": "LLM",
                "timestamp": "2023-02-20T14:30:20Z",
                "body": "Fascinating topics! I can provide you with an overview of AI and ML, as well as some resources to get you started."
            }
        ] 
    }

    return jsonify(chat_data)

# Converse with the LLM
@app.route("/chat/<chat_id>/converse", methods=["POST"])
def converse(chat_id):
    # Get user input from request body
    user_input = request.get_json()
    user_id = user_input["user_id"]
    message_body = user_input["message"]["body"]

    # message_doc = {
    #     "chat_id": chat_id,
    #     "message_id": "551e87f4-1cfa-49a4-8f4d-65c7a6f23e9a",
    #     "user": "936da01f-9abd-4d9d-80c7-02af85c822a8",
    #     "timestamp": datetime.datetime.now(),
    #     "body": message_body
    # }

    # db_chroma.insert("messages", message_doc)

    # Generate response from LLM
    response = llm.invoke(message_body)

    # Create a new message object
    message_id = uuid.uuid4()
    timestamp = datetime.datetime.now().isoformat()
    message = {
        "message_id": str(message_id),
        "user": "LLM",
        "timestamp": timestamp,
        "body": response
    }

    # Add message to chat history
    #db.add_message_to_chat(chat_id, message)

    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
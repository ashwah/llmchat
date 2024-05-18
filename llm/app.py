from flask import Flask, request, jsonify
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
import uuid
import datetime

app = Flask(__name__)

# Set up Ollama LLM and embeddings
ollama_url = "http://ollama:11434"
llm = Ollama(base_url=ollama_url, model="phi3")
ollama_embed = OllamaEmbeddings(base_url=ollama_url, model="nomic-embed-text")

# Set up Chroma database
db = Chroma(persist_directory="./chroma_db", embedding_function=ollama_embed)

# Load chat data
@app.route("/chat/<chat_id>/load", methods=["GET"])
def load_chat(chat_id):
    # Hard-coded sample chat data
    chat_data = {
        "title": "Sample Chat",
        "created_at": "2023-05-17T12:00:00Z",
        "history": [
            {
                "message_id": str(uuid.uuid4()),
                "user": "user",
                "timestamp": "2023-05-17T12:00:00Z",
                "body": "Hello, how are you?"
            },
            {
                "message_id": str(uuid.uuid4()),
                "user": "LLM",
                "timestamp": "2023-05-17T12:01:00Z",
                "body": "I'm fine, thank you! How can I assist you today?"
            }
        ]
    }

    return jsonify({
        "conversation": {
            "conversation_id": chat_id,
            "title": chat_data["title"],
            "created_at": chat_data["created_at"]
        },
        "history": chat_data["history"]
    })

# Converse with the LLM
@app.route("/chat/<chat_id>/converse", methods=["POST"])
def converse(chat_id):
    # Get user input from request body
    user_input = request.get_json()
    user_id = user_input["user_id"]
    message_body = user_input["message"]["body"]

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
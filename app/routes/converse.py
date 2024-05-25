from flask import request, jsonify
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.llms import Ollama

import datetime
import uuid

# Set up Ollama LLM and embeddings
ollama_url = "http://localhost:11434"
llm = Ollama(base_url=ollama_url, model="phi3")

# Connection string for the SQLite database.
connection_string = f"sqlite:///C:/Users/ashwa/Documents/VS Code/BBros/chroma/chroma.sqlite3"

def converse(chat_id):
    # Create a SQL chat message history object based on the current chat ID.
    chat_message_history = SQLChatMessageHistory(
        session_id=chat_id, connection_string=connection_string
    )

    memory = ConversationBufferMemory(
        chat_memory=chat_message_history,
        return_messages=True,
    )

    conversation = ConversationChain(
        llm=llm,
        memory=memory
    )

    #history = conversation.memory.load_memory_variables(inputs=[])['history']
    #print(history)

    # Get user input from request body
    user_input = request.get_json()
    user_id = user_input["user_id"]
    message_body = user_input["message"]["body"]

    # Converse with the LLM
    response = conversation.invoke(message_body)

    # Create a new message object
    message_id = uuid.uuid4()
    timestamp = datetime.datetime.now().isoformat()
    message = {
        "message_id": str(message_id),
        "user": "LLM",
        "timestamp": timestamp,
        "body": response['response']
    }

    return jsonify(message)
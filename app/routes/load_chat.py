from flask import jsonify

from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage

import json

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

    # Connection string for the SQLite database.
    connection_string = f"sqlite:///C:/Users/ashwa/Documents/VS Code/BBros/chroma/chroma.sqlite3"

    # Create a SQL chat message history object based on the current chat ID.
    chat_message_history = SQLChatMessageHistory(
        session_id=chat_id, 
        connection_string=connection_string,
    )

    # Get the messages from the chat message history.
    for message in chat_message_history.messages:

        if isinstance(message, HumanMessage):
            user = message.name
            body = message.content


        if isinstance(message, AIMessage):
            user = "AI-Guy"
            data = json.loads(message.content)
            body = data["response"]

        new_message = {
            "message_id": "123456",
            "timestamp": "654321",
            "user": user,
            "body": body
        }

        chat_data["history"].append(new_message)


    return jsonify(chat_data)
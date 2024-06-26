from flask import request, jsonify
from langchain.chains import ConversationChain
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.llms import Ollama
from langchain_core.messages import AIMessage, HumanMessage
from langchain.prompts import PromptTemplate
from multiperson_buffer import MultipersonConversationBufferMemory

import json
import datetime
import uuid

# Set up Ollama LLM and embeddings
ollama_url = "http://localhost:11434"
llm = Ollama(base_url=ollama_url, model="llama3")

# Connection string for the SQLite database.
connection_string = f"sqlite:///C:/Users/ashwa/Documents/VS Code/BBros/chroma/chroma.sqlite3"

def process_new_message(chat_id, user_id, message_body):
        # Create a SQL chat message history object based on the current chat ID.
    chat_message_history = SQLChatMessageHistory(
        session_id=chat_id, 
        connection_string=connection_string,
    )

    memory = MultipersonConversationBufferMemory(
        chat_memory=chat_message_history,
        return_messages=True,
        name=user_id,
    )

    # Set the user ID as the "name" in the memory object.
    memory.set_name(user_id)

    prompt = PromptTemplate.from_template(
        """
        This is a multiple participant chat between multiple humans and an LLM. It is critical you 
        evaluate the most recent human input below and decide whether or not your response is needed. 
        ONLY RESPOND with a non empty response if the humans address you directly as "AI-Guy".
        Sometimes the human participants talk to each other, if they are, you must give an empty response.
        
        If you decide a response from the AI is relevant, please respond with concise, short answers.

        You are also provided with the current conversation history below. Please use this to inform your response, 
        including questions about who is in the chat.
        
        An empty response must look like:
        
        {{ 
            "response": "",
            "info": "This is a place to put any info e.g. an explanation why you didn't response." 
        }}

        And a regular JSON response should look like:

        {{ 
            "response": "This is my response.",
            "info": "This is a place to put any additional info."  
        }}
        
        Current conversation:
        {history}
        
        Human ({user_id}): {input}
        """
    )

    # Fill in the prompt with the user ID.
    prompt = prompt.partial(user_id=user_id)

    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
    )

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

def load_chat_from_database(chat_id):
    # Prepare the chat data to be returned.
    chat_data = {
        "conversation": {
            "converation_id": chat_id,
            "title": "My Chat Conversation",
            "created_at": "123123123"
        },
        "history": [] 
    }

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
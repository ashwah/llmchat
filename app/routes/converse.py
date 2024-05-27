from flask import request, jsonify
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from multiperson_buffer import MultipersonConversationBufferMemory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.llms import Ollama

import datetime
import uuid

# Set up Ollama LLM and embeddings
ollama_url = "http://localhost:11434"
llm = Ollama(base_url=ollama_url, model="llama3")

# Connection string for the SQLite database.
connection_string = f"sqlite:///C:/Users/ashwa/Documents/VS Code/BBros/chroma/chroma.sqlite3"

def converse(chat_id):
    # history = conversation.memory.load_memory_variables(inputs=[])['history']

    # Get user input from request body
    user_input = request.get_json()
    user_id = user_input["user_id"]
    message_body = user_input["message"]["body"]

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
        
        Human ("""
        + user_id +
        """) : {input}
        """
    )

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
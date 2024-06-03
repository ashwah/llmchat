from flask import request
from src.conversation_manager import process_new_message

def converse(chat_id):
    # Get user input from request body
    user_input = request.get_json()
    user_id = user_input["user_id"]
    message_body = user_input["message"]["body"]

    # Process the new message
    return process_new_message(chat_id, user_id, message_body)
from flask import Flask, request
from src.conversation_manager import load_chat, process_new_message

app = Flask(__name__)

@app.route("/chat/<chat_id>/load", methods=["GET"])
def load_chat_route(chat_id):
    return load_chat(chat_id)

@app.route("/chat/<chat_id>/converse", methods=["POST"])
def converse_route(chat_id):
    # Get user input from request body
    user_input = request.get_json()
    user_id = user_input["user_id"]
    message_body = user_input["message"]["body"]

    # Process the new message
    return process_new_message(chat_id, user_id, message_body)

if __name__ == "__main__":
    app.run(debug=True)
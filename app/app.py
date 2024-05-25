from flask import Flask, request, jsonify
from routes import load_chat, converse

app = Flask(__name__)

@app.route("/chat/<chat_id>/load", methods=["GET"])
def load_chat_route(chat_id):
    return load_chat.load_chat(chat_id)

@app.route("/chat/<chat_id>/converse", methods=["POST"])
def converse_route(chat_id):
    return converse.converse(chat_id)

if __name__ == "__main__":
    app.run(debug=True)
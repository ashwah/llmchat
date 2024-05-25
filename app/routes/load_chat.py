from flask import jsonify

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
import json
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class DatabaseError(Exception):
    """Custom exception for database errors."""
    pass


def init_db():
    account_key_str = os.environ.get("accountKey")
    if account_key_str:
        try:
            account_key_dict = json.loads(account_key_str)
            cred = credentials.Certificate(account_key_dict)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON in 'accountKey' environment variable.") from e
    else:
        cred = credentials.Certificate("serviceAccountKey.json")

    firebase_admin.initialize_app(cred)

def get_db():
    return firestore.client()

def save_chat(session_id: str, messages: [str]):
    db = get_db()
    chats = db.collection("chats")
    chats.document(session_id).set({"messages": messages})

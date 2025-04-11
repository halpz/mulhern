import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response

session_store = {}

class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get session ID from cookie
        session_id = request.cookies.get("session_id")
        if not session_id:
            session_id = str(uuid.uuid4())

        # Get or create session data
        session_data = session_store.setdefault(session_id, {})

        # Attach to request
        request.state.session_id = session_id
        request.state.session = session_data

        # Call actual route handler
        response: Response = await call_next(request)

        # Set cookie if it's new
        if "session_id" not in request.cookies:
            response.set_cookie("session_id", session_id)

        return response


def get_messages(request: Request):
    return request.state.session.get("chat", [])

def add_message(request: Request, message: str):
    chat = request.state.session.setdefault("chat", [])
    chat.append(message)

def get_last_response_id(request: Request):
    return request.state.session.get("lastResponseId", None)

def set_last_response_id(request: Request, last_id: str):
    request.state.session["lastResponseId"] = last_id


def start_new_session(request: Request, response: Response):
    new_session_id = str(uuid.uuid4())
    session_store[new_session_id] = {}

    request.state.session_id = new_session_id
    request.state.session = session_store[new_session_id]

    response.set_cookie("session_id", new_session_id)
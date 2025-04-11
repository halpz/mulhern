import os
from fastapi import FastAPI
from openai import OpenAI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from database import save_chat, init_db
from session import SessionMiddleware, get_messages, get_last_response_id, add_message, set_last_response_id, start_new_session

app = FastAPI()

# noinspection PyTypeChecker
app.add_middleware(SessionMiddleware)

templates = Jinja2Templates(directory="templates")
app.mount("/resources", StaticFiles(directory="resources"), name="resources")
app.mount("/css", StaticFiles(directory="css"), name="css")


init_db()

if os.environ.get("OPENAI_API_KEY"):
    openai_client = OpenAI()
else:
    with open("apikey.txt") as f:
        key = f.read().strip()
        openai_client = OpenAI(api_key=key)


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("resources/favicon.ico")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    messages = get_messages(request)
    return templates.TemplateResponse("mulhern.html", {"request": request, "messages": messages})

@app.post("/send")
async def send(request: Request):
    data = await request.json()
    message = data.get("message", "")
    reply = prompt(request, message, get_last_response_id(request))
    return {"reply": reply}

@app.post("/clear")
def clear_chat(request: Request):
    response = RedirectResponse(url="/", status_code=303)
    start_new_session(request, response)
    return response

def prompt(request: Request, prompt_text: str, prev: str | None = None):
    add_message(request, "You: "+prompt_text)
    request_kwargs = {
        "model": "gpt-3.5-turbo",
        "instructions": "You are Stephen Mulhern from ITV. Please answer as if you are him. you are a very cheeky and mischievous man who is always trying to play tricks and pranks on people. You are talking on an online chat website made specifically for fans to speak to you. You made this website yourself and you are very proud of it.",
        "input": prompt_text,
    }

    if prev:
        request_kwargs["previous_response_id"] = prev

    response = openai_client.responses.create(**request_kwargs)

    add_message(request, "Stephen: "+response.output_text)
    set_last_response_id(request, response.id)

    session_id = request.state.session_id
    messages = get_messages(request)
    save_chat(session_id, messages)

    return response.output_text

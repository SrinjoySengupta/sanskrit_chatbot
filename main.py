from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
from difflib import SequenceMatcher
import os

# Load Gita dataset
DATA_FILE = "data/gita_dataset.csv"
df = pd.read_csv(DATA_FILE)

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# Utility: Find best matching line from dataset
def find_best_match(query):
    best_score = 0
    best_row = None
    for _, row in df.iterrows():
        score = SequenceMatcher(None, query.lower(), row['english'].lower()).ratio()
        if score > best_score:
            best_score = score
            best_row = row
    if best_row is not None:
        return {
            "sanskrit": best_row['sanskrit'],
            "english": best_row['english'],
            "similarity_score": round(best_score, 4)
        }
    return None


# Routes
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # Simple fake authentication
    if username and password:
        return RedirectResponse(url="/chatbot", status_code=303)
    return RedirectResponse(url="/", status_code=303)


@app.get("/chatbot", response_class=HTMLResponse)
async def chatbot_page(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    query = data.get("query", "")
    if not query.strip():
        return JSONResponse({"error": "Empty query"}, status_code=400)

    match = find_best_match(query)
    if match:
        return JSONResponse(match)
    else:
        return JSONResponse({"sanskrit": "N/A", "english": "No match found", "similarity_score": 0})

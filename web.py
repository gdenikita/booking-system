from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import aiosqlite
from database import get_all_bookings, init_db
import asyncio

app = FastAPI(title="Booking Panel")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    bookings = await get_all_bookings()
    return templates.TemplateResponse("index.html", {"request": request, "bookings": bookings})

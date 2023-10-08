from dotenv import load_dotenv
from fastapi import FastAPI

from hooks import shutdown, startup
from router import router

load_dotenv()

app = FastAPI()

app.include_router(router, tags=["Student"], prefix="/students")
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

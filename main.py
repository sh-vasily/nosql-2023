from dotenv import load_dotenv
from fastapi import FastAPI

from db import connect_and_init_db, close_db_connect
from router import router

load_dotenv()

app = FastAPI()

app.include_router(router, tags=["Student"], prefix="/students")
app.add_event_handler("startup", connect_and_init_db)
app.add_event_handler("shutdown", close_db_connect)

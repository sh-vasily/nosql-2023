from fastapi import FastAPI

from handler.event_handlers import startup, shutdown
from router.students_router import router

app = FastAPI()

app.include_router(router, tags=["Student"], prefix="/api/students")
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

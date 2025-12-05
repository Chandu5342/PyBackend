# main.py
from fastapi import FastAPI
from routers.tasks import router as tasks_router
app = FastAPI()
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
@app.get("/")
def read_root():
    return {"message": "Task Manager API is up"}

import os
from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI
from pydantic import BaseModel, Field


def get_conn():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    with get_conn() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS tasks ("
            "id SERIAL PRIMARY KEY, "
            "title TEXT NOT NULL, "
            "done BOOLEAN NOT NULL DEFAULT FALSE)"
        )
    yield


app = FastAPI(title="Taskboard API", lifespan=lifespan)


class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, title, done FROM tasks ORDER BY id"
        ).fetchall()
    return [{"id": r[0], "title": r[1], "done": r[2]} for r in rows]


@app.post("/tasks", status_code=201)
def create_task(task: TaskIn):
    with get_conn() as conn:
        r = conn.execute(
            "INSERT INTO tasks (title) VALUES (%s) RETURNING id, title, done",
            (task.title,),
        ).fetchone()
    return {"id": r[0], "title": r[1], "done": r[2]}

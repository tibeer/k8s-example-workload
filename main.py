import os
import psycopg

from fastapi import FastAPI
from loguru import logger
from uuid import uuid4


def get_note(conn, id) -> tuple:
    with conn.cursor() as cur:
        cur.execute(f"SELECT id, note_content FROM notes WHERE id = '{id}'")
        note = cur.fetchone()
    if not note:
        return ()
    return note


def get_notes(conn) -> list:
    notes = []
    with conn.cursor() as cur:
        for row in cur.execute("SELECT id, note_content FROM notes"):
            notes.append(row)
    return notes


def create_note(conn, note_content) -> str:
    id = str(uuid4())
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO notes (id, note_content) VALUES ('{id}', '{note_content}')")
        logger.debug(f"status message: {cur.statusmessage}")
    return id


def delete_note(conn, id) -> None:
    with conn.cursor() as cur:
        cur.execute(f"DELETE FROM notes WHERE id = '{id}'")
        logger.debug(f"status message: {cur.statusmessage}")


##########################################


app = FastAPI()

uri = "postgresql://root@127.0.0.1:26257/defaultdb?sslmode=disable"
uri = os.getenv("DB_CONNECTION_URI", uri)
try:
    conn = psycopg.connect(
        uri,
        application_name="$ docs_simplecrud_psycopg3",
        row_factory=psycopg.rows.namedtuple_row
    )
except Exception as e:
    logger.critical("database connection failed")
    logger.critical(e)
    exit()


@app.on_event("startup")
def db_setup():
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS notes (id UUID PRIMARY KEY, note_content TEXT)")


@app.get("/notes/{note_id}")
async def fapi_get_note(note_id: str) -> tuple:
    return get_note(conn, note_id)


@app.get("/notes/")
async def fapi_get_notes() -> list:
    return get_notes(conn)


@app.post("/notes/")
async def fapi_create_note(note_content: str) -> str:
    return create_note(conn, note_content)


@app.delete("/notes/{note_id}")
async def fapi_delete_note(note_id: str) -> None:
    delete_note(conn, note_id)

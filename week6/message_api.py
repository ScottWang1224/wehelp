from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from config import SESSION_SECRET_KEY
from database import get_database_connection

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)


@app.get("/api/message")
async def get_messages(request: Request):
    member = request.session.get("member")

    if member is None:
        return {"error": True}

    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                message.id,
                message.member_id,
                member.name,
                message.content
            FROM message
            INNER JOIN member
            ON message.member_id = member.id
            ORDER BY message.id
        """

        cursor.execute(query)
        messages = cursor.fetchall()

        data = []

        for message in messages:
            data.append(
                {
                    "id": message["id"],
                    "name": message["name"],
                    "content": message["content"],
                    "self": message["member_id"] == member["id"],
                }
            )

        return {
            "ok": True,
            "data": data,
        }

    except Exception as error:
        print(f"Get messages error: {error}")
        return {"error": True}

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


@app.post("/api/message")
async def create_message(request: Request):
    member = request.session.get("member")

    if member is None:
        return {"error": True}

    connection = None
    cursor = None

    try:
        body = await request.json()
        content = body.get("content", "").strip()

        if not content:
            return {"error": True}

        connection = get_database_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO message (member_id, content)
            VALUES (%s, %s)
        """

        cursor.execute(
            query,
            (member["id"], content),
        )

        connection.commit()

        return {"ok": True}

    except Exception as error:
        print(f"Create message error: {error}")

        if connection:
            connection.rollback()

        return {"error": True}

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


@app.delete("/api/message/{message_id}")
async def delete_message(message_id: int, request: Request):
    member = request.session.get("member")

    if member is None:
        return {"error": True}

    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM message
            WHERE id = %s AND member_id = %s
        """

        cursor.execute(
            query,
            (message_id, member["id"]),
        )

        connection.commit()

        if cursor.rowcount == 0:
            return {"error": True}

        return {"ok": True}

    except Exception as error:
        print(f"Delete message error: {error}")

        if connection:
            connection.rollback()

        return {"error": True}

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

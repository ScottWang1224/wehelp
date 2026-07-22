from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastmcp import FastMCP
from fastmcp.dependencies import CurrentHeaders

import hashlib
import secrets

from config import SESSION_SECRET_KEY
from database import get_database_connection

mcp = FastMCP("Testing Message Website")
mcp_app = mcp.http_app(path="/")

app = FastAPI(lifespan=mcp_app.lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@mcp.tool(
    name="create_message",
    description="Create a new message in Testing Message Website.",
)
async def create_message_tool(
    content: str,
    headers: dict = CurrentHeaders(),
) -> dict:
    connection = None
    cursor = None

    try:
        content = content.strip()

        if not content:
            return {"error": True}

        authorization = headers.get("authorization", "")

        if not authorization.startswith("Bearer "):
            return {"error": True}

        token = authorization.removeprefix("Bearer ").strip()

        if not token:
            return {"error": True}

        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        member_query = """
            SELECT id
            FROM member
            WHERE token = %s
        """

        cursor.execute(member_query, (token,))
        member = cursor.fetchone()

        if member is None:
            return {"error": True}

        message_query = """
            INSERT INTO message (member_id, content)
            VALUES (%s, %s)
        """

        cursor.execute(
            message_query,
            (member["id"], content),
        )

        connection.commit()

        return {"ok": True}

    except Exception as error:
        print(f"MCP create message error: {error}")

        if connection:
            connection.rollback()

        return {"error": True}

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


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


@app.put("/api/token")
async def create_token(request: Request):
    member = request.session.get("member")

    if member is None:
        return {"error": True}

    connection = None
    cursor = None

    try:
        # 產生隨機字串，再轉成固定 64 字元的 SHA256 Token
        random_value = secrets.token_hex(32)

        token = hashlib.sha256(random_value.encode("utf-8")).hexdigest()

        connection = get_database_connection()
        cursor = connection.cursor()

        query = """
            UPDATE member
            SET token = %s
            WHERE id = %s
        """

        cursor.execute(
            query,
            (token, member["id"]),
        )

        connection.commit()

        if cursor.rowcount == 0:
            return {"error": True}

        return {
            "ok": True,
            "token": token,
        }

    except Exception as error:
        print(f"Create token error: {error}")

        if connection:
            connection.rollback()

        return {"error": True}

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


app.mount("/mcp", mcp_app)

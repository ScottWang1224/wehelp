from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import get_database_connection
from starlette.middleware.sessions import SessionMiddleware

from config import SESSION_SECRET_KEY

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get("/member", response_class=HTMLResponse)
async def member_page(request: Request):
    member = request.session.get("member")

    if member is None:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="member.html",
        context={
            "member": member,
        },
    )


@app.get("/ohoh", response_class=HTMLResponse)
async def error_page(request: Request, msg: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "message": msg,
        },
    )


@app.post("/signup")
async def signup(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        check_query = """
            SELECT id
            FROM member
            WHERE email = %s
        """

        cursor.execute(check_query, (email,))
        existing_member = cursor.fetchone()

        if existing_member:
            return RedirectResponse(
                url="/ohoh?msg=重複的電子郵件",
                status_code=303,
            )

        insert_query = """
            INSERT INTO member (name, email, password)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (name, email, password),
        )

        connection.commit()

        return RedirectResponse(
            url="/",
            status_code=303,
        )

    except Exception as error:
        print(f"Signup error: {error}")

        if connection:
            connection.rollback()

        return RedirectResponse(
            url="/ohoh?msg=註冊失敗",
            status_code=303,
        )

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    connection = None
    cursor = None

    try:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT id, name, email
            FROM member
            WHERE email = %s AND password = %s
        """

        cursor.execute(query, (email, password))
        member = cursor.fetchone()

        if member is None:
            return RedirectResponse(
                url="/ohoh?msg=電子郵件或密碼錯誤",
                status_code=303,
            )

        request.session["member"] = {
            "id": member["id"],
            "name": member["name"],
            "email": member["email"],
        }

        return RedirectResponse(
            url="/member",
            status_code=303,
        )

    except Exception as error:
        print(f"Login error: {error}")

        return RedirectResponse(
            url="/ohoh?msg=登入失敗",
            status_code=303,
        )

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=303,
    )

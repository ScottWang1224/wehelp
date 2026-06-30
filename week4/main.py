from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from urllib.request import urlopen
import json

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.post("/login")
async def login(
    request: Request, email: str = Form(default=""), password: str = Form(default="")
):
    if email == "" or password == "":
        return RedirectResponse(url="/ohoh?msg=請輸入帳號、密碼", status_code=303)
    if email == "abc@abc.com" and password == "abc":
        request.session["logged_in"] = True
        return RedirectResponse(url="/member", status_code=303)

    return RedirectResponse(url="/ohoh?msg=帳號、或密碼輸入錯誤", status_code=303)


@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    if not request.session.get("logged_in"):
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(request=request, name="member.html", context={})


@app.get("/ohoh", response_class=HTMLResponse)
async def error(request: Request, msg: str = ""):
    return templates.TemplateResponse(
        request=request, name="error.html", context={"msg": msg}
    )


@app.get("/logout")
async def logout(request: Request):
    request.session["logged_in"] = False
    return RedirectResponse(url="/", status_code=303)


url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
url_en = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"


def get_hotels():
    response = urlopen(url)
    data = json.load(response)
    hotels = data["list"]

    response_en = urlopen(url_en)
    data_en = json.load(response_en)
    hotels_en = data_en["list"]

    english_hotels = {}

    for hotel in hotels_en:
        hotel_id = hotel["_id"]
        english_hotels[hotel_id] = hotel

    merged_hotels = {}

    for hotel in hotels:
        hotel_id = hotel["_id"]

        en_hotel = english_hotels.get(hotel_id)

        if en_hotel:
            merged_hotels[hotel_id] = {
                "chinese_name": hotel["旅宿名稱"],
                "english_name": en_hotel["hotel name"],
                "phone": hotel["電話或手機號碼"],
            }

    return merged_hotels


hotels = get_hotels()


@app.get("/hotel/{hotel_id}", response_class=HTMLResponse)
async def hotel(request: Request, hotel_id: int):
    hotel_data = hotels.get(hotel_id)

    return templates.TemplateResponse(
        request=request, name="hotel.html", context={"hotel": hotel_data}
    )

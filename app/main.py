import os

from fastapi import FastAPI, Request, Form, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from api.newPostUpload import add_post_to_json
from api.getPostsList import get_posts_from_json
from api.getPostById import get_post_by_id

from pathlib import Path

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "./static"),
    name= "static"
)

templates = Jinja2Templates(directory="../templates")



@app.get("/")
async def mainPage(request: Request):
    mainTitle = "Hello"
    mainText = "lololol"


    return templates.TemplateResponse(
        "mainPage.html", 
        {"request": request, 
         "MainTitle": mainTitle, 
         "MainText": mainText}
        )

@app.get("/postUploadPage")
async def postUploadPage(request: Request):
    return templates.TemplateResponse("postUploadPage.html", {"request": request})


@app.post("/postUpload", response_class=HTMLResponse)
async def postUpload(request: Request, writer: str = Form(...), title: str = Form(...), content: str = Form(...)):

    add_post_to_json("./db/post_data.json", writer, title, content)
    return templates.TemplateResponse("postUploadCompletedPage.html", {"request": request, "title": title, "content": content})


@app.get("/community")
async def communityPage(request: Request):

    posts = get_posts_from_json("./db/post_data.json")

    return templates.TemplateResponse("communityPage.html", {"request": request, "posts": posts})


@app.get("/post/{post_id}", response_class=HTMLResponse)
def read_post(request: Request, post_id: str):
    post = get_post_by_id(post_id)
    if post:
        return templates.TemplateResponse("postDetail.html", {"request": request, "post": post})
    else:
        return {"message": "게시물을 찾을 수 없습니다."}

# uvicorn main:app --reload
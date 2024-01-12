import os

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.api.newPostUpload import add_post_to_json
from app.api.getPostsList import get_posts_from_json
from app.api.getPostById import get_post_by_id
from app.api.modifyPostById import modify_post_by_time
from app.api.deletePostById import delete_post_by_time

from pathlib import Path

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="./static"),
    name="static"
)

templates = Jinja2Templates(directory="./templates")



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
async def postUpload(request: Request, writer: str = Form(...), title: str = Form(...), content: str = Form(...), password: str = Form(...)):

    add_post_to_json("./app/db/post_data.json", writer, title, content, password)
    return templates.TemplateResponse("postUploadCompletedPage.html", {"request": request, "messageTitle": "게시글 작성 완료!", "messageContent": "게시글 작성이 완료되었습니다."})


@app.get("/community")
async def communityPage(request: Request):

    posts = get_posts_from_json("./app/db/post_data.json")

    return templates.TemplateResponse("communityPage.html", {"request": request, "posts": posts})


@app.get("/post/{post_id}", response_class=HTMLResponse)
def read_post(request: Request, post_id: str):
    post = get_post_by_id(post_id)
    if post:
        return templates.TemplateResponse("postDetail.html", {"request": request, "post": post})
    else:
        return templates.TemplateResponse("postDetail.html", {"request": request, "post": {"message": "게시물을 찾을 수 없습니다."}})

@app.get("/postModify/{post_id}", response_class=HTMLResponse)
def postModify(request: Request, post_id: str):
    post = get_post_by_id(post_id)
    return templates.TemplateResponse("postModifyPage.html", {"request": request, "post": post})

@app.post("/postUpdate/{post_id}", response_class=HTMLResponse)
def postUpdate(request: Request, post_id: str, writer: str = Form(...), title: str = Form(...), content: str = Form(...), password: str = Form(...)):

    modify_post_by_time("./app/db/post_data.json", post_id, title, content)

    return templates.TemplateResponse("postUploadCompletedPage.html", {"request": request, "messageTitle": "게시글 수정 완료!", "messageContent": "게시글 수정이 완료되었습니다."})

@app.get("/postDelete/{post_id}/{post_password}", response_class=HTMLResponse)

async def postDeletePage(request: Request, post_id: str, post_password: str):

    return templates.TemplateResponse("postDeletePage.html", {"request": request, "post_id": post_id, "post_password": post_password})

@app.post("/postDeleteRR/{post_password}", response_class=HTMLResponse)
async def postDeleteRR(request: Request, post_password: str, post_id: str = Form(...), password: str = Form(...)):
    if post_password == password:
        delete_post_by_time("./app/db/post_data.json", post_id)
        return templates.TemplateResponse("postUploadCompletedPage.html", {"request": request, "messageTitle": "게시물 삭제!", "messageContent": "게시물이 삭제되었습니다. 더이상 해당 게시물을 복구 할 수 없습니다."})
    else:
        return templates.TemplateResponse("postUploadCompletedPage.html", {"request": request, "messageTitle": "게시물 삭제 실패!", "messageContent": "예상하지 못한 이유로 게시물 삭제를 실패하였습니다. 예) 올바르지 않은 비밀번호 입력."})

# uvicorn main:app --reload
from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/")
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}")
def get_user(request: Request, user_id: int) -> HTMLResponse:
    try:
        for user in users:
            if user.id == user_id:
                return templates.TemplateResponse("users.html", {"request": request, "user": user})
        raise HTTPException(status_code=404, detail=f"User ID={user_id} was not found")
    except IndexError:
        raise HTTPException(status_code=404, detail=f"User ID={user_id} was not found")


@app.post("/user/{username}/{age}")
def create_user(user: User) -> User:
    user.id = len(users)
    users.append(user)
    return user


@app.put("/user/{user_id}/{username}/{age}")
def update_user(user: User) -> User:
    try:
        for current_user in users:
            if current_user.id == user.id:
                users[users.index(current_user)] = user
                return user
        raise HTTPException(status_code=404, detail=f"User ID={user.id} was not found")
    except IndexError:
        raise HTTPException(status_code=404, detail=f"User ID={user.id} was not found")


@app.delete("/delete/{user_id}")
def delete_user(user_id: int) -> User:
    try:
        for current_user in users:
            if current_user.id == user_id:
                users.remove(current_user)
                return current_user
        raise HTTPException(status_code=404, detail=f"User ID={user_id} was not found")
    except IndexError:
        raise HTTPException(status_code=404, detail=f"User ID={user_id} was not found")

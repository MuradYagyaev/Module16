from fastapi import FastAPI, status, Body, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/users")
def get_all_users() -> List[User]:
    return users

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


@app.delete("/user/{user_id}")
def delete_user(user_id: int) -> User:
    try:
        for current_user in users:
            if current_user.id == user_id:
                users.remove(current_user)
                return current_user
        raise HTTPException(status_code=404, detail=f"User ID={user_id} was not found")
    except IndexError:
        raise HTTPException(status_code=404, detail=f"User ID={user_id} was not found")

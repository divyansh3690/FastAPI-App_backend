import sys
sys.path.append("..")
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
import model
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from router.auth import get_current_user, get_user_exception

router=APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}}
)
model.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class ui_posts(BaseModel):
    title: str
    description: Optional[str]
    is_archived: int


@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(model.Posts).all()


@router.get("/byuser")
async def read_by_user(db: Session = Depends((get_db)), user: dict = Depends(get_current_user)):
    if not user:
        raise get_user_exception
    return db.query(model.Posts).filter(model.Posts.user_id == user.get("id")).all()


@router.post("/")
async def create_todo(posts: ui_posts,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    post_model = model.Posts()
    post_model.title = posts.title
    post_model.description = posts.description
    post_model.is_archived = posts.is_archived
    post_model.user_id = user.get("id")

    db.add(post_model)
    db.commit()

    return successful_response(201)


@router.put("/{postid}")
async def update_todo(postid: int,
                      post: ui_posts,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    post_model = db.query(model.Posts) \
        .filter(model.Posts.id == postid) \
        .filter(model.Posts.user_id == user.get("id")) \
        .first()

    if post_model is None:
        raise http_exception()

    post_model.title = post.title
    post_model.description = post.description
    post_model.is_archived = post.is_archived

    db.add(post_model)
    db.commit()

    return successful_response(200)


@router.delete("/{post_id}")
async def delete_todo(post_id: int,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    todo_model = db.query(model.Posts) \
        .filter(model.Posts.id == post_id) \
        .filter(model.Posts.user_id == user.get("id")) \
        .first()

    if todo_model is None:
        raise http_exception()

    db.query(model.Posts) \
        .filter(model.Posts.id == post_id) \
        .delete()

    db.commit()

    return successful_response(200)


def http_exception():
    return HTTPException(status_code=404, detail="Post not found")


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }

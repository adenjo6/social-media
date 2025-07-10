from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import SessionLocal, engine, get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model= List[schemas.PostOut] )
def get_posts(db: Session = Depends(get_db),curr_user : int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]= ""):
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts
    # return [{"post": post, "votes": votes} for post, votes in posts] 
 

@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    # Raw SQL approach:
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    # post = cursor.fetchone()
    
    # SQLAlchemy ORM approach:
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")
    return post 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post )
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):
    # Raw SQL approach:
    # cursor.execute(
    #     """ 
    #     INSERT INTO posts (title,content,published) 
    #      VALUES (%s,%s,%s) RETURNING *
    #     """, 
    #     (post.title, post.content, post.published ))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(curr_user.email)
    print(curr_user.id)
    # SQLAlchemy ORM approach:
    new_post = models.Post(owner_id=curr_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post 

@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):
    # Raw SQL approach:
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (update_post.title,update_post.content,update_post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    # SQLAlchemy ORM approach:
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")
    
    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):
    # Raw SQL approach:
    # cursor.execute(""" DELETE FROM posts WHERE id = %s """, (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    # SQLAlchemy ORM approach: 


    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post == None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")
    
    if post.owner_id != curr_user:
        raise HTTPException(status_code=403, detail=f"Not authorized to perform requested action")

    db.delete(post)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)






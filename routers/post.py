import app.models
import app.schemas
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
import app.models
from sqlalchemy import func

import app.oauth as oauth2


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=list[app.schemas.PostOut])
def get_posts(db: Session = Depends(get_db),user_id:int = Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute("SELECT * FROM posts")
    # all_posts = cursor.fetchall()
    # print(all_posts)
    # return {"data": all_posts}
    # print(limit)
    # posts=db.query(app.models.Post).limit(limit).all()
    # posts=db.query(app.models.Post).limit(limit).offset(skip).all()
    # posts=db.query(app.models.Post).filter(app.models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(app.models.Post).all()
    posts=db.query(app.models.Post, func.count(app.models.Vote.post_id).label("votes")).join(app.models.Vote, app.models.Vote.post_id == app.models.Post.id, isouter=True).group_by(app.models.Post.id).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=app.schemas.PostResponse)#dont have seperate schemaas for post in and out having to input owner_id in body will sendingreq
def create_posts(post:app.schemas.PostBase, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data": new_post}    
    new_post = app.models.Post(owner_id=current_user.id,title=post.title, content=post.content, published=post.published)
    # new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}",response_model=app.schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db),user_id:int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # post = cursor.fetchone()
    # post = db.query(app.models.Post).filter(app.models.Post.id == id).first()
    post=db.query(app.models.Post, func.count(app.models.Vote.post_id).label("votes")).join(app.models.Vote, app.models.Vote.post_id == app.models.Post.id, isouter=True).group_by(app.models.Post.id).filter(app.models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
    return post
    

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),current_user= Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query=db.query(app.models.Post).filter(app.models.Post.id==id)
    post=post_query.first()
    
    if post== None:
        raise HTTPException(status_code=404, detail=f"post with id: {id} does not exist")
    if str(post.owner_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authorized to perform request action")
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    


@router.put("/{id}",response_model=app.schemas.PostResponse)
def update_post(id:int, updated_post:app.schemas.PostBase, db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))
    # post_dict = cursor.fetchone()
    # conn.commit()
    post_query = db.query(app.models.Post).filter(app.models.Post.id == id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=404, detail=f"post with id: {id} does not exist")
    if str(post.owner_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authorised to perform request action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


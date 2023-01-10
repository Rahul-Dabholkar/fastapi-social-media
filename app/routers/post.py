from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, utils, oauth2
from typing import Optional
from sqlalchemy import func


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


#-----------------| CREATING A NEW POST |----------------------
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(user_id = current_user.id, **post.dict())  
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#-----------------| RETURNING ALL POSTS |----------------------
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ''):

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # 1.query columns to get | 2.left outer join | 3. group by postid | 4. filter query | 5. limit query
    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes'))\
            .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
            .group_by(models.Post.id)\
            .filter(models.Post.title.contains(search))\
            .limit(limit).offset(skip).all()
    
    return results


#-----------------| RETURNING POST BY ID |----------------------
@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    # 1.query columns to get | 2.left outer join | 3. group by postid | 4. filter by post.id | 6. grabbing first post with that id
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes'))\
            .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
            .group_by(models.Post.id)\
            .filter(models.Post.id == id).first()

    # if post not found (manipulating status code)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'post with id : {id} was not found')

    return post


#-----------------| DELETING POST BY ID |----------------------
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'post with id : {id} does not exist')

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= f'not authorized to perform requested action')           

    post_query.delete(synchronize_session = False) #sync session works the best when deleting
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


#-----------------| UPDATING POST BY ID |----------------------
@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'post with id : {id} does not exist')

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= f'not authorized to perform requested action')     

    post.update(updated_post.dict(), synchronize_session = False)
    db.commit()
    
    return post_query.first()
import app.models
import app.schemas
import app.utils
from fastapi import  status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=app.schemas.UserOut)
def create_user(user: app.schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password =app.utils.hash(user.password)
    user.password = hashed_password
    new_user = app.models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=app.schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(app.models.User).filter(app.models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {id} was not found")
    return user
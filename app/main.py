from fastapi import  FastAPI,HTTPException


import psycopg2
from psycopg2.extras import RealDictCursor
import time




from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from routers import post, user,auth,xvote
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(xvote.router)

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Rishabh@2007', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)
@app.get("/")
def root():
    return {"message": "Hello World"}
my_post = [{"title":"title of post 1","content":"content of post 1", "id": 1},{"title":"title of post 2","content":"content of post 2", "id": 2}]
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#    posts = db.query(models.Post).all()
#    return {"data": posts}

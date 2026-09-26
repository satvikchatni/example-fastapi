from app.schemas import UserOut
from tests.database import client,session
import pytest
from jose import jwt
from app.schemas import Token
from app.config import settings


def test_root(client):
    res=client.get("/")
    print(res.json())
    print(res.json().get('message'))
    assert res.json().get('message')=='Hello World'
    assert res.status_code==200

def test_create_user(client):
    res=client.post("/users",json={"email":"heheh@gmail.com","password":"password123"})
    # assert res.json().get("email")=="heheh@gmail.com"
    new_user=UserOut(**res.json())
    assert new_user.email=="heheh@gmail.com"
    assert res.status_code==201

def test_login_user(client,test_user):
    # res=client.post("/login",data={"username":"heheh@gmail.com","password":"password123"})

    # assert res.status_code==200
    res=client.post("/login",data={"username":test_user['email'],"password":test_user['password']})
    login_res=Token(**res.json())
    payload=jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id=payload.get("user_id")
    assert login_res.token_type=="bearer"
    assert id==test_user['id']
    assert res.status_code==200

@pytest.mark.parametrize("email,password,status_code",[("wrong@gmail.com","Rishabh2007",403),("satvikchatni@gmail.com","wrongpwd",403),("wrong@gmail.com","pwd123wrng",403),(None,"Rishabh2007",422),("satvikchatni@gmail.com",None,422)])
def test_incorrect_login(test_user,client,email,password,status_code):
    res=client.post("/login",data={"username":email,"password":password})
    assert res.status_code==status_code
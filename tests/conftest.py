import pytest
from app.oauth import create_access_token
from tests.database import client,session
from app import models
@pytest.fixture
def test_user(client):
    user_data={"email":"satvikchatni@gmail.com","password":"Rishabh2007"}
    res=client.post("/users/",json=user_data)
    assert res.status_code==201
    print(res.json())
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user
@pytest.fixture
def test_user2(client):
    user_data={"email":"satvikchatni123@gmail.com","password":"Rishabh200740"}
    res=client.post("/users/",json=user_data)
    assert res.status_code==201
    print(res.json())
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    create_access_token({"user_id":test_user['id']})
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client

def create_post_model(post):
    return models.Post(**post)

@pytest.fixture
def test_posts(test_user,session,test_user2):
    posts_data=[{
            "title":"1",
            "content":"1",
            "owner_id":test_user['id']
        },
        
        {
                        "title":"2",
                        "content":"2",
                        "owner_id":test_user['id']
        },
        {
                                "title":"3",
                                "content":"3",
                                "owner_id":test_user['id']
        },
        {
            "title":"4",
            "content":"4",
            "owner_id":test_user2['id']
        }]
    post_map=map(create_post_model,posts_data)
    posts=list(post_map)
    session.add_all(posts)
    session.commit()
    posts=session.query(models.Post).all()
    return posts
    
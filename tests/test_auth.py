from conftest import client
from app.services.user_service import create_user
def test_auth_register_success():
    """注册新用户应该成功"""
    response = client.post("/api/auth/register",json={
        "username": "admin",
        "password": "123456",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "注册成功"
    assert data["username"] == "admin"

def test_auth_register_duplicate():
    """重复用户名应该返回 400"""
    # 先注册一次
    client.post("/api/auth/register",json={
        "username": "dupuser",
        "password": "xyz789",
    })
    # 再注册同名的
    response = client.post("/api/auth/register", json={
        "username": "dupuser",
        "password": "xyz789"
    })
    assert response.status_code == 400
    assert "用户已存在" in response.json()["detail"]

#测试登录成功
def test_auth_login_success():
    #创建用户
    create_user(username="ikun66",password="123456")
    #调用登录接口
    response = client.post("/api/auth/login",json={
        "username": "ikun66",
        "password": "123456"
    })
    data = response.json()
    assert data["message"] == "登录成功"
    assert data["token"]

#测试登录失败
def test_auth_login_false():
    #创建用户
    create_user(username="lk666", password="123456")
    #调用登录接口
    response = client.post("/api/auth/login", json={
        "username": "admin",
        "password": "123457"
    })
    assert response.status_code == 401


from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

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
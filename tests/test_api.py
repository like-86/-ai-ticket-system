from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)
#健康接口测试
def test_root_endpoint():
    """GET / 应该返回应用名称和版本"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_create_knowledge(mock_chromadb):
    """POST /api/knowledge 应该返回 id 和成功消息"""
    response = client.post("/api/knowledge", json={
        "content": "测试知识条目的内容",
        "source": "test"
    })
    assert response.status_code == 200
    assert len(mock_chromadb.add.call_args[1]['ids'])>0
    data = response.json()
    assert "id" in data
    assert data["message"] == "添加成功"
#查询工单测试
def test_list_tickets_empty(mock_chromadb):
      """GET /api/tickets 数据库为空时应该返回空列表"""
      response = client.get("/api/tickets")
      assert response.status_code == 200
      assert response.json() == []
#创建工单测试
def test_list_tickets_with_data(mock_chromadb):
    #直接插入一条数据
    from app.db.database import SessionLocal
    from app.db.models import Ticket
    db_test = SessionLocal()
    ticket = Ticket(title="测试工单",description="测试描述")
    db_test.add(ticket)
    db_test.commit()
    db_test.close()
    #查询列表
    response = client.get("/api/tickets")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] =="测试工单"
    assert data[0]["description"] == "测试描述"

def test_get_ticket_by_id(mock_chromadb):
    #插入一条数据
    from app.db.database import SessionLocal
    from app.db.models import Ticket
    db_test = SessionLocal()
    ticket = Ticket(title="查询测试1",description="测试描述")
    db_test.add(ticket)
    db_test.commit()
    db_test.refresh(ticket)
    db_test.close()
    response = client.get(f"/api/tickets/{ticket.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "查询测试1"
    assert data["description"] == "测试描述"
    assert data["status"] == "pending"

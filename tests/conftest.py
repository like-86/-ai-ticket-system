"""pytest 全局共享配置"""
import pytest
from unittest.mock import MagicMock, patch
import os
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///file::memory:?cache=shared&uri=true"
@pytest.fixture
def mock_chromadb():
    """模拟 ChromaDB 集合，让测试不连真实数据库"""
    mock_collection = MagicMock()
    # 模拟 get() 返回假数据
    mock_collection.get.return_value ={
        "documents": [
            "密码重置方法：在登录页面点击'忘记密码'",
            "退款政策：购买后7天内可申请全额退款",
            "API调用限制：免费用户每小时100次",
        ]
    }
    # 模拟 query() 返回假数据
    def mock_query(query_texts=None, n_results=3):
        """模拟搜索：根据 query 内容决定返回什么"""
        if "密码" in str(query_texts):
            return {"documents": [["密码重置方法：在登录页面点击'忘记密码'"]]}
        # 搜不到就返回空
        return {"documents": [[]]}

    mock_collection.query.side_effect = mock_query
    with patch("app.services.knowledge_base.collection", mock_collection):
        yield mock_collection



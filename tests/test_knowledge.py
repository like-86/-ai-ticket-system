"""测试知识库相关功能"""
from app.services.knowledge_base import chunk_text

def test_chunk_text_default_params():
    """chunk_text 默认参数（size=200, overlap=50）的行为"""
    text = "a"*500
    chunks = chunk_text(text)
    #应该返回4块
    assert len(chunks)==4
    #第一块从0开始，长度200
    assert chunks[0]=="a"*200
    #第二块从150开始，长度200
    assert chunks[1]=="a"*200
    #第三块从300开始，长度200
    assert chunks[2]=="a"*200
    #第四块从450开始，长度50
    assert chunks[3]=="a"*50
def test_chunk_text_short_text():
    """文本小于 chunk_size，应该返回 1 块"""
    assert chunk_text("hello") == ["hello"]

def test_search_knowledge_found(mock_chromadb):
    """搜索关键词 '密码'，应该返回匹配的结果"""
    from app.services.knowledge_base import search_knowledge
    result = search_knowledge("密码")
    assert "密码重置" in result

def test_search_knowledge_not_found(mock_chromadb):
    """搜索不存在的关键词，返回提示语"""
    from app.services.knowledge_base import search_knowledge
    result = search_knowledge("区块链")
    assert result == "未找到相关答案"




"""测试知识库相关功能"""
from app.services.knowledge_base import chunk_text, smart_chunk


# ===== smart_chunk 自然边界切分测试 =====

def test_smart_chunk_short_text():
    """文本短于 chunk_size，直接返回一整块"""
    result = smart_chunk("你好世界", chunk_size=500)
    assert result == ["你好世界"]


def test_smart_chunk_by_paragraph():
    """按段落（\n\n）切分，每段都小于 chunk_size"""
    text = "第一段内容。\n\n第二段内容。\n\n第三段内容。"
    result = smart_chunk(text, chunk_size=100)
    assert result == ["第一段内容。", "第二段内容。", "第三段内容。"]


def test_smart_chunk_by_sentence():
    """段落太长，降级按句号切分"""
    # 一段 300 字，chunk_size=200，应该按句号切成两句
    text = "这是第一句话。这是第二句话。" + "x" * 200 + "。这是第三句话。"
    result = smart_chunk(text, chunk_size=100)
    # 至少切成 2 块以上（不会是一整段）
    assert len(result) >= 2
    # 每块都 <= chunk_size + 一点余量（句号可能跨边界）
    for chunk in result:
        assert len(chunk) <= 150


def test_smart_chunk_no_separator():
    """没有分隔符且超过 chunk_size，保底按字数切"""
    text = "x" * 1000
    result = smart_chunk(text, chunk_size=300)
    # 应该切成至少 3 块（1000/300 ≈ 3.3）
    assert len(result) >= 3
    # 每块不能超过 chunk_size
    for chunk in result:
        assert len(chunk) <= 300


def test_smart_chunk_empty_text():
    """空文本返回空列表"""
    assert smart_chunk("") == []


def test_smart_chunk_mixed_content():
    """混合段落和长句"""
    text = "短段落。\n\n" + "a" * 300 + "。\n\n" + "b" * 100 + "。"
    result = smart_chunk(text, chunk_size=200)
    # 短段落（约5字）直接收
    assert "短段落。" in result
    # 总块数 >= 2
    assert len(result) >= 2
    # 每块不超过 chunk_size + 余量
    for chunk in result:
        assert len(chunk) <= 220


def test_smart_chunk_exact_fit():
    """文本刚好等于 chunk_size，直接返回"""
    text = "x" * 500
    result = smart_chunk(text, chunk_size=500)
    assert result == [text]


# ===== 原 chunk_text 测试保留 =====

def test_chunk_text_default_params():
    """chunk_text 默认参数（size=200, overlap=50）的行为"""
    text = "a" * 500
    chunks = chunk_text(text)
    # 应该返回4块
    assert len(chunks) == 4
    # 第一块从0开始，长度200
    assert chunks[0] == "a" * 200
    # 第二块从150开始，长度200
    assert chunks[1] == "a" * 200
    # 第三块从300开始，长度200
    assert chunks[2] == "a" * 200
    # 第四块从450开始，长度50
    assert chunks[3] == "a" * 50


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
import uuid
import chromadb
#嵌入模型


#chromaDB客户端持久化到文件
chroma_client = chromadb.PersistentClient(path ="./chroma_data")
collection = chroma_client.get_or_create_collection(
    name="knowledge",
)
#知识库数据
documents = [
      {"id": "1", "content":
  "密码重置方法：在登录页面点击'忘记密码'，输入注册邮箱接收重置链接"},
      {"id": "2", "content":
  "账号激活：注册后请查收激活邮件，如未收到请检查垃圾邮箱或重新发送"},
      {"id": "3", "content":
  "退款政策：购买后7天内可申请全额退款，退款将在3-5个工作日原路返回"},
      {"id": "4", "content": "定价方案：基础版免费，专业版99元/月，企业版联系销售定制"},
      {"id": "5", "content": "API调用限制：免费用户每小时100次，专业版每小时10000次"},
      {"id": "6", "content": "数据导出：支持CSV和JSON格式导出，在设置页面点击导出按钮"},
  ]

def init_knowledge_base():
    """初始化向量知识库（如果还没有数据的话）"""
    if collection.count()>0:
        return collection.count()
    for doc in documents:
        collection.add(
            ids = [doc["id"]],
            documents=[doc["content"]],
            metadatas = [{"content": doc["content"]}],
        )
    print(f"知识库初始化完成，共 {len(documents)} 条记录")

def search_knowledge(query:str,top_k:int =2)->str:
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
    )
    if not results["documents"][0]:
        return "未找到相关答案"
    return "\n".join(results["documents"][0])
#增添数据库文档
def add_knowledge(content:str,source:str = "manual")->str:
    """添加一条知识到向量库"""
    kid = str(uuid.uuid4())[:8]
    collection.add(
        ids=[kid],
        documents=[content],
        metadatas=[{"content": content, "source": source}],
    )
    return kid
#展示数据库内容
def list_knowledge():
    results = collection.get()
    if not results["ids"]:
        return []
    entries=[]
    for i , kid in enumerate(results["ids"]):
        entries.append({
            "id": kid,
            "content": results["documents"][i],
            "source": results["metadatas"][i].get("source", "unknown"),
        })
    return entries
#删除数据库内容
def delete_knowledge(kid: str) -> bool:
    """删除一条知识"""
    collection.delete(ids=[kid])
    return True
#文本切块函数
def chunk_text(text:str,chunk_size:int =200,overlap:int = 50)->list:
    """把长文本切成小块，每块之间重叠 overlap 个字"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk:
            chunks.append(chunk)
        start += chunk_size-overlap
    return chunks


def add_knowledge_from_text(text: str, source: str = "file") -> list:
    """把文本切分后全部入库。返回生成的 ID 列表"""
    chunks = chunk_text(text)
    ids = []
    for chunk in chunks:
        kid = add_knowledge(chunk, source=source)
        ids.append(kid)
    return ids

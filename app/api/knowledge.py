from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.services.knowledge_base import (
    add_knowledge,
    list_knowledge,
    delete_knowledge,
    add_knowledge_from_text,
)

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


class KnowledgeCreate(BaseModel):
    content: str
    source: str = "manual"


@router.get("")
def get_all():
    """获取所有知识条目"""
    return list_knowledge()


@router.post("")
def create(req: KnowledgeCreate):
    """添加一条知识"""
    kid = add_knowledge(req.content, req.source)
    return {"id": kid, "message": "添加成功"}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """上传文件（.txt），自动切分入库"""
    if not file.filename.endswith(".txt"):
        raise HTTPException(400, "仅支持 .txt 文件")
    content = await file.read()
    text = content.decode("utf-8")
    ids = add_knowledge_from_text(text, source=file.filename)
    return {"ids": ids, "count": len(ids), "message": f"已导入 {len(ids)} 条知识"}


@router.delete("/{kid}")
def delete(kid: str):
    """删除一条知识"""
    delete_knowledge(kid)
    return {"message": "删除成功"}
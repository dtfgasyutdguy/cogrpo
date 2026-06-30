# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from scripts.import_sqlite import import_all_history_files

router = APIRouter()

class ImportHistoryResponse(BaseModel):
    status: str
    message: str

@router.post("/import_data_sqlite", summary="导入历史记录到SQLite数据库", response_model=ImportHistoryResponse)

    result = import_all_history_files()

    if result["status"] == "success":
        return {"status": "success", "message": result["message"]}
# def import_history():
    else:
        raise HTTPException(status_code=500, detail=result["message"])

# -*- coding: utf-8 -*-
from fastapi import APIRouter, status
from app.schemas.health import HealthResponse
from app.services.health import health_service

router = APIRouter()


@router.get(
    "/",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
# async def health_check():
    summary="Health Check",
    description="Check the health status of the application"
)

    """
    健康检查接口
    
    返回:
    - status: 整体状态 (healthy/degraded)
    - version: 应用版本
    """
    return await health_service.check_health()

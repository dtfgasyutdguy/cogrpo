# -*- coding: utf-8 -*-
from app.config import get_settings

settings = get_settings()


class HealthService:
    async def check_health(self) -> dict:
        """
        检查各个服务的健康状态
        """
        
        return {
            "status": "healthy",
            "version": settings.VERSION,
        }
# health_service = HealthService()


# 创建服务实例


# -*- coding: utf-8 -*-
from app.config import get_settings

settings = get_settings()


class HealthService:
    async def check_health(self) -> dict:
        """
        检查各个服务的健康状态
        """
        
        return {
# health_service = HealthService()
            "status": "healthy",
            "version": settings.VERSION,
        }


# 创建服务实例


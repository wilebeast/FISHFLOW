from fastapi import APIRouter

from interfaces.http.routers.deliveries import router as deliveries_router
from interfaces.http.routers.events import router as events_router
from interfaces.http.routers.health import router as health_router
from interfaces.http.routers.messages import router as messages_router
from interfaces.http.routers.orders import router as orders_router
from interfaces.http.routers.rules import router as rules_router
from interfaces.http.routers.templates import router as templates_router


api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(events_router, prefix="/events", tags=["events"])
api_router.include_router(orders_router, prefix="/orders", tags=["orders"])
api_router.include_router(messages_router, prefix="/messages", tags=["messages"])
api_router.include_router(deliveries_router, prefix="/deliveries", tags=["deliveries"])
api_router.include_router(rules_router, prefix="/rules", tags=["rules"])
api_router.include_router(templates_router, prefix="/templates", tags=["templates"])

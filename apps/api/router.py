from fastapi import APIRouter

from interfaces.http.routers.accounts import router as accounts_router
from interfaces.http.routers.ai_reply import router as ai_reply_router
from interfaces.http.routers.audit import router as audit_router
from interfaces.http.routers.conversations import router as conversations_router
from interfaces.http.routers.deliveries import router as deliveries_router
from interfaces.http.routers.events import router as events_router
from interfaces.http.routers.health import router as health_router
from interfaces.http.routers.inventory import router as inventory_router
from interfaces.http.routers.messages import router as messages_router
from interfaces.http.routers.notifications import router as notifications_router
from interfaces.http.routers.orders import router as orders_router
from interfaces.http.routers.products import router as products_router
from interfaces.http.routers.rules import router as rules_router
from interfaces.http.routers.system import router as system_router
from interfaces.http.routers.templates import router as templates_router


api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(events_router, prefix="/events", tags=["events"])
api_router.include_router(accounts_router, prefix="/accounts", tags=["accounts"])
api_router.include_router(orders_router, prefix="/orders", tags=["orders"])
api_router.include_router(products_router, prefix="/products", tags=["products"])
api_router.include_router(conversations_router, prefix="/conversations", tags=["conversations"])
api_router.include_router(messages_router, prefix="/messages", tags=["messages"])
api_router.include_router(deliveries_router, prefix="/deliveries", tags=["deliveries"])
api_router.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
api_router.include_router(rules_router, prefix="/rules", tags=["rules"])
api_router.include_router(templates_router, prefix="/templates", tags=["templates"])
api_router.include_router(notifications_router, prefix="/notifications", tags=["notifications"])
api_router.include_router(audit_router, prefix="/audit", tags=["audit"])
api_router.include_router(ai_reply_router, prefix="/ai/reply", tags=["ai-reply"])
api_router.include_router(system_router, prefix="/system", tags=["system"])

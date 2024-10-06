from ninja import Router

from core.api.v1.main.handlers import router as main_router


router = Router(tags=["v1"])

router.add_router("", main_router, tags=["main"])

from ninja import Router

from core.api.v1.main.handlers import router as main_router
from core.api.v1.users.handlers import router as user_router


router = Router(tags=["v1"])

router.add_router("", main_router, tags=["main"])
router.add_router("user/", user_router, tags=["user"])

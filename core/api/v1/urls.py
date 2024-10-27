from ninja import Router

from core.api.v1.carts_products.handlers import router as cart_router
from core.api.v1.main.handlers import router as main_router
from core.api.v1.orders.handlers import router as order_router
from core.api.v1.packet.handlers import router as packet_router
from core.api.v1.users.handlers import router as user_router


router = Router(tags=["v1"])

router.add_router("", main_router, tags=["main"])
router.add_router("user/", user_router, tags=["user"])
router.add_router("packet/", packet_router, tags=["packet"])
router.add_router("cart/", cart_router, tags=["cart"])
router.add_router("order/", order_router, tags=["order"])

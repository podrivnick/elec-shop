from core.apps.main.utils.main import GetUserModel
from core.apps.packet.models.cart import Cart


def get_carts(request):
    if request.user.is_authenticated:
        return (
            Cart.objects.filter(user=request.user)  # noqa
            .select_related("product")
            .order_by("-quantity")
        )

    if not request.session.session_key:
        request.session.create()

    return Cart.objects.filter(session_key=request.session.session_key).order_by(  # noqa
        "-quantity",  # noqa
    )  # noqa


class UserOrSessionKeyMixin:
    def get_user_or_created_session_key(self):
        if self.request.user.is_authenticated:
            user_model = GetUserModel(self.request.user)
            user = user_model.get_user_model()

            return user, True
        else:
            return self.request.session.session_key, False

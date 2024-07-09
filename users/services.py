from packet.models import Cart
from django.contrib.auth import get_user_model


class AddSessionCartToUser:
    def __init__(self, session_key, user):
        self.session_key = session_key
        self.user = user

    def add_session_cart_to_user(self):
        if self.session_key:
            Cart.objects.filter(session_key=self.session_key).update(user=self.user)


class ChangeProfileUserData:
    def __init__(self, user, new_data_profile):
        self.user = user
        self.new_data_profile = new_data_profile

    def change_profile(self):
        if self.user and self.new_data_profile:

            for par, value in self.new_data_profile.items():
                if not value:
                    continue
                setattr(self.user, par, value)
                self.user.save(update_fields=[par])


class UpdateProfileAvatarUsername:
    def __init__(self, user, data, files):
        self.user = user
        self.data = data
        self.files = files

    def change_avatar_or_username(self):
        User = get_user_model()

        self.user.username = self.data.get('username', self.user.username)

        if self.files.get('avatar'):
            self.user.image = self.files['avatar']

        self.user.save()
        return self.user

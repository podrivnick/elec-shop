from django.contrib.auth.models import (
    AbstractUser,
    Group,
    Permission,
)
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models


class User(AbstractUser):
    image = models.ImageField(
        upload_to="avatars/%Y/%m/%d/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Телефон",
        default="+380 00 000 00 00",
    )
    age = models.PositiveIntegerField(
        default=0,
        verbose_name="Возраст",
        validators=[MinValueValidator(16), MaxValueValidator(90)],
    )

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
    )

    class Meta:
        db_table = "user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

from django.contrib.auth import get_user_model
from django.db import models


class Favorites(models.Model):
    product_id = models.IntegerField(verbose_name="Товар")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        db_table = "favorite"
        verbose_name = "Избранные"
        ordering = ("id",)

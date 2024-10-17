from django.contrib.auth import get_user_model
from django.db import models

from core.apps.carts_products.entities.review import ReviewEntity
from core.apps.main.models.products import Products


class Reviews(models.Model):
    id_product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        verbose_name="Товар",
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    review = models.CharField(max_length=300, verbose_name="Отзывы")
    data_added = models.DateField()
    likes = models.IntegerField(default=0, verbose_name="Лайки")

    class Meta:
        db_table = "review"
        verbose_name = "Отзывы"

    def to_entity(
        self,
    ) -> ReviewEntity:
        return ReviewEntity(
            pk=self.pk,
            id_product=self.id_product,
            user=self.user,
            review=self.review,
            data_added=self.data_added,
            likes=self.likes,
        )


class LikesReviews(models.Model):
    id_product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        verbose_name="Товар",
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    review_id = models.ForeignKey(
        "Reviews",
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Отзыв",
    )

    class Meta:
        verbose_name = "Лайкнутые отзывы"

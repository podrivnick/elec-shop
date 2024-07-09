from django.db import models
from django.contrib.auth import get_user_model

from main_favorite.models import Products

class Opinions(models.Model):
    id_product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    opinion = models.CharField(max_length=300, verbose_name='Отзывы')
    data_added = models.DateField()
    likes = models.IntegerField(default=0, verbose_name='Лайки')

    class Meta:
        db_table = 'opinions'
        verbose_name = 'Отзывы'

class LikesOpinion(models.Model):
    id_product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    opinion_id = models.ForeignKey('Opinions', on_delete=models.CASCADE, null=True, verbose_name='Отзыв')

    class Meta:
        verbose_name = 'Лайкнутыее отзывы'
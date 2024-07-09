# Generated by Django 4.2.9 on 2024-03-07 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carts_products', '0002_initial'),
        ('main_favorite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinions',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='likesopinion',
            name='id_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_favorite.products', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='likesopinion',
            name='opinion_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='carts_products.opinions', verbose_name='Отзыв'),
        ),
        migrations.AddField(
            model_name='likesopinion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]

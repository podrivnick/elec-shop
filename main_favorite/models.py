from django.db import models
from django.contrib.auth import get_user_model

class Information(models.Model):
    text_info = models.TextField()

    class Meta:
        db_table = 'information'
        verbose_name = 'Информация'

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True, null=True, max_length=100, verbose_name='URL')
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    discount = models.DecimalField(blank=True, max_digits=10, default=0.00, decimal_places=2)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    count_product = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey('Categories_Product', on_delete=models.PROTECT, blank=True)
    id_product = models.DecimalField(decimal_places=0, max_digits=7, null=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Товары'
        ordering = ('id',)

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price

class Categories_Product(models.Model):
    category = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True, max_length=40, null=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        ordering = ('id',)


class Favorites(models.Model):
    product_id = models.IntegerField(verbose_name='Товар')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        db_table = 'favorite'
        verbose_name = 'Избранные'
        ordering = ('id',)






























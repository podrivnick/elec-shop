from django.db import models

from core.apps.common.models import TimeBaseModel


class Products(TimeBaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True, null=True, max_length=100, verbose_name="URL")
    image = models.ImageField(upload_to="products/%Y/%m/%d/")
    discount = models.DecimalField(
        blank=True,
        max_digits=10,
        default=0.00,
        decimal_places=2,
    )
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    count_product = models.PositiveIntegerField(default=0, verbose_name="Количество")
    category = models.ForeignKey(
        "Categories_Product",
        on_delete=models.PROTECT,
        blank=True,
    )
    id_product = models.DecimalField(decimal_places=0, max_digits=7, null=True)

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price

    def __str__(self):
        return self.title

    class Meta:
        db_table = "products"
        verbose_name = "Товары"
        ordering = ("id",)


class CategoriesProduct(TimeBaseModel):
    category = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True, max_length=40, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "category"
        verbose_name = "Категорию"
        ordering = ("id",)
